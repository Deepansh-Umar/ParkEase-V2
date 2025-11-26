<template>
  <div class="container mt-4">
    <h3 class="mb-4">Admin Dashboard</h3>

    <div class="row g-4">
      <div class="col-md-4">
        <div class="card shadow-sm p-3 text-center">
          <h5>Manage Lots</h5>
          <p class="text-muted">Create, edit, delete lots.</p>
          <router-link to="/admin/lots" class="btn btn-primary">Open</router-link>
        </div>
      </div>

      <div class="col-md-4">
        <div class="card shadow-sm p-3 text-center">
          <h5>Users</h5>
          <p class="text-muted">View all users.</p>
          <router-link to="/admin/users" class="btn btn-primary">Open</router-link>
        </div>
      </div>

      <div class="col-md-4">
        <div class="card shadow-sm p-3 text-center">
          <h5>Summary</h5>
          <p class="text-muted">Analytics and charts.</p>
          <router-link to="/admin/summary" class="btn btn-primary">Open</router-link>
        </div>
      </div>
    </div>
  </div>
</template>
