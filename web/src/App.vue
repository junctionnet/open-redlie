<template>
  <main>
    <!--
    <authenticator :hide-sign-up="true" style="margin-top: 10%;">
      <template v-slot="{ user, signOut }">
        <button @click="signOut">Sign Out</button>
    -->
    
    <div class="min-h-screen flex flex-column">
      <div class="bg-gray-900" style="height: 250px;">
        <div class="py-3 px-5 flex align-items-center justify-content-between relative lg:static"
          style="min-height: 80px;">
          <a class="text-white mr-4">
            Redlie
          </a>
          <div
            class="align-items-center flex-grow-1 justify-content-between hidden lg:flex absolute lg:static w-full bg-gray-900 left-0 top-100 z-1">
            <ul class="list-none p-0 m-0 flex lg:align-items-center select-none flex-column lg:flex-row">
              <li><a
                  class="flex px-6 p-3 lg:px-3 lg:py-2 align-items-center text-gray-400 hover:text-white hover:bg-gray-800 font-medium border-round cursor-pointer transition-colors transition-duration-150 p-ripple"
                  data-pd-ripple="true"><i class="pi pi-home mr-2"></i><span>Home</span><span role="presentation"
                    aria-hidden="true" data-p-ink="true" data-p-ink-active="false" class="p-ink" data-pc-name="ripple"
                    data-pc-section="root"></span></a></li>
            </ul>
          </div>
        </div>
        <!-- <ul
          class="list-none py-3 px-5 m-0 flex align-items-center font-medium overflow-x-auto border-top-1 border-gray-800">
          <li class="pr-3"><a class="cursor-pointer"><i class="pi pi-home text-gray-400"></i></a></li>
          <li class="px-2"><i class="pi pi-angle-right text-gray-400"></i></li>
          <li class="px-2"><a class="cursor-pointer text-gray-400 white-space-nowrap">Level 3</a></li>
        </ul> -->
      </div>
      <div class="p-5 flex flex-column flex-auto" style="margin-top: -12rem;">
        <div class="border-2 border-dashed surface-border border-round surface-section flex-auto p-5">
          
          <div class="surface-section px-4 py-8 md:px-6 lg:px-8">
            <div class="grid">
              <div class="col-12 md:col-6">
                <div class="pr-0 md:pr-8">
                  <h2>Índice de disponibilidad léxica</h2>
                  <p>
                    <b>Indicaciones REDLIE</b>
                  </p>
                  <p class="m-0">
                    Bienvenido a REDLIE, nuestro software libre para cálculo IDL. Por favor, atiende las siguientes
                    indicaciones.
                  </p>
                  <p>
                    Para poder procesar tus datos, organiza tu base de datos en un documento Excel con las siguientes
                    columnas: NI (número de informante), CI (número de Centro de Interés), edad y sexo (1 para hombre, 2
                    para mujer y 0 si el informante omitió la respuesta). Asegúrate de que tu docuemento Excel tenga
                    SOLAMENTE UNA HOJA. En la cuarta columna escribe las palabras por CI separadas por comas y un punto
                    al
                    final de la lista. Asegúrate de que TODAS LAS PALABRAS ESTÉN DENTRO DE ESA CASILLA.
                  </p>
                  <p>
                    <b><br> 1. Pincha el botón "Añadir archivo" y elige tu archivo Excel (extensión.xlsx) en donde has
                      organizado tus datos.
                      <br>2. Pincha el botón "Procesar" y espera a que te arroje el resultado.
                      <br>3. Descarga tus datos en formato Excel.</b>
                  </p>
                  <p>
                    Si deseas calcular vocablos por sexo o correlación de variables, elige el botón correspondiente.
                  </p>
                </div>
              </div>
              <div class="col-12 md:col-6">
                <div class="font-medium text-3xl text-900 mb-3">
                  <input type="file" ref="fileInput" @change="handleFileUpload" style="display: none;" accept=".xlsx, .xls">
                  <button @click="openFileInput" class="custom-upload-button">Añadir archivo</button>
                  <button @click="uploadFile" class="custom-upload-button">Procesar</button>
                  <button @click="downloadFile" class="custom-upload-button">Descargar</button>
                  <div v-if="selectedFile" class="file-info">
                      <span class="file-name">{{ selectedFile.name }}</span>
                      <span class="file-progress" v-if="uploading">Uploading...</span>
                  </div>
                  <!--
                      <FileUpload ref="fileUpload" name="nicd_data[]" :url="`${apiurl}/upload`" @upload="uploadFile()" :multiple="false" accept=".txt, .csv, .xlsx" :maxFileSize="1000000" chooseLabel="Agregar archivo CSV">
                        <template #empty>
                          <p>Sube aquí tus archivos CSV.</p>
                        </template>
                      </FileUpload> 
                   -->
                </div>
                <div id="app1">
                  <h2>Rellena los datos del archivo por subir</h2>
                  <form @submit.prevent="submitForm">
                    <div class="for">
                      <label for="estudio" class="lab">Estudio:</label>
                      <input type="text" class="in" v-model.lazy="form.estudio" required>
                    </div>
                    <div class="for">
                      <label for="ubicacion" class="lab">Ubicacion:</label>
                      <input type="text" class="in" v-model.lazy="form.ubicacion" required>
                    </div>
                    <div class="for">
                      <label for="informantes" class="lab">Informantes:</label>
                      <input type="text" class="in" v-model.lazy="form.informantes" required>
                    </div>
                    <div class="for">
                      <label for="nivelEscolar" class="lab">Nivel Escolar:</label>
                      <input type="text" class="in" v-model.lazy="form.nivelEscolar" required>
                    </div>
                    <div class="for">
                      <label for="rolInformante" class="lab">Rol Informante:</label>
                      <input type="text" class="in" v-model.lazy="form.rolInformante" required>
                    </div>
                  </form>
                </div>
              </div>
            </div>
          </div>

          <!--    <ProgressBar mode="indeterminate" v-show="loading" style="height: 15px"></ProgressBar>-->
          <label for="selectSex">Sexo:</label>
          <select v-model="selectedOption" @change="handleChange">
            <option v-for="(option, index) in options" :key="index" :value="option.value">{{ option.label }}</option>
          </select>
          <h1 class="text-3xl font-bold text-900">Índice de disponibilidad léxica</h1>
          <DataTable showGridlines resizableColumns columnResizeMode="expand" v-show="!loading" :value="currentDataForTable.fakeArray" :rows="20" :rowsPerPageOptions="[20, 50, 100]"  paginator >
            <DataColumn v-for="(column, _index) in Object.keys(currentDataForTable.response)" :field="_index" :header="column">
              <template #body="{data: index}">
                  <span>
                    <strong>{{ get(currentDataForTable,`response[${column}][${index}]`, ["",""])[0] }}</strong>: <span>{{ get(currentDataForTable,`response[${column}][${index}]`, ["",""])[1] }}</span>
                  </span>
              </template>
            </DataColumn>
          </DataTable>
          <h1 class="text-3xl font-bold text-900">Statistics del archivo</h1>
          <!--    <ProgressBar mode="indeterminate" v-show="loading" style="height: 15px"></ProgressBar>-->
          <CiWordsTable v-show="!loading" :value="ci_words" paginator :rows="45" :rowsPerPageOptions="[5, 10, 20, 50]"
            scrollable scrollHeight="900px" resizableColumns columnResizeMode="expand" showGridlines
            rowGroupMode="rowspan" groupRowsBy="ni" sortMode="single" sortField="ni" :sortOrder="1"
            tableStyle="min-width: 50rem">
            <DataColumn field="ci" sortable header="CI"></DataColumn>
            <DataColumn field="total" sortable header="Total"></DataColumn>
            <DataColumn field="words" header="Words"></DataColumn>
          </CiWordsTable>

          <h1 class="text-3xl font-bold text-900">Datos del archivo</h1>
          <ProgressBar mode="indeterminate" v-show="loading" style="height: 15px"></ProgressBar>
          <DataTable v-show="!loading" :value="listData" paginator :rows="45" :rowsPerPageOptions="[5, 10, 20, 50]"
            scrollable scrollHeight="900px" resizableColumns columnResizeMode="expand" showGridlines
            rowGroupMode="rowspan" groupRowsBy="ni" sortMode="single" sortField="ni" :sortOrder="1"
            tableStyle="min-width: 50rem">
            <DataColumn field="ni" sortable header="NI"></DataColumn>
            <DataColumn field="ci" sortable header="CI"></DataColumn>
            <DataColumn field="items" header="Items"></DataColumn>
          </DataTable>
        </div>
      </div>
    </div>
  <!--
  </template>
  </authenticator>
  -->
  </main>
