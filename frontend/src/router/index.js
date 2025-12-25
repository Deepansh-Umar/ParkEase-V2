import { createRouter, createWebHistory } from "vue-router"

import Login from "../views/auth/Login.vue"
import Register from "../views/auth/Register.vue"
import Landing from "../views/Landing.vue"

import UserDashboard from "../views/user/UserDashboard.vue"
import UserSummary from "../views/user/UserSummary.vue"

import AdminDashboard from "../views/admin/AdminDashboard.vue"
import AdminLots from "../views/admin/AdminLots.vue"
import AdminSummary from "../views/admin/AdminSummary.vue"
import AdminUsers from "../views/admin/AdminUsers.vue"
import AdminCreateLot from "../views/admin/AdminCreateLot.vue"  
import AdminLotEdit from "../views/admin/AdminLotEdit.vue" 
import AdminLotSpots from "../views/admin/AdminLotSpots.vue"

const routes = [
  { path: "/", component: Landing },
  { path: "/login", component: Login },
  { path: "/register", component: Register },

  { path: "/user/dashboard", component: UserDashboard },
  { path: "/user/summary", component: UserSummary },

  { path: "/admin/dashboard", component: AdminDashboard },
  { path: "/admin/lots", component: AdminLots },
  { path: "/admin/lots/create", component: AdminCreateLot },  
  { path: "/admin/users", component: AdminUsers },
  { path: "/admin/summary", component: AdminSummary },
  { path: "/admin/lots/edit/:id", component: AdminLotEdit },
  { path : "/admin/lots/:id/spots", component : AdminLotSpots},

]

export default createRouter({
  history: createWebHistory(),
  routes
})
