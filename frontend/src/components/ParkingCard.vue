<template>
  <div class="card shadow-sm mb-3">
    <div class="card-body">
      <h5 class="card-title">{{ lot.prime_location_name }}</h5>
      <p class="mb-1">{{ lot.address }}</p>
      <p class="mb-1">Available: {{ lot.available_spots }}</p>
      <p class="mb-2 fw-bold">₹{{ lot.price }} / hr</p>

      <button class="btn btn-primary"
              @click="$emit('reserve', lot.id)"
              :disabled="lot.available_spots === 0">
        Book Now
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps(["lot"])
</script>