</template>

<script>
import axios from 'axios'; // Ensure axios is installed or use this.axios if globally available
import DataTable from "primevue/datatable";
import * as XLSX from 'xlsx';
import get from "lodash.get"
export default {
  name: 'App',
  data() {
    return {
      selectedFile: null,
      excelData: null,
      loading: false,
      listData: [],
      stats: {},
      ci_words: [],
      index: [],
      index1: [],
      index2: [],
      index3: [],
      selectedOption: "index",
      name: '',
      form: {
        estudio: '',
        ubicacion: '',
        informantes: '',
        nivelEscolar: '',
        rolInformante: ''
      },
      options: [
        { label: 'Ambos', value: 'index' }, // Replace 'data1' with your actual data variable
        { label: 'Masculino', value: 'index1' },
        { label: 'Femenino', value: 'index2' },
        { label: 'Sin Respuesta', value: 'index3' },// Replace 'data2' with your actual data variable
        // Add more options as needed
      ],
      apiurl: "https://api-redlie.edu.junctionnet.tech", // Ensure you have this variable in your .env file
    };
  },
  computed: {
    currentData() {
      let a = this[this.selectedOption];
      return a
    },
    currentDataForTable() {
      let response = this.currentData.reduce((acc, item) => {
        acc['CI ' + item.ci] = Object.keys(item.values).map((c) => {
          return [c, item.values[c]]
        });
        return acc;
      }, {});

      const responseByTotals = Object.keys(response).map((c) => {
        return response[c].length
      }).sort().pop() || 0;

      return {
        response,
        responseByTotals: responseByTotals,
        fakeArray: Array.from(Array(responseByTotals).keys()).map(  c => c  )
      }
    }
  },
  methods: {
    handleFileUpload(event) {
      this.selectedFile = event.target.files[0];
    },
    async getList() {
      try {
        let filename;
        if (this.selectedFile) {
          filename = this.name;
        } else {
          filename = 'uploaded_file.csv'; // Replace 'default.txt' with your desired default filename
        }
        const response = await axios.get(`https://api-redlie.edu.junctionnet.tech/results`, {
          params: {
            filename: filename
          }
        });
        this.listData = response.data.all_records;
        this.ci_words = response.data.ci_words2;
        this.index = response.data.disp;
        this.index1 = response.data.disp1;
        this.index2 = response.data.disp2;
        this.index3 = response.data.disp3;
        this.stats = response.data.stats;

      } catch (error) {
        console.error("There was an error fetching the data: ", error);
      } finally {
        this.loading = false;
      }
    },
    uploadFile() {
      if (this.form.estudio && this.form.ubicacion && this.form.informantes && this.form.nivelEscolar && this.form.rolInformante) {
        try {
          if (!this.selectedFile) {
            console.error('No file selected.');
            return;
          }

          // Read Excel file

          const reader = new FileReader();
          reader.onload = async (e) => {
            const data = new Uint8Array(e.target.result);
            const workbook = XLSX.read(data, { type: 'array' });
            const sheetName = workbook.SheetNames[0];
            const sheet = workbook.Sheets[sheetName];
            //const excelData = XLSX.utils.sheet_to_json(sheet, { header: 1 });
            this.excelData = XLSX.utils.sheet_to_csv(sheet, { FS: ';' });

            // Upload file
            this.name = this.form.estudio + "_" + this.form.ubicacion + "_" + this.form.informantes + "_" + this.form.nivelEscolar + "_" + this.form.rolInformante + ".xlsx"
            const formData = new FormData();
            formData.append(this.name, this.excelData);

            const uploadResponse = await fetch(`${this.apiurl}/upload`, {
              method: 'POST',
              body: formData
            });
            console.log(this.excelData)
            console.log(this.selectedFile.name)
            if (uploadResponse.ok) {
              console.log('File uploaded successfully');
              // Post data from Excel file
              // const postDataResponse = await axios.post(`${this.apiurl}/upload`, this.excelData);
              // console.log('Data posted successfully:', postDataResponse.data);
            } else {
              console.error('Failed to upload file');
            }
          };
          this.loading = true; // Start loading when the upload starts
          setTimeout(() => {
            this.getList().catch(error => {
              console.error("Error during file upload or fetching the list:", error);
            }).finally(() => {
              this.loading = false; // Stop loading once the list is refreshed or an error occurs
            });
          }, 1500); // Adjust this timeout as needed
          reader.readAsArrayBuffer(this.selectedFile);
        } catch (error) {
          console.error('Error:', error);
        }
      } else {
        alert('Rellena todos los campos de información del archivo');
      }
    },
    openFileInput() {
      // Trigger the click event of the file input element when the button is clicked
      this.$refs.fileInput.click();
    },
    handleChange() {
      // Update the 'index' variable based on the selected option
    },
    downloadFile() {
      try {
        // Prepare data for Excel export (grouped by 'ci')
        let index_map = {
          "index": this.index,
          "index1": this.index1,
          "index2": this.index2,
          "index3": this.index3
        }

        const ciGroups = new Map();
        // Group items by 'ci' value
        index_map[this.selectedOption].forEach(item => {
          const ci = item.ci;
          if (!ciGroups.has(ci)) {
            ciGroups.set(ci, []);
          }

          // Loop through each key-value pair in 'values' dictionary
          for (const [key, value] of Object.entries(item.values)) {
            ciGroups.get(ci).push({
              CI: ci,
              Vocablo: key,
              IDL: value
            });
          }
        });

        // Create a new workbook
        const wb = XLSX.utils.book_new();

        // Iterate over each 'ci' group and add a worksheet for each
        ciGroups.forEach((groupData, ci) => {
          const ws = XLSX.utils.json_to_sheet(groupData);
          XLSX.utils.book_append_sheet(wb, ws, `CI_${ci}`); // Use 'CI_' + ci as sheet name
        });

        // Generate the Excel file
        const wbout = XLSX.write(wb, { bookType: 'xlsx', type: 'array' });

        // Convert the array buffer to a Blob
        const blob = new Blob([wbout], { type: 'application/octet-stream' });

        // Create a download link
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');

        // Set download filename
        if (this.selectedFile) {
          const new_name = this.selectedFile.name;
          let lastDotIndex = new_name.lastIndexOf('.');
          let namePart = new_name.slice(0, lastDotIndex);
          let extensionPart = new_name.slice(lastDotIndex);
          let modifiedName = namePart + "_" + this.getLabelByValue(this.selectedOption) + '_index' + extensionPart;
          a.download = modifiedName;
        } else {
          a.download = "undefined_index.xlsx";
        }

        // Set download link URL
        a.href = url;

        // Append the anchor element to the document body
        document.body.appendChild(a);

        // Trigger the download
        a.click();

        // Clean up
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      } catch (error) {
        console.error('Error downloading Excel file:', error);
        // Handle error (e.g., display a message to the user)
      }
    },

    renderValuesCell(rowData) {
      const values = rowData.values; // Assuming rowData is an object representing a row in your table
      let content = '';
      for (const key in values) {
        if (Object.hasOwnProperty.call(values, key)) {
          content += `${key}: ${values[key]}, `;
        }
      }
      // Remove the trailing comma and space
      content = content.slice(0, -2);
      return content;
    },
    getLabelByValue(value) {
      // Find the corresponding label for the given value
      const selectedOption = this.options.find(option => option.value === value);
      return selectedOption ? selectedOption.label : '';
    }
  },
  created() {
    this.getList();
  },
};
</script>

