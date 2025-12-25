<template>
  <div class="user-dashboard">

    <h3 class="page-title">User Dashboard</h3>

    <div class="glass-card mb-4">
      <div class="card-title">Active Reservations</div>

      <div v-if="active.length > 0">
        <table class="glass-table">
          <thead>
            <tr>
              <th>Spot</th>
              <th>Lot</th>
              <th>Started At</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="a in active" :key="a.spot_id">
              <td>{{ a.spot_id }}</td>
              <td>{{ a.lot_name }}</td>
              <td>{{ a.start_time }}</td>
              <td>
                <button class="danger-btn" @click="vacate(a.spot_id)">
                  Vacate
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <p v-else class="muted">No active reservations.</p>
    </div>

    <div class="section-header">
      <h5>Available Lots</h5>
      <router-link to="/user/summary" class="ghost-btn">
        My Summary
      </router-link>
    </div>

    <div class="row">
      <div class="col-md-4" v-for="lot in lots" :key="lot.id">
        <div class="glass-card lot-card">
          <h5>{{ lot.name }}</h5>
          <p class="muted">{{ lot.address }}</p>
          <p>Pincode: {{ lot.pincode }}</p>
          <p>₹{{ lot.hourly_price }}/hr</p>
          <p>Available Spots: {{ lot.available_spots }}</p>

          <button class="success-btn" @click="reserve(lot.id)">
            Reserve
          </button>
        </div>
      </div>
    </div>

  </div>
</template>


<script setup>
import { ref, onMounted } from "vue"
import axios from "../../api/axios"

const lots = ref([])
const active = ref([])

async function fetchLots() {
  const res = await axios.get("/user/lots")
  lots.value = res.data
}

async function fetchActive() {
  const res = await axios.get("/user/active")
  active.value = res.data || []
}

async function reserve(lotId) {
  try {
    const r = await axios.post(`/user/reserve/${lotId}`)
    alert(`Reserved spot ${r.data.spot_id}`)
    await fetchActive()
    await fetchLots()
  } catch (e) {
    alert(e.response?.data?.error || "Could not reserve.")
  }
}

async function vacate(spotId) {
  try {
    const r = await axios.post(`/user/release/${spotId}`)
    alert(
      `Vacated!\n
      Cost: ₹${r.data.cost}\n
      Time Parked: ${r.data.time_hours} hours\n
      From: ${r.data.start}\n
      To:   ${r.data.end}`
    )

    await fetchActive()
    await fetchLots()
  } catch (e) {
    alert(e.response?.data?.error || "Could not vacate.")
  }
}

onMounted(async () => {
  await fetchLots()
  await fetchActive()
})
</script>

<style scoped>
.user-dashboard {
  color: #e5e7eb;
}

.page-title {
  margin-bottom: 20px;
  font-weight: 600;
}

.glass-card {
  background: rgba(15, 23, 42, 0.7);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
}

.card-title {
  font-weight: 600;
  margin-bottom: 12px;
}

.glass-table {
  width: 100%;
  border-collapse: collapse;
}

.glass-table th,
.glass-table td {
  padding: 10px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.glass-table th {
  color: #cbd5f5;
  font-weight: 500;
}

.muted {
  color: #94a3b8;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.lot-card {
  margin-bottom: 16px;
}

.ghost-btn {
  color: #7dd3fc;
  text-decoration: none;
  padding: 6px 12px;
  border-radius: 10px;
}

.ghost-btn:hover {
  background: rgba(255, 255, 255, 0.08);
}

.success-btn {
  margin-top: 10px;
  background: linear-gradient(135deg, #16a34a, #22c55e);
  border: none;
  color: white;
  padding: 8px 14px;
  border-radius: 10px;
}

.danger-btn {
  background: rgba(239, 68, 68, 0.2);
  border: 1px solid rgba(239, 68, 68, 0.4);
  color: #fecaca;
  padding: 6px 12px;
  border-radius: 8px;
}
</style>

