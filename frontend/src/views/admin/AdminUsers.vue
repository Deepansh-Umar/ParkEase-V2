<template>
  <div class="container mt-4">
    <h3 class="mb-3">Registered Users</h3>

    <div v-if="loading" class="text-center my-4">Loading...</div>

    <table v-else class="table table-striped table-bordered">
      <thead class="table-dark">
        <tr>
          <th>ID</th>
          <th>Username</th>
          <th>Email</th>
          <th>Role</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="u in users" :key="u.id">
          <td>{{ u.id }}</td>
          <td>{{ u.username }}</td>
          <td>{{ u.email }}</td>
          <td>{{ u.role }}</td>
          <td>
            <button class="btn btn-sm btn-info me-2" @click="openSummary(u.id)">View Summary</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- User Summary Modal -->
    <div class="modal fade" id="userSummaryModal" tabindex="-1" aria-hidden="true" ref="modalEl">
      <div class="modal-dialog modal-lg modal-dialog-scrollable">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">User Summary - {{ modalData.user || "" }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" />
          </div>
          <div v-if="modalLoading" class="text-center">Loading...</div>

<div v-else>
  <!-- STATS -->
  <h6>Stats</h6>
  <div class="list-group mb-3">
    <div class="list-group-item">
      <strong>Total Bookings:</strong> {{ modalData.top_usage }}
    </div>
  </div>

  <!-- BOOKINGS TABLE -->
  <h6 class="mt-3">Bookings</h6>
  <table class="table table-bordered">
    <thead class="table-dark">
      <tr>
        <th>ID</th>
        <th>Lot</th>
        <th>Spot</th>
        <th>Start</th>
        <th>Leave</th>
        <th>Total Cost</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="b in modalData.bookings" :key="b.id">
        <td>{{ b.id }}</td>
        <td>{{ b.lot }}</td>
        <td>{{ b.spot_id }}</td>
        <td>{{ b.start_time }}</td>
        <td>{{ b.leave_time || "-" }}</td>
        <td>₹{{ b.total_cost || 0 }}</td>
      </tr>
    </tbody>
  </table>

  <!-- FAVORITE SPOTS -->
  <h6 class="mt-3">Favorite Spots</h6>

  <div v-if="sortedFavSpots.length">
    <ul class="list-group">
      <li 
        v-for="spot in sortedFavSpots" 
        :key="spot.lot" 
        class="list-group-item d-flex justify-content-between align-items-center"
      >
        <span class="fw-bold">{{ spot.lot }}</span>
        <span class="badge bg-primary rounded-pill">
          {{ spot.count }} {{ spot.count === 1 ? "booking" : "bookings" }}
        </span>
      </li>
    </ul>
  </div>

  <div v-else class="text-muted fst-italic">
    No favorite spot usage found.
  </div>
</div>

          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue"

import axios from "../../api/axios"

const users = ref([])
const loading = ref(true)

const modalEl = ref(null)
let bootstrapModal = null

const modalData = ref({
  user: "",
  bookings: [],
  top_usage: 0,
  fav_spots: []
})

const modalLoading = ref(false)

const sortedFavSpots = computed(() => {
  if (!modalData.value.fav_spots) return []
  return [...modalData.value.fav_spots].sort((a, b) => b.count - a.count)
})

async function loadUsers() {
  loading.value = true
  try {
    const res = await axios.get("/admin/users")
    users.value = res.data
  } catch (err) {
    alert(err.response?.data?.error || "Failed to load users")
  } finally {
    loading.value = false
  }
}

async function openSummary(userId) {
  modalLoading.value = true
  modalData.value = { user: "", bookings: [], top_usage: [], fav_spots: {} }

  try {
    const res = await axios.get(`/admin/summary/${userId}`)
    
    modalData.value = res.data
  } catch (err) {
    alert(err.response?.data?.error || "Failed to load user summary")
  } finally {
    modalLoading.value = false
    
    if (!bootstrapModal) {
      
      bootstrapModal = new bootstrap.Modal(modalEl.value)
    }
    bootstrapModal.show()
  }
}

onMounted(() => {
  loadUsers()
})
</script>

<style scoped>
.table td, .table th {
  vertical-align: middle;
}
</style>
