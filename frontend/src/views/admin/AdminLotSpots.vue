<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h3>Parking Spots</h3>
    </div>

    <table class="table table-striped table-bordered">
      <thead class="table-dark">
        <tr>
          <th>ID</th>
          <th>Belongs to</th>
          <th>Status</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="spot in spots" :key="spot.id">
          <td>{{ spot.id }}</td>
          <td>{{ spot.lot_id }}</td>
          <td>{{ spot.status }}</td>
        </tr>
      </tbody>
    </table>
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