import base64
import json
from http import HTTPStatus
import os
import sys
from aws_lambda_powertools import Logger, Tracer, Metrics
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, CORSConfig, Response
from aws_lambda_powertools.event_handler.exceptions import (BadRequestError, InternalServerError)
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.metrics import MetricUnit, MetricResolution
from aws_lambda_powertools.utilities.typing import LambdaContext
from src.utils.helpers import dict_to_custom_string

from src import csv_document
from src import s3_documents_repository
from src import elastic_repository

from src.services.results_service import ResultsService
sys.path.append(os.path.abspath(''))

logger = Logger(service='results')
tracer = Tracer(service='results')
metrics = Metrics(service='results', namespace='redlie')
metrics.set_default_dimensions(environment="dev")

cors_config = CORSConfig(allow_origin="*", max_age=300)
app = APIGatewayRestResolver(cors=cors_config)


results_service = ResultsService(documents_repository=s3_documents_repository, logger=logger)

@app.post("/upload")
@tracer.capture_method
def upload():
    body = app.current_event.body
    if body is None:
        raise BadRequestError("Missing required parameter: body")

    if app.current_event.get('isBase64Encoded', False):
        body = base64.b64decode(body).decode('utf-8', errors='ignore')
    boundary = app.current_event['headers']['content-type'].split("boundary=")[1]
    filedata = csv_document.parse_multipart_data(body, boundary)
    try:
        response = results_service.upload(filedata)
    except Exception as e:
        logger.exception(e)
        raise InternalServerError("ERROR results_service.upload") from e

    logger.info("Document Uploaded", extra={"data":response})

    metrics.add_metric(name="CreatedResults", unit=MetricUnit.Count, value=1, resolution=MetricResolution.High)
    logger.info("Upload results")
    return Response(status_code=HTTPStatus.OK.value, content_type="application/json",
                    body=json.dumps({
                        "message": "Success",
                        "show_toast": True,
                        "message_detail": "Document uploaded successfully",
                        "data": filedata[1]
                    }))

@app.get("/results")
@tracer.capture_method
def find_results():
    try:
        file_name = app.current_event.get_query_string_value("filename", None)
        file_name = file_name.replace("xlsx", "csv")
    except Exception as e:
        file_name = "uploaded_file.csv"
    exist = elastic_repository.exist(file_name)
    if exist:
        logger.info("Get document from Elastic")
        _records = elastic_repository.get_results(file_name)
        return Response(status_code=HTTPStatus.OK.value, content_type="application/json",
                    body=json.dumps(_records))
    try:
        logger.info("Proccess results from API")
        _records = results_service.process_results(file_name)
    except Exception as e:
        logger.exception(e)
        raise InternalServerError("ERROR results_service.process_results") from e

    return Response(status_code=HTTPStatus.OK.value, content_type="application/json",
                    body=json.dumps(_records.__dict__))

@app.get("/documents")
@tracer.capture_method
def get_list():
    logger.info("Get documents")
    s3_list = results_service.get_documents()
    return s3_list

def dict_to_custom_string(data):
    """
    Convert a dictionary into a 'key=value' string format separated by commas.

    Args:
    data (dict): The dictionary to convert.

    Returns:
    str: A string representation of the dictionary in the specified format.
    """
    if data is None or data == {}:
        return ''
    # Create a list to store each 'key=value' string
    result = []
    # Iterate over key-value pairs in the dictionary
    for key, value in data.items():
        # Add 'key=value' string to the list
        result.append(f"{key}:{value}")
    # Join all elements in the list with a comma
    return ', '.join(result)


@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
@tracer.capture_lambda_handler
@metrics.log_metrics(capture_cold_start_metric=True)
def proxy_handler(event, context: LambdaContext):
    query_params = event.get('queryStringParameters', {})

    if type(query_params) is dict and len(query_params) and 'organization' in query_params.keys():
        query_params.pop('organization')

    env = os.getenv('STAGE', 'dev')
    logger.append_keys(method=event.get('httpMethod'))
    logger.append_keys(resource=event.get('resource'))
    logger.append_keys(request_params=dict_to_custom_string(query_params))
    logger.append_keys(query_params=query_params)
    logger.append_keys(organization="redlie")
    logger.append_keys(username="test")
    logger.append_keys(application='RedLie')
    logger.append_keys(env=env)
    # logger.debug("App Params Config Debug", extra=env_parameters.config)
    # logger.info("App Params Config Info", extra=env_parameters.config)
    print("*" * 88)
    print("==================================== Results API ====================================")
    print("*" * 88)
    response = app.resolve(event, context)
    metrics.flush_metrics()
    return response