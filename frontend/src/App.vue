<template>
  <div>
    <Navbar v-if="showNavbar" />

    <div :class="wrapperClass">
      <router-view />
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue"
import { useRoute } from "vue-router"
import Navbar from "./components/Navbar.vue"

const route = useRoute()

const fullWidthRoutes = ["/", "/login", "/register"]

const wrapperClass = computed(() =>
  fullWidthRoutes.includes(route.path)
    ? "full-width"
    : "container mt-4"
)

const showNavbar = computed(() =>
  !fullWidthRoutes.includes(route.path)
)
</script>

<style>
.full-width {
  width: 100%;
  margin: 0;
  padding: 0;
}
</style>
