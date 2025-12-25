<template>
  <div class="auth-wrapper">
    <div class="auth-card">
      <h3 class="title">Welcome Back</h3>
      <p class="subtitle">Login to continue to ParkEase</p>

      <form @submit.prevent="login">
        <div class="mb-3">
          <label class="form-label">Username</label>
          <input
            v-model="username"
            type="text"
            class="form-control glass-input"
            required
          />
        </div>

        <div class="mb-3">
          <label class="form-label">Password</label>
          <input
            v-model="password"
            type="password"
            class="form-control glass-input"
            required
          />
        </div>

        <button
          class="btn primary-btn w-100"
          type="submit"
          :disabled="loading"
        >
          {{ loading ? "Logging in..." : "Login" }}
        </button>
      </form>

      <div class="links">
        <router-link to="/register">Create an account</router-link>
        <span>•</span>
        <router-link to="/">Back to Home</router-link>
      </div>
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

<style scoped>
/* PAGE BACKGROUND */
.auth-wrapper {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;

  background:
    radial-gradient(circle at top, #1e293b, #020617 70%);
  font-family: "Inter", system-ui, sans-serif;
}

/* CARD */
.auth-card {
  width: 100%;
  max-width: 420px;
  padding: 40px;
  border-radius: 20px;

  background: rgba(15, 23, 42, 0.75);
  backdrop-filter: blur(18px);
  border: 1px solid rgba(255, 255, 255, 0.12);

  box-shadow: 0 30px 60px rgba(0, 0, 0, 0.6);
  color: #e5e7eb;
}

/* TEXT */
.title {
  text-align: center;
  font-weight: 700;
  margin-bottom: 6px;
  color: #f8fafc;
}

.subtitle {
  text-align: center;
  font-size: 0.95rem;
  color: #cbd5f5;
  margin-bottom: 28px;
}

/* INPUTS */
.form-label {
  color: #cbd5f5;
  font-size: 0.85rem;
}

.glass-input {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: #f8fafc;
}

.glass-input:focus {
  background: rgba(255, 255, 255, 0.12);
  border-color: #38bdf8;
  box-shadow: none;
  color: #f8fafc;
}

/* BUTTON */
.primary-btn {
  margin-top: 10px;
  background: linear-gradient(135deg, #2563eb, #38bdf8);
  border: none;
  border-radius: 12px;
  padding: 12px;
  font-weight: 600;
}

.primary-btn:disabled {
  opacity: 0.7;
}

/* LINKS */
.links {
  margin-top: 22px;
  display: flex;
  justify-content: center;
  gap: 10px;
  font-size: 0.9rem;
}

.links a {
  color: #7dd3fc;
  text-decoration: none;
}

.links a:hover {
  text-decoration: underline;
}
</style>
