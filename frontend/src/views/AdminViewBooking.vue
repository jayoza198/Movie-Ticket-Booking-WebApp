<template>
  <div>
    <h2>Admin View Bookings</h2>
    <div v-if="bookings.length">
      <h3>Bookings List</h3>
      <ul>
        <li v-for="booking in bookings" :key="booking.id">
          Show Name: {{ booking.show.name }} (ID: {{ booking.show.id }})<br>
          User ID: {{ booking.user_id }}, Number of Tickets: {{ booking.num_tickets }}, Amount: {{ booking.amount }}
        </li>
      </ul>
    </div>
    <button @click="goToAdminDashboard">Back to Admin Dashboard</button>
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
    this.fetchBookings(); // Fetch bookings when the component is created
  },
  methods: {
    async fetchBookings() {
      try {
        const response = await axios.get(`${API_BASE_URL}/admin-booking`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          },
        });
        this.bookings = response.data;
      } catch (error) {
        console.error("Error fetching bookings:", error);
      }
    },
    goToAdminDashboard() {
      this.$router.push('/admin-dashboard');
    },
  },
};
</script>

<style>
/* AdminViewBooking.vue styles */
body {
  font-family: 'Arial', sans-serif;
  margin: 0;
  padding: 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

/* List styles */
ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin-bottom: 10px;
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 4px;
}
</style>
