<template>
  <nav v-if="showNavbar" class="glass-navbar">
    <div class="nav-inner">
      <div class="brand">ParkEase</div>

      <ul class="nav-links">

        <!-- PUBLIC -->
        <template v-if="!isLoggedIn">
          <li>
            <router-link to="/login" class="nav-link">Login</router-link>
          </li>
          <li>
            <router-link to="/register" class="nav-link primary">Register</router-link>
          </li>
        </template>

        <!-- USER -->
        <template v-if="isLoggedIn && role === 'user'">
          <li>
            <router-link to="/user/dashboard" class="nav-link">Dashboard</router-link>
          </li>
          <li>
            <router-link to="/user/summary" class="nav-link">Summary</router-link>
          </li>
        </template>

        <!-- ADMIN -->
        <template v-if="isLoggedIn && role === 'admin'">
          <li>
            <router-link to="/admin/dashboard" class="nav-link">Dashboard</router-link>
          </li>
          <li>
            <router-link to="/admin/lots" class="nav-link">Manage Lots</router-link>
          </li>
          <li>
            <router-link to="/admin/users" class="nav-link">Users</router-link>
          </li>
          <li>
            <router-link to="/admin/summary" class="nav-link">Summary</router-link>
          </li>
        </template>

        <!-- LOGOUT -->
        <li v-if="isLoggedIn">
          <button @click="logout" class="logout-btn">Logout</button>
        </li>

      </ul>
    </div>
  </nav>
</template>

<script setup>
import { ref, watch } from "vue"
import { useRoute } from "vue-router"

const route = useRoute()

// Reactive states
const showNavbar = ref(true)
const isLoggedIn = ref(false)
const role = ref(null)

// pages where navbar must be hidden
const hideOnRoutes = ["/login", "/register"]

// Sync localStorage → reactive state
function syncAuth() {
  isLoggedIn.value = !!localStorage.getItem("access_token")
  role.value = localStorage.getItem("role")
  showNavbar.value = !hideOnRoutes.includes(route.path)
}

// Watch route change → update navbar visibility
watch(
  () => route.path,
  () => {
    syncAuth()
  }
)

// Initial sync
syncAuth()

function logout() {
  localStorage.clear()
  syncAuth()
  window.location.href = "/login"
}
</script>

<style scoped>
/* ===== GLASS NAVBAR ===== */
.glass-navbar {
  position: sticky;
  top: 16px;
  z-index: 100;

  margin: 0 auto;
  width: calc(100% - 48px);
  max-width: 1200px;

  background: rgba(15, 23, 42, 0.75);
  backdrop-filter: blur(18px);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 18px;

  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6);
}

/* ===== INNER ===== */
.nav-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 24px;
}

/* ===== BRAND ===== */
.brand {
  font-size: 1.4rem;
  font-weight: 700;
  color: #f8fafc;
}

/* ===== LINKS ===== */
.nav-links {
  display: flex;
  align-items: center;
  gap: 14px;
  list-style: none;
  margin: 0;
  padding: 0;
}

.nav-link {
  color: #cbd5f5;
  text-decoration: none;
  padding: 8px 14px;
  border-radius: 10px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.08);
  color: #f8fafc;
}

/* ACTIVE */
.nav-link.router-link-active {
  background: rgba(56, 189, 248, 0.18);
  color: #7dd3fc;
}

/* PRIMARY LINK (REGISTER) */
.nav-link.primary {
  background: linear-gradient(135deg, #2563eb, #38bdf8);
  color: white;
}

.nav-link.primary:hover {
  box-shadow: 0 10px 30px rgba(56, 189, 248, 0.35);
}

/* LOGOUT */
.logout-btn {
  background: rgba(239, 68, 68, 0.15);
  color: #fecaca;
  border: 1px solid rgba(239, 68, 68, 0.35);
  padding: 8px 14px;
  border-radius: 10px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.logout-btn:hover {
  background: rgba(239, 68, 68, 0.3);
}
</style>





