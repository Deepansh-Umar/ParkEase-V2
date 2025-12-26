<template>
  <div class="container-fluid px-4 py-4">

    <h3 class="mb-4 fw-semibold">Admin Summary</h3>

    <!-- STATS -->
    <div class="row g-4 mb-4">
      <div class="col-md-3" v-for="s in stats" :key="s.label">
        <div class="card glass-card text-center">
          <div class="card-body">
            <div class="stat-label">{{ s.label }}</div>
            <div class="stat-value">{{ s.value }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- ACTION -->
    <div class="mb-4">
      <button class="btn btn-primary" @click="exportAllReservations">
        Export All Reservations (CSV)
      </button>
    </div>

    <!-- CHARTS -->
    <div class="row g-4">
      <div class="col-md-6">
        <div class="card glass-card">
          <div class="card-body">
            <h5 class="section-title mb-3">
              Top Users (Most Reservations)
            </h5>
            <div style="height: 320px;">
              <canvas ref="usersChart"></canvas>
            </div>
          </div>
        </div>
      </div>

      <div class="col-md-6">
        <div class="card glass-card">
          <div class="card-body">
            <h5 class="section-title mb-3">
              Top Parking Lots (By Usage)
            </h5>
            <div style="height: 320px;">
              <canvas ref="lotsChart"></canvas>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>


<script setup>
import { ref, onMounted, computed } from "vue"
import axios from "../../api/axios"
import Chart from "chart.js/auto"

const usersChart = ref(null)
const lotsChart = ref(null)

const rawData = ref({
  users: [],
  lots: [],
  total_reservations: 0,
  total_revenue: 0,
  total_users: 0
})

const chartColors = [
  "#38bdf8", "#22c55e", "#facc15",
  "#fb7185", "#a78bfa", "#f97316"
]

function formatK(num) {
  if (num >= 1000000) return (num / 1000000).toFixed(1) + "M"
  if (num >= 1000) return (num / 1000).toFixed(1) + "k"
  return num
}

async function exportAllReservations() {
  const res = await axios.post("/admin/export")
  const taskId = res.data.task_id

  const interval = setInterval(async () => {
    const check = await axios.get(`/admin/task/${taskId}`)
    if (check.data.status === "SUCCESS") {
      clearInterval(interval)
      window.location.href =
        `${window.location.origin}/api/admin/download/${taskId}`
    }
  }, 1500)
}

async function load() {
  const res = await axios.get("/admin/lotwise_summary")

  rawData.value.users = res.data.top_users || []
  rawData.value.lots = res.data.top_lots || []
  rawData.value.total_reservations = res.data.total_reservations || 0
  rawData.value.total_revenue = res.data.total_revenue || 0
  rawData.value.total_users = res.data.total_users || 0

  drawCharts()
}

function drawCharts() {
  new Chart(usersChart.value, {
    type: "bar",
    data: {
      labels: rawData.value.users.map(u => u.username),
      datasets: [{
        data: rawData.value.users.map(u => u.count),
        backgroundColor: chartColors
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false }
      },
      scales: {
        x: {
          ticks: { color: "#cbd5f5" },
          grid: { color: "rgba(255,255,255,0.05)" }
        },
        y: {
          ticks: { color: "#cbd5f5" },
          grid: { color: "rgba(255,255,255,0.05)" }
        }
      }
    }
  })

  new Chart(lotsChart.value, {
  type: "pie",
  data: {
    labels: rawData.value.lots.map(l => l.name),
    datasets: [{
      data: rawData.value.lots.map(l => l.count),
      backgroundColor: chartColors
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: "bottom",
        labels: {
          color: "#e5e7eb",
          padding: 16,
          boxWidth: 14
        }
      }
    }
  }
  })
}
const stats = computed(() => {
  const favLot =
    rawData.value.lots[0]?.name || "-"

  return [
    {
      label: "Total Reservations",
      value: formatK(rawData.value.total_reservations)
    },
    {
      label: "Total Revenue",
      value: `₹${formatK(rawData.value.total_revenue)}`
    },
    {
      label: "Total Users",
      value: formatK(rawData.value.total_users)
    },
    {
      label: "Most Used Lot",
      value: favLot
    }
  ]
})

onMounted(load)
</script>
