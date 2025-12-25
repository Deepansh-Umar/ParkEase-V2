<template>
  <div class="auth-wrapper">
    <div class="auth-card">
      <h3 class="title">Create Account</h3>
      <p class="subtitle">Join ParkEase in just a few steps</p>

      <form @submit.prevent="registerUser">
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
          <label class="form-label">Email</label>
          <input
            v-model="email"
            type="email"
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

        <button class="btn success-btn w-100" type="submit">
          Register
        </button>
      </form>

      <div class="links">
        <router-link to="/login">Already have an account?</router-link>
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
  max-width: 450px;
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
  border-color: #22c55e;
  box-shadow: none;
  color: #f8fafc;
}

/* BUTTON */
.success-btn {
  margin-top: 10px;
  background: linear-gradient(135deg, #16a34a, #22c55e);
  border: none;
  border-radius: 12px;
  padding: 12px;
  font-weight: 600;
}

.success-btn:hover {
  box-shadow: 0 10px 30px rgba(34, 197, 94, 0.35);
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
