<template>
  <div class="container mt-4">
    <h3>Create Parking Lot</h3>

    <form @submit.prevent="submit">
      <div class="mb-3">
        <label class="form-label">Name</label>
        <input v-model="form.name" class="form-control" required />
      </div>

      <div class="mb-3">
        <label class="form-label">Address</label>
        <input v-model="form.address" class="form-control" required />
      </div>

      <div class="mb-3">
        <label class="form-label">Pincode</label>
        <input v-model="form.pincode" class="form-control" required />
      </div>

      <div class="mb-3">
        <label class="form-label">Max Spots</label>
        <input v-model.number="form.max_spots" type="number" min="1" class="form-control" required />
      </div>

      <div class="mb-3">
        <label class="form-label">Hourly Price</label>
        <input v-model.number="form.hourly_price" type="number" min="0" class="form-control" required />
      </div>

      <button class="btn btn-primary w-100">Create Lot</button>
    </form>
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
