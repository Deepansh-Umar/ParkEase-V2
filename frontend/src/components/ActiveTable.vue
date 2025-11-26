<template>
  <table class="table table-bordered" v-if="active">
    <thead>
      <tr class="table-info">
        <th>Lot</th>
        <th>Spot</th>
        <th>Start Time</th>
        <th></th>
      </tr>
    </thead>

    <tbody>
      <tr>
        <td>{{ active.lot_name }}</td>
        <td>{{ active.spot_id }}</td>
        <td>{{ active.parking_timestamp }}</td>
        <td>
          <button class="btn btn-danger" @click="$emit('vacate', active.spot_id)">
            Vacate
          </button>
        </td>
      </tr>
    </tbody>
  </table>

  <p v-else class="text-muted">No active reservations.</p>
</template>

<script setup>
defineProps(["active"])
</script>
