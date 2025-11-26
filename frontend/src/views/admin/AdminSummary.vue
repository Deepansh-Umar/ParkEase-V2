<template>
  <div class="container mt-4">

    <h3>Admin Summary</h3>

    <div class="row mt-4">

      <!-- Top Users -->
      <div class="col-md-6">
        <div class="card p-3">
          <h5>Top Users (Most Reservations)</h5>
          <canvas ref="usersChart"></canvas>
        </div>
      </div>

      <!-- Top Lots -->
      <div class="col-md-6">
        <div class="card p-3">
          <h5>Top Parking Lots (By Usage)</h5>
          <canvas ref="lotsChart"></canvas>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import axios from "../../api/axios"
import Chart from "chart.js/auto"

const usersChart = ref(null)
const lotsChart = ref(null)

const chartColors = [
  "#4e79a7", "#f28e2b", "#e15759",
  "#76b7b2", "#59a14f", "#edc949",
  "#af7aa1", "#ff9da7", "#9c755f", "#bab0ac"
]

async function load() {
  const res = await axios.get("/admin/lotwise_summary")

  const users = res.data.top_users
  const lots = res.data.top_lots

  // --- Users Chart ---
  new Chart(usersChart.value, {
    type: "bar",
    data: {
      labels: users.map(u => u.username),
      datasets: [
        {
          label: "Reservations",
          data: users.map(u => u.count),
          backgroundColor: chartColors.slice(0, users.length),
          borderColor: "#333",
          borderWidth: 1
        }
      ]
    }
  })

  // --- Lots Chart ---
  new Chart(lotsChart.value, {
    type: "pie",
    data: {
      labels: lots.map(l => l.name),
      datasets: [
        {
          data: lots.map(l => l.count),
          backgroundColor: chartColors.slice(0, lots.length)
        }
      ]
    }
  })
}

onMounted(load)
</script>
