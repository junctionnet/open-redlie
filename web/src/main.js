import * as Vue from 'vue' // in Vue 3
// import { createApp } from 'vue';
import App from './App.vue'

import { Amplify } from 'aws-amplify';
import awsconfig from './aws-exports';

import PrimeVue from 'primevue/config';
// import Lara from '@/presets/lara';      //import preset
import 'primevue/resources/themes/aura-light-green/theme.css'
// import DataViewLayoutOptions from 'primevue/dataviewlayoutoptions'   // optional
import Button from "primevue/button"
import { ref } from 'vue';
import FileUpload from 'primevue/fileupload';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import ColumnGroup from 'primevue/columngroup';   // optional
import Row from 'primevue/row';                   // optional
import Card from 'primevue/card';
import Divider from 'primevue/divider';
import ProgressBar from 'primevue/progressbar';
import DataView from 'primevue/dataview';

import axios from 'axios'
// const apiClient = axios.create({
//     baseURL: process.env.VUE_APP_API_URL,
//     // You can add more default settings here
// });
// export default apiClient;

import VueAxios from 'vue-axios'

// import { Authenticator } from "@aws-amplify/ui-vue";
// import "@aws-amplify/ui-vue/styles.css";
//
// import { Amplify } from 'aws-amplify';
// import awsconfig from './aws-exports';
// Amplify.configure(awsconfig);



import 'primeflex/primeflex.css';
import 'primeicons/primeicons.css';
Amplify.configure(awsconfig);

const app = Vue.createApp(App);

app.use(VueAxios, axios)
app.use(PrimeVue);
app.use(ref);
// app.use(PrimeVue);
app.component("PrimeButton", Button);
app.component('DataTable', DataTable);
app.component('CiWordsTable', DataTable);
app.component('DataTableTable', DataTable);
app.component('DataColumn', Column);
app.component('ColumnGroup', ColumnGroup);
app.component('DataRow', Row);
app.component('InfoCard', Card);
app.component('InfoDivider', Divider);
app.component('ProgressBar', ProgressBar);
app.component('FileUpload', FileUpload);
app.component('DataView', DataView);
app.mount('#app')
