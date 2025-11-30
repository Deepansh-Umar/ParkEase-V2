<template>
  <div class="container mt-4">

    <h3 class="mb-3">User Dashboard</h3>

    <!-- ACTIVE RESERVATIONS TABLE -->
    <div class="card mb-4">
      <div class="card-header">Active Reservations</div>
      <div class="card-body">
        
        <div v-if="active.length > 0">
          <table class="table table-bordered table-striped">
            <thead class="table-dark">
              <tr>
                <th>Spot</th>
                <th>Lot</th>
                <th>Started At</th>
                <th>Action</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="a in active" :key="a.spot_id">
                <td>{{ a.spot_id }}</td>
                <td>{{ a.lot_name }}</td>
                <td>{{ a.start_time }}</td>
                <td>
                  <button class="btn btn-danger btn-sm" @click="vacate(a.spot_id)">
                    Vacate
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <p v-else class="text-muted">No active reservations.</p>

      </div>
    </div>

    <!-- AVAILABLE LOTS -->
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h5>Available Lots</h5>
      <router-link class="btn btn-outline-secondary" to="/user/summary">
        My Summary
      </router-link>
    </div>

    <div class="row">
      <div class="col-md-4" v-for="lot in lots" :key="lot.id">
        <div class="card shadow-sm mb-3">
          <div class="card-body">
            <h5>{{ lot.name }}</h5>
            <p class="text-muted">{{ lot.address }}</p>
            <p class="mb-2">Pincode: {{ lot.pincode }}</p>
            <p class="mb-1">Price: ₹{{ lot.hourly_price }}/hr</p>
            <p class="mb-2">Available Spots: {{ lot.available_spots }}</p>

            <button class="btn btn-success btn-sm" @click="reserve(lot.id)">
              Reserve
            </button>
          </div>
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
