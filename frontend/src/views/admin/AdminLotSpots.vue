<template>
  <div class="container-fluid px-4 py-4">

    <div class="d-flex justify-content-between align-items-center mb-4">
      <h3 class="fw-semibold">Parking Spots</h3>
      <button class="btn btn-outline-secondary" @click="router.back()">
        ← Back
      </button>
    </div>

    <div class="card glass-card">
      <div class="card-body p-0">

        <table class="table table-dark table-hover align-middle mb-0">
          <thead>
            <tr>
              <th>ID</th>
              <th>Lot ID</th>
              <th>Status</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="spot in spots" :key="spot.id">
              <td>{{ spot.id }}</td>
              <td>{{ spot.lot_id }}</td>
              <td>
                <span
                  class="badge"
                  :class="spot.status === 'occupied' ? 'bg-danger' : 'bg-success'"
                >
                  {{ spot.status }}
                </span>
              </td>
            </tr>
          </tbody>

        </table>

      </div>
    </div>

  </div>
</template>


<script setup>
import { ref, onMounted } from "vue";
import axios from "../../api/axios";
import { useRouter, useRoute } from "vue-router";

const route = useRoute();           
const id = route.params.id;  
const router = useRouter();
const spots = ref([]);

async function load() {
  const res = await axios.get(`/admin/lots/${id}/spots`);
  spots.value = res.data;
}

onMounted(() => {
  load();
});
</script>

<style scoped>
.glass-card {
  background: rgba(15, 23, 42, 0.75);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 14px;
}
</style>
