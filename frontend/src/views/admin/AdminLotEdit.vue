<template>
  <div class="container mt-4">
    <h3>Edit Lot</h3>

    <div class="card p-4 mt-3">
      <div class="mb-3">
        <label class="form-label">Name</label>
        <input v-model="form.name" class="form-control" />
      </div>

      <div class="mb-3">
        <label class="form-label">Address</label>
        <input v-model="form.address" class="form-control" />
      </div>

      <div class="mb-3">
        <label class="form-label">Pincode</label>
        <input v-model="form.pincode" class="form-control" />
      </div>

      <div class="mb-3">
        <label class="form-label">Hourly Price</label>
        <input v-model="form.hourly_price" type="number" class="form-control" />
      </div>

      <div class="mb-3">
        <label class="form-label">Max Spots</label>
        <input v-model.number="form.max_spots" type="number" min="1" class="form-control" />
      </div>

      <button class="btn btn-primary" @click="updateLot">Save</button>
      <button class="btn btn-secondary ms-2" @click="router.push('/admin/lots')">Cancel</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import axios from "../../api/axios"
import { useRoute, useRouter } from "vue-router"

const route = useRoute()
const router = useRouter()

const id = route.params.id

const form = ref({
  name: "",
  address: "",
  pincode: "",
  hourly_price: "",
  max_spots: ""
})

async function loadLot() {
  try {
    const res = await axios.get("/admin/lots")
    const lot = res.data.find(l => l.id == id)

    if (!lot) {
      alert("Lot not found")
      return router.push("/admin/lots")
    }

    form.value = { ...lot }
  } catch {
    alert("Error loading lot")
  }
}

async function updateLot() {
  try {
    await axios.put(`/admin/lots/${id}`, form.value)
    alert("Updated successfully")
    router.push("/admin/lots")
  } catch (e) {
    alert(e.response?.data?.error || "Update failed")
  }
}

onMounted(loadLot)
</script>
