<template>
  <div class="container-fluid px-4 py-4">

    <h3 class="mb-4 fw-semibold">Create Parking Lot</h3>

    <div class="card glass-card mx-auto" style="max-width: 720px;">
      <div class="card-body p-4">

        <form @submit.prevent="submit">
          <div class="row g-3">

            <div class="col-md-6">
              <label class="form-label">Lot Name</label>
              <input v-model="form.name" class="form-control" required />
            </div>

            <div class="col-md-6">
              <label class="form-label">Pincode</label>
              <input v-model="form.pincode" class="form-control" required />
            </div>

            <div class="col-12">
              <label class="form-label">Address</label>
              <input v-model="form.address" class="form-control" required />
            </div>

            <div class="col-md-6">
              <label class="form-label">Max Spots</label>
              <input
                v-model.number="form.max_spots"
                type="number"
                min="1"
                class="form-control"
                required
              />
            </div>

            <div class="col-md-6">
              <label class="form-label">Hourly Price (₹)</label>
              <input
                v-model.number="form.hourly_price"
                type="number"
                min="0"
                class="form-control"
                required
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
              Create Lot
            </button>
          </div>

        </form>

      </div>
    </div>

  </div>
</template>


<script setup>
import { reactive } from "vue"
import axios from "../../api/axios"
import { useRouter } from "vue-router"

const router = useRouter()

const form = reactive({
  name: "",
  address: "",
  pincode: "",
  max_spots: 1,
  hourly_price: 0
})

async function submit() {
  try {
    await axios.post("/admin/lots", form)
    router.push("/admin/lots")
  } catch (err) {
    console.error(err)
    alert("Error creating lot")
  }
}
</script>
