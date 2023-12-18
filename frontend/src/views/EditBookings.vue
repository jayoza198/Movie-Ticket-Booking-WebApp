<template>
  <div>
    <h2>Edit Booking</h2>
    <form @submit.prevent="updateBooking">
      <div>
        <label for="num_tickets">Number of Tickets:</label>
        <input type="number" v-model="editedBooking.num_tickets" required />
      </div>
      <div>
        <label for="amount">Amount:</label>
        <input type="number" v-model="editedBooking.amount" required />
      </div>
      <button type="submit">Update Booking</button>
    </form>
  </div>
</template>

<script>
import axios from "axios";
const API_BASE_URL = 'http://localhost:5000';

export default {
  data() {
    return {
      editedBooking: {
        num_tickets: 0,
        amount: 0,
      },
      message: "",
    };
  },
  created() {
    this.getBookingDetails();
  },
  methods: {
    getBookingDetails() {
      const bookingId = this.$route.params.id; // Get booking ID from route parameter
      axios
        .get(`${API_BASE_URL}/view-user-bookings/${bookingId}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`
          }
        })
        .then((response) => {
          this.editedBooking = response.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    updateBooking() {
      const bookingId = this.$route.params.id; // Get booking ID from route parameter
      axios
        .put(`${API_BASE_URL}/view-user-bookings/${bookingId}`, this.editedBooking, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`
          }
        })
        .then((response) => {
          this.message = response.data.message;
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
};
</script>

<style>
/* Add any necessary styling here */
</style>
