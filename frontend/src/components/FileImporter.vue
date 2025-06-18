<script setup lang="ts">
import { ref } from 'vue'

const selectedFile = ref(null)
const response = ref(null)
const loading = ref(false)
const error = ref('')

function onFileChange(event) {
  selectedFile.value = event.target.files[0]
}

async function uploadFile() {
  if (!selectedFile.value) {
    alert("Please select a file!")
    return
  }

  loading.value = true
  error.value = ''

  const formData = new FormData()
  formData.append("file", selectedFile.value)

  try {
    const res = await fetch("http://127.0.0.1:8000/upload-file/", {
      method: "POST",
      body: formData,
    })
    
    if (res.ok) {
      response.value = await res.json()
    } else {
      error.value = "Upload failed"
    }
  } catch (err) {
    console.log("Error:", err)
    error.value = "Something went wrong"
  }
  
  loading.value = false
}
</script>

<template>
  <div>
    <h2>Upload Playwright Report</h2>
    
    <div>
      <input type="file" @change="onFileChange" />
      <button @click="uploadFile" :disabled="loading">
        {{ loading ? 'Uploading...' : 'Upload' }}
      </button>
    </div>

    <div v-if="error" style="color: red; margin: 10px 0;">
      {{ error }}
    </div>

    <div v-if="response" style="background: lightgreen; padding: 10px; margin: 10px 0;">
      <p>{{ response.message }}</p>
      <p>Tests processed: {{ response.test_runs_count }}</p>
    </div>

    <div style="margin-top: 20px;">
      <h3>How to use:</h3>
      <p>1. Run: npx playwright test --reporter=json</p>
      <p>2. Find the JSON file</p>
      <p>3. Upload it here</p>
    </div>
  </div>
</template>

<style scoped>
button {
  margin-left: 10px;
  padding: 5px 10px;
}

input {
  margin: 10px 0;
}
</style>
