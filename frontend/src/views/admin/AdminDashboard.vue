<template>
  <div class="container-fluid px-4 py-4">

    <!-- HEADER -->
    <h3 class="fw-semibold mb-4">Admin Dashboard</h3>

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

    <!-- ACTIVE RESERVATIONS -->
    <div class="card glass-card">
      <div class="card-body">

        <h5 class="section-title mb-3">Active Reservations</h5>

        <div class="table-responsive">
          <table class="table table-dark table-hover align-middle mb-0">
            <thead>
              <tr>
                <th>ID</th>
                <th>User</th>
                <th>Lot</th>
                <th>Address</th>
                <th>Spot</th>
                <th>Active Since</th>
                <th>Duration</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="r in reservations" :key="r.id">
                <td>{{ r.id }}</td>
                <td class="fw-semibold">{{ r.username }}</td>
                <td>{{ r.lot_name }}</td>
                <td>{{ r.address }}</td>
                <td>{{ r.spot_id }}</td>
                <td>{{ formatDate(r.start_time) }}</td>
                <td>
                  <span class="badge bg-info text-dark">
                    {{ formatDuration(r.start_time) }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <p v-if="!reservations.length" class="text-muted mt-3">
          No active reservations.
        </p>

      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue"
import axios from "../../api/axios"

const reservations = ref([])

async function load() {
  const res = await axios.get("/admin/active-reservations")
  reservations.value = res.data
}

function formatDate(dt) {
  return new Date(dt).toLocaleString("en-IN", {
    dateStyle: "medium",
    timeStyle: "short"
  })
}

function formatDuration(start) {
  const startTime = new Date(start)
  const now = new Date()

  const diffMinutes = Math.floor((now - startTime) / 60000)

  if (diffMinutes < 30) return "< 30 min"

  const bucket = Math.floor(diffMinutes / 30) * 30

  if (bucket < 60) return `${bucket} min`

  const hours = bucket / 60
  return Number.isInteger(hours)
    ? `${hours} hr`
    : `${hours.toFixed(1)} hr`
}

const stats = computed(() => {
  return [
    {
      label: "Active Reservations",
      value: reservations.value.length
    },
    {
      label: "Active Users",
      value: new Set(reservations.value.map(r => r.username)).size
    },
    {
      label: "Occupied Spots",
      value: reservations.value.length
    },
    {
      label: "Avg Duration",
      value: reservations.value.length
        ? `${(
            reservations.value.reduce((s, r) => {
              const mins = Math.floor(
                (Date.now() - new Date(r.start_time)) / 60000
              )
              return s + mins
            }, 0) /
            reservations.value.length /
            60
          ).toFixed(1)} hr`
        : "0 hr"
    }
  ]
})

onMounted(load)
</script>

<style scoped>
.glass-card {
  background: rgba(15, 23, 42, 0.7);
  backdrop-filter: blur(14px);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 16px;
}

.section-title {
  color: #f8fafc;
  font-weight: 600;
}

.stat-label {
  font-size: 0.85rem;
  color: #9ca3af;
  margin-bottom: 6px;
}

.stat-value {
  font-size: 1.6rem;
  font-weight: 700;
  color: #f9fafb;
}
</style>
