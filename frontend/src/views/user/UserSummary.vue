<template>
  <div class="container-fluid px-4 py-4">

    <h3 class="mb-4 fw-semibold">User Summary</h3>

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

    <!-- CHART -->
    <div class="card glass-card mb-4">
      <div class="card-body">
        <h5 class="section-title mb-3">Daily Parking Cost</h5>

        <div style="height: 340px;">
          <canvas ref="costChart"></canvas>
        </div>
      </div>
    </div>

    <!-- HISTORY -->
    <div class="card glass-card">
      <div class="card-body">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h5 class="section-title">Parking History</h5>

          <button class="btn btn-success btn-sm" @click="exportMyReservations">
            Download CSV
          </button>
        </div>

        <div class="table-responsive" style="max-height: 420px;">
          <table class="table table-dark table-hover align-middle mb-0">
            <thead>
              <tr>
                <th>ID</th>
                <th>Lot</th>
                <th>Spot</th>
                <th>Cost</th>
                <th>Start</th>
                <th>End</th>
                <th>Time</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="h in history" :key="h.id">
                <td>{{ h.id }}</td>
                <td>{{ h.lot_name }}</td>
                <td>{{ h.spot_id }}</td>
                <td>₹{{ h.cost }}</td>
                <td>{{ h.start }}</td>
                <td>{{ h.end }}</td>
                <td>{{ h.duration_hours }} hrs</td>
              </tr>
            </tbody>
          </table>
        </div>

        <p v-if="!history.length" class="text-muted mt-3">
          No parking history yet.
        </p>
      </div>
    </div>

  </div>
</template>



<script setup>
import { ref, onMounted, computed } from "vue"
import axios from "../../api/axios"
import Chart from "chart.js/auto"

const costChart = ref(null)
const summary = ref([])
const history = ref([])

async function exportMyReservations() {
  const res = await axios.post("/user/export")
  const taskId = res.data.task_id

  const interval = setInterval(async () => {
    const check = await axios.get(`/user/task/${taskId}`)

    if (check.data.status === "SUCCESS") {
      clearInterval(interval)
      window.location.href =
        `${window.location.origin}/api/user/download/${taskId}`
    }
  }, 1500)
}

async function load() {
  const r = await axios.get("/user/summary")
  summary.value = r.data.summary
  history.value = r.data.history
  drawCostChart()
}

function drawCostChart() {
  if (!summary.value.length) return

  const labels = summary.value.map(s => s.date)
  const values = summary.value.map(s => s.total_cost)

  new Chart(costChart.value, {
    type: "bar",
    data: {
      labels,
      datasets: [{
        label: "Cost (₹)",
        data: values,
        backgroundColor: "rgba(56, 189, 248, 0.8)",
        borderRadius: 6,
        barThickness: 32
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,

      plugins: {
        legend: {
          labels: {
            color: "#e5e7eb"
          }
        }
      },

      scales: {
        x: {
          ticks: { color: "#cbd5f5" },
          grid: { color: "rgba(255,255,255,0.05)" }
        },
        y: {
          beginAtZero: true,
          ticks: {
            color: "#cbd5f5",
            callback: v => `₹${v}`
          },
          grid: { color: "rgba(255,255,255,0.05)" }
        }
      }
    }
  })
}


const stats = computed(() => {
  if (!history.value.length) {
    return [
      { label: "Total Reservations", value: 0 },
      { label: "Total Spent", value: "₹0.00" },
      { label: "Avg Cost / Reservation", value: "₹0.00" },
      { label: "Favorite Lot", value: "-" }
    ]
  }

  const totalSpent = history.value.reduce((s, h) => s + h.cost, 0)
  const avgCost = totalSpent / history.value.length

  const lotCount = {}
  history.value.forEach(h => {
    lotCount[h.lot_name] = (lotCount[h.lot_name] || 0) + 1
  })

  const favLot = Object.keys(lotCount).reduce((a, b) =>
    lotCount[a] > lotCount[b] ? a : b
  )

  return [
    {
      label: "Total Reservations",
      value: history.value.length
    },
    {
      label: "Total Spent",
      value: `₹${totalSpent.toFixed(2)}`
    },
    {
      label: "Avg Cost / Reservation",
      value: `₹${avgCost.toFixed(2)}`
    },
    {
      label: "Favorite Lot",
      value: favLot
    }
  ]
})


onMounted(load)
</script>
