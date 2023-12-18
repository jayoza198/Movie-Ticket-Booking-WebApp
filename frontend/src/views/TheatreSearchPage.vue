<template>
  <div>
    <h2>Search Theatres</h2>
    <form @submit.prevent="searchTheatres" class="search-form">
      <div>
        <label for="name">Theatre Name:</label>
        <select v-model="selectedTheatre">
          <option value="">-- Select Theatre Name --</option>
          <option v-for="theatre in theatres" :key="theatre.id" :value="theatre.name">{{ theatre.name }}</option>
        </select>
      </div>
      <button type="submit">Search</button>
    </form>

    <div v-if="message">{{ message }}</div>

    <div v-if="matchingTheatres.length">
      <h3>Matching Theatres</h3>
      <ul>
        <li v-for="theatre in matchingTheatres" :key="theatre.id">
          Name: {{ theatre.name }} - Place: {{ theatre.place }}
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
      selectedTheatre: "",
      theatres: [],
      matchingTheatres: [], // Store matching theatres for display
      message: "",
    };
  },
  created() {
    this.getTheatres(); // Fetch theatres when the component is created
  },
  methods: {
    getTheatres() {
      axios.get(`${API_BASE_URL}/theatres-data`, 
      { headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` } })
        .then((response) => {
          this.theatres = response.data;
        });
    },
    searchTheatres() {
      axios.get(`${API_BASE_URL}/theatres/search`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` },
        params: {
          name: this.selectedTheatre,
        },
      })
      .then((response) => {
        this.matchingTheatres = response.data.theatres; // Store matching theatres
        this.message = "";

        if (this.matchingTheatres.length === 0) {
          this.message = "No theatres found for the given name";
        }
      })
      .catch((error) => {
        this.message = error.response.data;
      });
    },
    goToAdminDashboard() {
      this.$router.push('/admin-dashboard');
    },
  },
};
</script>

<style>
/* TheatreSearchPage.vue styles */
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

select,
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
</style>
