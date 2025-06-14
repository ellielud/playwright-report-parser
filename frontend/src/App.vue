<script setup lang="ts">
import HelloWorld from './components/HelloWorld.vue'
import TheWelcome from './components/TheWelcome.vue'
import { onMounted, type Ref, ref } from 'vue'
import axios from 'axios'
import FileImporter from '@/components/FileImporter.vue'

const goodbyeResponse: Ref<any> = ref(undefined)

onMounted(() => {
  console.log('onMounted was called!')
  axios.get('http://127.0.0.1:8000/goodbye').then(response => {
    console.log(response.data)
    goodbyeResponse.value = response.data.message;
  })
})

</script>

<template>
  <header>
    <img alt="Vue logo" class="logo" src="./assets/logo.svg" width="125" height="125" />
    {{goodbyeResponse}}
    <file-importer></file-importer>
    <div class="wrapper">
      <HelloWorld msg="You did it!" />
    </div>
  </header>

  <main>
    <TheWelcome />
  </main>
</template>

<style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>
