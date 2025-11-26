<template>
  <nav v-if="showNavbar" class="navbar navbar-expand-lg navbar-dark bg-dark px-3">
    <a class="navbar-brand" href="#">ParkEase</a>

    <div class="collapse navbar-collapse">
      <ul class="navbar-nav ms-auto">

        <!-- PUBLIC (when not logged in) -->
        <template v-if="!isLoggedIn">
          <li class="nav-item">
            <router-link class="nav-link" to="/login">Login</router-link>
          </li>

          <li class="nav-item">
            <router-link class="nav-link" to="/register">Register</router-link>
          </li>
        </template>

        <!-- USER -->
        <template v-if="isLoggedIn && role === 'user'">
          <li class="nav-item">
            <router-link class="nav-link" to="/user/dashboard">Dashboard</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/user/summary">Summary</router-link>
          </li>
        </template>

        <!-- ADMIN -->
        <template v-if="isLoggedIn && role === 'admin'">
          <li class="nav-item">
            <router-link class="nav-link" to="/admin/dashboard">Dashboard</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/admin/lots">Manage Lots</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/admin/users">Users</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/admin/summary">Summary</router-link>
          </li>
        </template>

        <!-- LOGOUT -->
        <li v-if="isLoggedIn" class="nav-item">
          <button @click="logout" class="btn btn-danger btn-sm ms-2">Logout</button>
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

<style>
.navbar .nav-link.router-link-active {
  font-weight: bold;
  text-decoration: underline;
}
</style>
