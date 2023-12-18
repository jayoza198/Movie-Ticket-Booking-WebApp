<template>
  <div>
    <h2>Your Bookings</h2>
    <ul>
      <li v-for="booking in bookings" :key="booking.id">
        Show: {{ booking.show_name }} - Date: {{ booking.show_date }} - Tickets: {{ booking.num_tickets }} - Amount: {{ booking.amount }}
      </li>
    </ul>
    <button @click="goToUserDashboard">Back to User Dashboard</button>>
  </div>
</template>

<script>
import axios from "axios";
const API_BASE_URL = 'http://localhost:5000';

export default {
  data() {
    return {
      bookings: [],
    };
  },
  created() {
    this.getUserBookings();
  },
  methods: {
    getUserBookings() {
      axios
        .get(`${API_BASE_URL}/view-user-bookings`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`
          }
        })
        .then((response) => {
          this.bookings = response.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    goToUserDashboard() {
      this.$router.push('/user-dashboard');
    },
  },
};
</script>