<script setup>
import { Authenticator } from "@aws-amplify/ui-vue";
import "@aws-amplify/ui-vue/styles.css";

import { Amplify } from 'aws-amplify';
import awsconfig from './aws-exports'; 
Amplify.configure(awsconfig);
</script>

<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.table-like {
  white-space: nowrap;
  /* Prevent wrapping to new lines */
}

.pair-container {
  display: inline-block;
  /* Display pairs inline */
  margin-right: 20px;
  /* Add spacing between pairs */
}

.pair {
  display: inline-block;
  /* Make pairs inline-block */
  vertical-align: top;
  /* Align pairs to top */
  width: 250px;
  /* Set initial width for all pairs */
  overflow: hidden;
  /* Hide overflow for long keys */
}

.key {
  font-weight: bold;
  /* Optionally, make keys bold */
  display: inline-block;
  /* Ensure keys are displayed inline */
}

.value {
  display: inline-block;
  /* Ensure values are displayed inline */
  margin-left: 5px;
  /* Add spacing between key and value */
  vertical-align: top;
  /* Align values to top */
}

.custom-upload-button {
  background-color: #4CAF50;
  border: none;
  color: white;
  padding: 10px 20px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  cursor: pointer;
  border-radius: 4px;
}

/* Hide default file input */
input[type="file"] {
  display: none;
}

.file-info {
  margin-top: 10px;
}

.file-name {
  margin-right: 10px;
}

.file-progress {
  font-style: italic;
}

select {
  padding: 8px 12px;
  /* Adjust the padding of the select button */
  margin-left: 20px;
  border: 1px solid #ccc;
  /* Add a border to the select button */
  border-radius: 4px;
  /* Add border radius to the select button */
  background-color: #fff;
  /* Set the background color of the select button */
  font-size: 14px;
  /* Adjust the font size of the select button */
  color: #333;
  /* Set the text color of the select button */
  cursor: pointer;
  /* Change cursor to pointer when hovering over the select button */
}

form {
  max-width: 400px;
  text-align: left;
}

.for {
  margin-bottom: 15px;
  text-align: left;
}
.lab {
  display: block;
  margin-bottom: 5px;
}
.in {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}

#app1 {
  text-align: left;
}
</style>
