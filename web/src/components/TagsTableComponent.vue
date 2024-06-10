<template>
    <h2 class="text-left">
        Recently Uploaded Tags Files
    </h2>
    <div class="card flex align-items-center justify-content-center" v-if="!props.xlsListLoading">
        <Card style="width: 45em">
            <template #header>
                <div class="flex w-full justify-content-center" style="height: 20rem;">
<!--                    <img src="../assets/invoice.gif" alt="" class="">-->
                </div>
            </template>
            <template #title>
                <p class="text-center -mt-6">Upload Tags File</p>
            </template>
            <template #subtitle>
                <p class="text-center"><b>Tags Key File .xls , .xlsx</b></p>
            </template>
            <template #content>
                <p class="m-0 text-center -mt-2">
                    The tags key file servers a similar purpose as the References key file by inputing
                    the rules for assigning references to invoices. In this case you can assign Tags to
                    Invoices. The Tags file requires the following columns: Emisor, Emisor RFC,
                    TagFilter, Hierarchy, Tag Name, Description Code, Tag Default; The tag filter will
                    try to Match the invoices data with the rules and Hierarchy as configured on the
                    Tags File, Once a match if find the process stops and the Tag is assigned, First we
                    check ProductCode a.k.a TagFilter, Then we check Description, and as last resource
                    we check for Tag Default.
                </p>
            </template>
            <template #footer>
                <div class="flex justify-content-center">
                    <Button label="Upload Tags File" icon="pi pi-upload" @click="handleButtonClick" />
                </div>
            </template>
        </Card>
    </div>
</template>
<script setup>
// const emit = defineEmits(['upload-tags', 'on-page']);

// const handleButtonClick = () => {
//     emit('upload-tags');
// };
// const onPage = () => {
//     emit('on-page')
// }
</script>

<style scoped>
:deep(.p-card) {
    box-shadow: none !important;
}
</style>