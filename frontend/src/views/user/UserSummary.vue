<template>
  <div class="container mt-4">

    <h3>User Summary</h3>

    <div class="row mt-4">
      <div class="col-md-6">
        <div class="card p-3">
          <h5>Total Cost per Day</h5>
          <canvas ref="costChart"></canvas>
        </div>
      </div>

      <div class="col-md-6">
        <div class="card p-3">
          <h5>Past History</h5>
          <table class="table table-bordered table-striped">
            <thead class="table-dark">
              <tr>
                <th>ID</th>
                <th>Lot</th>
                <th>Spot</th>
                <th>Cost</th>
                <th>Start (hrs)</th>
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
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import axios from "../../api/axios"
import Chart from "chart.js/auto"

const costChart = ref(null)
const summary = ref([])
const history = ref([])

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
        data: values
      }]
    }
  })
}

onMounted(load)
</script>
