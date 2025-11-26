<template>
  <div class="container mt-5" style="max-width: 420px;">
    <h3 class="text-center mb-4">Login</h3>

    <div class="card shadow-sm p-4">
      <form @submit.prevent="login">
        <div class="mb-3">
          <label class="form-label">Username</label>
          <input v-model="username" type="text" class="form-control" required />
        </div>

        <div class="mb-3">
          <label class="form-label">Password</label>
          <input v-model="password" type="password" class="form-control" required />
        </div>

        <button class="btn btn-primary w-100" type="submit" :disabled="loading">
          {{ loading ? "Logging in..." : "Login" }}
        </button>
      </form>

      <p class="text-center mt-3">
        <router-link to="/register">Create an account</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import axios from "../../api/axios"
import { useRouter } from "vue-router"

const router = useRouter()
const username = ref("")
const password = ref("")
const loading = ref(false)

async function login() {
  loading.value = true
  try {
    const res = await axios.post("/auth/login", {
      username: username.value,
      password: password.value
    })

    localStorage.setItem("access_token", res.data.access_token)
    localStorage.setItem("role", res.data.role)

    if (res.data.role === "admin") router.push("/admin/dashboard")
    else router.push("/user/dashboard")

  } catch (e) {
    alert(e.response?.data?.error || "Login failed")
  }
  loading.value = false
}
</script>
