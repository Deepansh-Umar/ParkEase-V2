<template>
  <div class="container-fluid px-4 py-4">

    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h3 class="fw-semibold">Parking Lots</h3>
      <button class="btn btn-success" @click="goAddLot">
        + Add Lot
      </button>
    </div>

    <!-- STATS -->
    <div class="row g-3 mb-4">
      <div class="col-md-3">
        <div class="card glass-card text-center p-3">
          <h6 class="stat-label">Total Lots</h6>
          <h3 class="stat-value">{{ stats.total_lots }}</h3>
        </div>
      </div>

      <div class="col-md-3">
        <div class="card glass-card text-center p-3">
          <h6 class="stat-label">Total Spots</h6>
          <h3 class="stat-value">{{ stats.total_spots }}</h3>
        </div>
      </div>

      <div class="col-md-3">
        <div class="card glass-card text-center p-3">
          <h6 class="stat-label">Occupied</h6>
          <h3 class="stat-value">{{ stats.occupied }}</h3>
        </div>
      </div>

      <div class="col-md-3">
        <div class="card glass-card text-center p-3">
          <h6 class="stat-label">Available</h6>
          <h3 class="stat-value">{{ stats.available }}</h3>
        </div>
      </div>
    </div>

    <!-- LOTS TABLE -->
    <div class="card glass-card">
      <div class="card-body p-0">

        <table class="table table-dark table-hover align-middle mb-0">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Location</th>
              <th>Capacity</th>
              <th>Status</th>
              <th class="text-end">Actions</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="lot in lots" :key="lot.id">
              <td>{{ lot.id }}</td>
              <td class="fw-semibold">{{ lot.name }}</td>
              <td>{{ lot.address }}</td>
              <td>{{ lot.max_spots }}</td>
              <td>
                <span
                  class="badge"
                  :class="lot.active ? 'bg-success' : 'bg-secondary'"
                >
                  {{ lot.active ? "Active" : "Inactive" }}
                </span>
              </td>

              <td class="text-end">
                <button
                  class="btn btn-sm btn-outline-info me-2"
                  @click="viewSpots(lot.id)">
                  Spots
                </button>
                <button
                  class="btn btn-sm btn-outline-warning me-2"
                  :disabled="lot.active"
                  @click="editLot(lot.id)">
                  Edit
                </button>
                <button
                  class="btn btn-sm btn-outline-danger"
                  :disabled="lot.active"
                  @click="deleteLot(lot.id)">
                  Delete
                </button>
              </td>
            </tr>
          </tbody>

        </table>

      </div>
    </div>

  </div>
</template>


<script setup>
import { ref, onMounted } from "vue"
import axios from "../../api/axios"
import { useRouter } from "vue-router"

const router = useRouter()

const lots = ref([])
const stats = ref({
  total_lots: 0,
  total_spots: 0,
  occupied: 0,
  available: 0
})

async function load() {
  const res = await axios.get("/admin/lots")
  lots.value = res.data.lots
  stats.value = res.data.stats
}

function viewSpots(id) {
  router.push(`/admin/lots/${id}/spots`)
}

function editLot(id) {
  router.push(`/admin/lots/edit/${id}`)
}

async function deleteLot(id) {
  if (!confirm("Delete this lot?")) return

  try {
    await axios.delete(`/admin/lots/${id}`)
    alert("Lot deleted successfully")
    load()
  } catch (err) {
    alert(
      err.response?.data?.error ||
      "Cannot delete lot while reservations are active"
    )
  }
}


function goAddLot() {
  router.push("/admin/lots/create")
}

onMounted(load)
</script>

<style scoped>
.glass-card {
  background: rgba(15, 23, 42, 0.75);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 14px;
}
.stat-label {
  color: #9ca3af; /* soft grey, readable */
  font-size: 0.85rem;
  letter-spacing: 0.04em;
  margin-bottom: 4px;
}

.stat-value {
  color: #f9fafb; /* near white */
  font-weight: 600;
}

</style>
