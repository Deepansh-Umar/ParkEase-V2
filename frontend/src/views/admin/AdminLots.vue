<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h3>Parking Lots</h3>
      <router-link class="btn btn-success" to="/admin/lots/create">Add New</router-link>
    </div>

    <table class="table table-striped table-bordered">
      <thead class="table-dark">
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Address</th>
          <th>Pincode</th>
          <th>Price/hr</th>
          <th>Max Spots</th>
          <th>In Use</th>
          <th>Action</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="lot in lots" :key="lot.id">
          <td>{{ lot.id }}</td>
          <td>{{ lot.name }}</td>
          <td>{{ lot.address }}</td>
          <td>{{ lot.pincode }}</td>
          <td>{{ lot.hourly_price }}</td>
          <td>{{ lot.max_spots }}</td>
          <td>{{ lot.in_use }}</td>

          <td>
            <button class="btn btn-warning btn-sm me-2"
                    :disabled="lot.in_use > 0"
                    @click="openEdit(lot)">
              Edit
            </button>

            <button class="btn btn-danger btn-sm me-2"
                    :disabled="lot.in_use > 0"
                    @click="deleteLot(lot.id)">
              Delete
            </button>

            <button class="btn btn-danger btn-sm me-2"
                    @click="Spots_view(lot.id)">
              View Spots
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "../../api/axios";
import { useRouter } from "vue-router";

const router = useRouter();
const lots = ref([]);

async function load() {
  const res = await axios.get("/admin/lots");
  lots.value = res.data;
}

function openEdit(lot) {
  router.push(`/admin/lots/edit/${lot.id}`);
}
function Spots_view(id) {
  router.push(`/admin/lots/${id}/spots`);
}

async function deleteLot(id) {
  if (!confirm("Delete this lot?")) return;

  try {
    await axios.delete(`/admin/lots/${id}`);
    alert("Lot deleted");
    await load();
  } catch (e) {
    alert(e.response?.data?.error || "Cannot delete lot");
  }
}

onMounted(load);
</script>
