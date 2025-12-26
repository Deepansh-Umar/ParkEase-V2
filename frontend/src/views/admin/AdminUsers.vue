<template>
  <div class="container-fluid px-4 py-4">

    <h3 class="fw-semibold mb-4">Registered Users</h3>

    <div v-if="loading" class="text-center my-4 text-muted">
      Loading...
    </div>

    <div v-else class="card glass-card">
      <div class="card-body p-0">
        <table class="table table-dark table-hover align-middle mb-0">
          <thead>
            <tr>
              <th>ID</th>
              <th>Username</th>
              <th>Email</th>
              <th>Role</th>
              <th class="text-end">Action</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="u in users" :key="u.id">
              <td>{{ u.id }}</td>
              <td class="fw-semibold">{{ u.username }}</td>
              <td>{{ u.email }}</td>
              <td>
                <span
                  class="badge"
                  :class="u.role === 'admin' ? 'bg-warning text-dark' : 'bg-info text-dark'"
                >
                  {{ u.role }}
                </span>
              </td>
              <td class="text-end">
                <button
                  class="btn btn-sm btn-outline-info"
                  @click="openSummary(u.id)"
                >
                  View Summary
                </button>
              </td>
            </tr>
          </tbody>

        </table>
      </div>
    </div>

    <!-- USER SUMMARY MODAL -->
    <div
      class="modal fade"
      tabindex="-1"
      aria-hidden="true"
      ref="modalEl"
    >
      <div class="modal-dialog modal-xl modal-dialog-scrollable">
        <div class="modal-content glass-card text-light">

          <div class="modal-header border-bottom border-secondary">
            <h5 class="modal-title fw-semibold">
              User Summary — {{ modalData.user || "" }}
            </h5>
            <button
              type="button"
              class="btn-close btn-close-white"
              data-bs-dismiss="modal"
            />
          </div>

          <div class="modal-body">

            <div v-if="modalLoading" class="text-center text-muted">
              Loading...
            </div>

            <div v-else>

              <!-- STATS -->
              <div class="row g-3 mb-4">
                <div class="col-md-4">
                  <div class="card glass-card text-center p-3">
                    <div class="stat-label">Total Bookings</div>
                    <div class="stat-value">{{ modalData.top_usage }}</div>
                  </div>
                </div>
              </div>

              <!-- BOOKINGS -->
              <h6 class="section-title mb-2">Bookings</h6>

              <div class="table-responsive mb-4" style="max-height: 300px;">
                <table class="table table-dark table-hover align-middle mb-0">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Lot</th>
                      <th>Spot</th>
                      <th>Start</th>
                      <th>Leave</th>
                      <th>Cost</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="b in modalData.bookings" :key="b.id">
                      <td>{{ b.id }}</td>
                      <td>{{ b.lot }}</td>
                      <td>{{ b.spot }}</td>
                      <td>{{ b.start_time }}</td>
                      <td>{{ b.leave_time || "-" }}</td>
                      <td>₹{{ b.total_cost || 0 }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <!-- FAVORITE SPOTS -->
              <h6 class="section-title mb-2">Favorite Spots</h6>

              <div v-if="sortedFavSpots.length">
                <ul class="list-group">
                  <li
                    v-for="spot in sortedFavSpots"
                    :key="spot.lot"
                    class="list-group-item d-flex justify-content-between align-items-center bg-transparent text-light border-secondary"
                  >
                    <span class="fw-semibold">{{ spot.lot }}</span>
                    <span class="badge bg-info text-dark rounded-pill">
                      {{ spot.count }} {{ spot.count === 1 ? "booking" : "bookings" }}
                    </span>
                  </li>
                </ul>
              </div>

              <div v-else class="text-muted fst-italic">
                No favorite spot usage found.
              </div>

            </div>
          </div>

          <div class="modal-footer border-top border-secondary">
            <button
              type="button"
              class="btn btn-secondary"
              data-bs-dismiss="modal"
            >
              Close
            </button>
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
  } finally {
    loading.value = false
  }
}

async function openSummary(userId) {
  modalLoading.value = true
  modalData.value = { user: "", bookings: [], top_usage: 0, fav_spots: [] }

  try {
    const res = await axios.get(`/admin/summary/${userId}`)
    modalData.value = res.data
  } finally {
    modalLoading.value = false

    if (!bootstrapModal) {
      bootstrapModal = new bootstrap.Modal(modalEl.value)
    }
    bootstrapModal.show()
  }
}

onMounted(loadUsers)
</script>

<style scoped>
.glass-card {
  background: rgba(15, 23, 42, 0.7);
  backdrop-filter: blur(14px);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 14px;
}

.stat-label {
  font-size: 0.8rem;
  color: #94a3b8;
  letter-spacing: 0.04em;
}

.stat-value {
  font-size: 1.6rem;
  font-weight: 600;
  color: #f8fafc;
}

.section-title {
  color: #f8fafc;
  font-weight: 600;
}

.table td, .table th {
  vertical-align: middle;
}
</style>
