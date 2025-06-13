<script setup lang="ts">
import { ref } from 'vue'

const selectedFile = ref(null)
const response = ref(null)

function onFileChange(event) {
  selectedFile.value = event.target.files[0]
}

async function uploadFile() {
  if (!selectedFile.value) {
    alert("No file selected.")
    return
  }

  const formData = new FormData()
  formData.append("file", selectedFile.value)

  try {
    const res = await fetch("http://127.0.0.1:8000/upload-file/", {
      method: "POST",
      body: formData,
    })
    response.value = await res.json()
  } catch (err) {
    console.error("Upload failed", err)
  }
}

</script>

<template>
  <h2>Upload File</h2>
  <form @submit.prevent="uploadFile">
    <input type="file" @change="onFileChange" />
    <button type="submit">Upload</button>
  </form>

  <div v-if="response">
    <p>File size: {{ response.file_size }} bytes</p>
  </div>

</template>

<style scoped>

</style>
