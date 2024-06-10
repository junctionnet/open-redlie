import pandas as pd


def clean_csv_remove_blanks(file_path, cleaned_file_path, data=None):
    # Read the entire file into memory
    try:
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = file.readlines()
        print("Encoding utf-8")
    except Exception:
        if file_path:
            with open(file_path, 'r', encoding='latin-1') as file:
                data = file.readlines()
        print("Encoding latin-1")
    # Remove all blank spaces from each line
    print(data)
    char_replace = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', "ñ": "n", "ü": "u", ".": "", "-": "", "¿": ""}
    cleaned_data = []
    for line in data:
        line = line.lower()
        for old_char, new_char in char_replace.items():
            line = line.replace(old_char, new_char)
        cleaned_data.append(line)

    print(f"Data after special character replace  {cleaned_data[:10]}")
    with open(cleaned_file_path, 'w', encoding='utf-8') as file:
        file.writelines(cleaned_data)

    return cleaned_file_path


def pretty_print_csv(file_path):
    try:
        # Load the CSV file
        df = pd.read_csv(file_path)
        # Print the DataFrame in a pretty way
        print(df.to_string(index=False))  # Print without the DataFrame index
    except Exception as e:
        print(f"Error reading {file_path}: {e}")




def parse_multipart_data(event_body, boundary):
    parts = event_body.split(boundary)
    file_content = None
    file_name = None
    for part in parts:
        if "Content-Disposition" in part:
            file_name = part.split('name="')[1]
            file_name = file_name.split('.xlsx"', 1)[0]
            file_content = part.split("\r\n\r\n")[1].rstrip("\r\n--")
    return [file_content, file_name]


def clear_data(records, gender):
    count = 0
    for response in records:
        try:
            response["ITEMS"] = response["ITEMS"].lower()
            response["NI"] = str(int(response["NI"]))
            response["CI"] = str(int(response["CI"]))
            response["EDAD"] = str(int(response["EDAD"]))
            response["SEXO"] = str(int(response["SEXO"]))
        except Exception as e:
            if (not pd.isnull(response["NI"])) and (not pd.isnull(response["EDAD"]) and (not pd.isnull(response["SEXO"]))):
                
                print(f"Exception: Items is not string: {e} in {response} for {gender} data")
            count += 1
            continue

    print(f"[{gender}] There are {count} records empty")
    return records

