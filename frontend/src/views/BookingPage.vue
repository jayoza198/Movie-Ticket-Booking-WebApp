<template>
  <div>
    <h2>Book Show Tickets</h2>
    <form @submit.prevent="bookTickets" class="booking-form">
      <div>
        <label for="show_name">Show Name:</label>
        <!-- Use a select element to show a dropdown of show names -->
        <select v-model="selectedShow" required>
          <option v-for="show in shows" :key="show.id" :value="show.id">{{ show.name }}</option>
        </select>
      </div>
      <div v-if="selectedShow">
        <label>Theatres:</label>
        <ul>
          <li v-for="theatre in selectedTheatres" :key="theatre.id">{{ theatre.name }}</li>
        </ul>
      </div>
      <div>
        <label for="num_tickets">Number of Tickets:</label>
        <input type="number" v-model.number="num_tickets" required />
      </div>
      <button type="submit">Book Tickets</button>
    </form>
    <div v-if="message">{{ message }}</div>
  </div>
</template>

<script>
import axios from "axios";
const API_BASE_URL = 'http://localhost:5000';
export default {
  data() {
    return {
      selectedShow: null,
      num_tickets: 0,
      message: "",
      shows: [], // Store the list of shows here
    };
  },
  created() {
    this.fetchShows(); // Fetch shows when the component is created
  },
  computed: {
    selectedTheatres() {
      if (this.selectedShow) {
        const selectedShow = this.shows.find(show => show.id === this.selectedShow);
        return selectedShow ? selectedShow.theatres : [];
      }
      return [];
    },
  },
  methods: {
    async fetchShows() {
      try {
        const response = await axios.get(`${API_BASE_URL}/shows`);
        this.shows = response.data;
      } catch (error) {
        console.error("Error fetching shows:", error);
      }
    },
    bookTickets() {
      const access_token = localStorage.getItem("access_token");
      if (!access_token) {
        this.message = "Please login to book tickets";
        return;
      }

      axios
        .post(
          `${API_BASE_URL}/bookings`,
          {
            show_id: this.selectedShow,
            num_tickets: this.num_tickets,
          },
          {
            headers: {
              Authorization: `Bearer ${access_token}`,
            },
          }
        )
        .then((response) => {
          this.message = response.data;
        })
        .catch((error) => {
          this.message = error.response.data;
        });
    },
  },
};
</script>

<style>
/* Booking.vue styles */
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

/* Form styles */
form {
  display: flex;
  flex-direction: column;
  max-width: 400px;
  margin: 0 auto;
}

label {
  font-weight: bold;
  margin-bottom: 5px;
}

input,
button {
  margin-bottom: 10px;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  outline: none;
}

button {
  cursor: pointer;
  background-color: #4caf50;
  color: white;
}

/* List styles */
ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin-bottom: 10px;
}

/* Message styles */
.message {
  margin-top: 10px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: #f2f2f2;
  color: #333;
}

.booking-form {
  max-width: 400px;
  margin: 0 auto;
}
</style>
