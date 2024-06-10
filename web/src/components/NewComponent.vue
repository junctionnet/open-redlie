<template>
  <div>
    <h3>This is a new component!</h3>
  </div>
</template>

<script>
export default {
  name: 'NewComponent',
}
</script>

<style scoped>
@layer reset, primevue;

/* Reset CSS */
@layer reset {
    button,
    input {
        /* CSS to Reset */
    }
}
/* Your CSS styles for NewComponent here */
</style>
