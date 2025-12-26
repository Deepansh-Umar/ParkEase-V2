<template>
  <div class="container-fluid px-4 py-4">

    <h3 class="mb-4 fw-semibold">Edit Parking Lot</h3>

    <div class="card glass-card mx-auto" style="max-width: 720px;">
      <div class="card-body p-4">

        <form @submit.prevent="updateLot">
          <div class="row g-3">

            <div class="col-md-6">
              <label class="form-label">Lot Name</label>
              <input v-model="form.name" class="form-control" />
            </div>

            <div class="col-md-6">
              <label class="form-label">Pincode</label>
              <input v-model="form.pincode" class="form-control" />
            </div>

            <div class="col-12">
              <label class="form-label">Address</label>
              <input v-model="form.address" class="form-control" />
            </div>

            <div class="col-md-6">
              <label class="form-label">Hourly Price (₹)</label>
              <input
                v-model="form.hourly_price"
                type="number"
                class="form-control"
              />
            </div>

            <div class="col-md-6">
              <label class="form-label">Max Spots</label>
              <input
                v-model.number="form.max_spots"
                type="number"
                min="1"
                class="form-control"
              />
            </div>

          </div>

          <div class="d-flex justify-content-end mt-4 gap-2">
            <button
              type="button"
              class="btn btn-outline-secondary"
              @click="router.push('/admin/lots')"
            >
              Cancel
            </button>

            <button class="btn btn-primary px-4">
              Save Changes
            </button>
          </div>
        </form>

      </div>
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
    const lot = res.data.lots.find(l => l.id == id)


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
