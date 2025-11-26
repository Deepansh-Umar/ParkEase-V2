<template>
  <canvas ref="canvas"></canvas>
</template>

<script setup>
import { onMounted, ref } from "vue"
import { Chart, BarController, BarElement, CategoryScale, LinearScale } from "chart.js"

Chart.register(BarController, BarElement, CategoryScale, LinearScale)

const props = defineProps(["labels", "values"])

const canvas = ref(null)

onMounted(() => {
  new Chart(canvas.value, {
    type: "bar",
    data: {
      labels: props.labels,
      datasets: [
        {
          label: "Parking Cost (₹)",
          data: props.values
        }
      ]
    }
  })
})
</script>
