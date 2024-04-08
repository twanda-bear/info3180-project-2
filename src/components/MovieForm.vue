<template>
    <div v-if="isError" class="alert alert-danger">
        File Upload Failed
    </div>
    <div v-if="isSuccess" class="alert alert-success">
        File Upload Successful
    </div>
    <form method="POST" id="movieForm" action="" @submit.prevent="saveMovie">
        <div class="form-group mb-3">
            <label for="title" class="form-label" required>Movie Title</label>
            <input type="text" name="title" class="form-control" />
        </div>
        <div class="form-group mb-3">
            <label for="description" class="form-label">Description</label>
            <input type="text" name="description" class="form-control" />
        </div>
        <div class="form-group mb-3">
            <label for="poster" class="form-label">Poster Image</label>
            <input type="file" name="poster" class="form-control" />
        </div>
        <button type="submit" class="btn btn-primary">Submit</button>
    </form>
</template>

<script setup>
import { ref, onMounted } from 'vue';
let csrf_token = ref("")
let isError = ref(false);
let isSuccess = ref(false);

function getCsrfToken() {
    fetch('/api/v1/csrf-token')
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            csrf_token.value = data.csrf_token;
        })
}

onMounted(() => {
    getCsrfToken();
})

let saveMovie = () => {
    let movieForm = document.getElementById('movieForm');
    let form_data = new FormData(movieForm)
    form_data.append("_csrf", csrf_token.value);
    fetch("/api/v1/movies", {
        method: 'POST',
        body: form_data,
        headers: {
            'X-CSRF-TOKEN': csrf_token.value
        },
    })
        .then(function (response) {
            console.log(form_data);
            return response.json();
        })
        .then(function (data) {
            // display a success message 
            console.log(data);
            isSuccess.value = true;
        })
        .then(async function (response) {
            if (isError.value) {
                const errorsfound = await response.json();
                errors.value = receivedErrors.errors;
            }

            return response;
        })
        .catch(function (error) {
            console.log(error);
            isError.value = true;
            isSuccess.value = false;
        });
}


</script>