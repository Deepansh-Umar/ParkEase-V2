<template>
  <div class="container mt-5" style="max-width: 450px;">
    <h3 class="text-center mb-4">Register</h3>

    <div class="card shadow-sm p-4">
      <form @submit.prevent="registerUser">
        <div class="mb-3">
          <label class="form-label">Username</label>
          <input v-model="username" type="text" class="form-control" required />
        </div>

        <div class="mb-3">
          <label class="form-label">Email</label>
          <input v-model="email" type="email" class="form-control" required />
        </div>

        <div class="mb-3">
          <label class="form-label">Password</label>
          <input v-model="password" type="password" class="form-control" required />
        </div>

        <button class="btn btn-success w-100" type="submit">
          Register
        </button>
      </form>

      <p class="text-center mt-3">
        <router-link to="/login">Already have an account?</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import axios from "../../api/axios"
import { useRouter } from "vue-router"

const username = ref("")
const email = ref("")
const password = ref("")
const router = useRouter()

async function registerUser() {
  try {
    await axios.post("/auth/register", {
      username: username.value,
      email: email.value,
      password: password.value
    })

    alert("Account created successfully!")
    router.push("/login")
  } catch (e) {
    alert(e.response?.data?.error || "Registration failed")
  }
}
</script>
