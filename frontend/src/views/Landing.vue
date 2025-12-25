<template>
  <div class="landing-container">
    <!-- NAV -->
    <header class="landing-nav">
      <div class="logo">ParkEase</div>

      <div class="actions">
        <router-link to="/login" class="btn ghost">Login</router-link>
        <router-link to="/register" class="btn primary">Get Started</router-link>
      </div>
    </header>

    <!-- HERO -->
    <main class="hero">
      <div class="hero-card">
        <span class="badge">Smart Parking Platform</span>

        <h1>
          Park Smarter.<br />
          Not Harder.
        </h1>

        <p>
          A modern parking management system for users and admins.
          Real-time reservations, lot analytics, and seamless control.
        </p>

        <div class="hero-actions">
          <router-link to="/register" class="btn primary large">
            Create Account
          </router-link>
          <router-link to="/login" class="btn ghost large">
            Login
          </router-link>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup></script>

<style scoped>

.landing-container {
  min-height: 100vh;
  background:
    radial-gradient(circle at top, #1e293b, #020617 70%);
  color: #e5e7eb;
  font-family: "Inter", system-ui, sans-serif;
}


.landing-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 28px 64px;
}

.logo {
  font-size: 1.7rem;
  font-weight: 700;
  color: #f8fafc;
}


.actions {
  display: flex;
  gap: 14px;
}

.btn {
  padding: 10px 20px;
  border-radius: 12px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.25s ease;
}

.btn.primary {
  background: linear-gradient(135deg, #2563eb, #38bdf8);
  color: white;
}

.btn.primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 10px 30px rgba(56, 189, 248, 0.3);
}

.btn.ghost {
  background: rgba(255, 255, 255, 0.08);
  color: #e5e7eb;
  backdrop-filter: blur(14px);
  border: 1px solid rgba(255, 255, 255, 0.15);
}

.btn.ghost:hover {
  background: rgba(255, 255, 255, 0.14);
}

.btn.large {
  padding: 14px 28px;
  font-size: 1rem;
}

/* ===== HERO ===== */
.hero {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 120px 24px;
}

.hero-card {
  max-width: 820px;
  padding: 64px;
  border-radius: 24px;

  background: rgba(15, 23, 42, 0.65);
  backdrop-filter: blur(18px);
  border: 1px solid rgba(255, 255, 255, 0.12);

  box-shadow: 0 30px 60px rgba(0, 0, 0, 0.6);
  text-align: center;
}


.badge {
  display: inline-block;
  margin-bottom: 20px;
  padding: 6px 14px;
  font-size: 0.85rem;
  border-radius: 999px;
  background: rgba(56, 189, 248, 0.15);
  color: #7dd3fc;
}

.hero-card h1 {
  font-size: 3.4rem;
  margin-bottom: 24px;
  color: #f8fafc;
}

.hero-card p {
  font-size: 1.15rem;
  line-height: 1.7;
  color: #cbd5f5;
  margin-bottom: 36px;
}

.hero-actions {
  display: flex;
  justify-content: center;
  gap: 18px;
  flex-wrap: wrap;
}
</style>
