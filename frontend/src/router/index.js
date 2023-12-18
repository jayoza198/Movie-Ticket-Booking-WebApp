import { createRouter, createWebHistory } from 'vue-router'
// import HomeView from '../views/HomeView.vue'
import HomePage from '../views/HomePage.vue';
import SignupPage from '../views/SignupPage.vue';
import LoginPage from '../views/LoginPage.vue';
import TheatreManagementPage from '../views/TheatreManagementPage.vue';
import ShowManagementPage from '../views/ShowManagementPage.vue';
import TheatreSearchPage from '../views/TheatreSearchPage.vue';
import ShowSearchPage from '../views/ShowSearchPage.vue';
// import BookingPage from '../views/BookingPage.vue';
import DailyReminderPage from '../views/DailyReminderPage.vue';
import MonthlyReportPage from '../views/MonthlyReportPage.vue';
import UserDashboard from "@/views/UserDashboard.vue";
import AdminDashboard from "@/views/AdminDashboard.vue";
import EditTheatre from "@/views/EditTheatre.vue";
import EditShow from "@/views/EditShow.vue";
import AdminViewBooking from "@/views/AdminViewBooking.vue";
import UserBooking from "@/views/UserBooking.vue";
import ShowSearchUserPage from "@/views/ShowSearchUserPage.vue";
import TheatreSearchUserPage from "@/views/TheatreSearchUserPage.vue";
import ViewUserBookings from "@/views/ViewUserBookings.vue";
import EditBookings from "@/views/EditBookings.vue";
import AdminTheatreExport from "@/views/AdminTheatreExport.vue";

const routes = [

  { path: '/', name: 'HomePage',component: HomePage},
  { path: "/user-dashboard", component: UserDashboard, meta: { requiresAuth: true, role: "user" },},
  { path: "/admin-dashboard", component: AdminDashboard, meta: { requiresAuth: true, role: "admin" },},
  { path: '/signup', name: 'Signup',component: SignupPage },
  { path: '/login', name: 'Login', component: LoginPage },
  { path: '/theatres', name: 'Theatres', component: TheatreManagementPage },
  { path: '/edittheatre/:id', name: 'EditTheatre', component: EditTheatre },
  { path: '/editshow/:id', name: 'EditShow', component: EditShow },
  { path: '/shows', name: 'Shows', component: ShowManagementPage },
  { path: '/theatres/search', name: 'TheatreSearch', component: TheatreSearchPage },
  { path: '/shows/search', name: 'ShowSearch', component: ShowSearchPage },
  { path: '/theatres/search/user', name: 'TheatreUserSearch', component: TheatreSearchUserPage },
  { path: '/shows/search/user', name: 'ShowUserSearch', component: ShowSearchUserPage },
  // { path: '/bookings', name: 'Bookings', component: BookingPage },
  { path: "/user-booking", component: UserBooking },
  { path: "/admin-booking", component: AdminViewBooking },
  { path: "/edit-booking", component: EditBookings },
  { path: '/view-user-bookings', name: 'ViewUserBookings', component: ViewUserBookings },
  { path: '/schedule/daily-reminder', name: 'DailyReminder', component: DailyReminderPage },
  { path: '/schedule/monthly-report', name: 'MonthlyReport', component: MonthlyReportPage },
  { path: '/theatre-export', name: 'AdminTheatreExport', component: AdminTheatreExport },
  // {
  //   path: '/',
  //   name: 'home',
  //   component: HomeView
  // },
  // {
  //   path: '/about',
  //   name: 'about',
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  // }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router

// import Vue from 'vue'
// import VueRouter from 'vue-router'

// import { createRouter, createWebHistory } from "vue-router";

// Vue.use(VueRouter)

// const routes = [
  
// ];

// // const router = new VueRouter({
// //   routes
// // })
//   const router = createRouter({
//     history: createWebHistory(),
//     routes,
// })
// export default router
