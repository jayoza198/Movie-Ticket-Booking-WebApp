<template>
  <div>
    <h2>Search Shows</h2>
    <form @submit.prevent="searchShows" class="search-form">
      <div>
        <label for="name">Show Name:</label>
        <select v-model="selectedShow">
          <option value="">-- Select Show Name --</option>
          <option v-for="show in shows" :key="show.id" :value="show.name">{{ show.name }}</option>
        </select>
      </div>
      <button type="submit">Search</button>
    </form>

    <div v-if="message">{{ message }}</div>

    <div v-if="matchingShows.length">
      <h3>Matching Shows</h3>
      <ul>
        <li v-for="show in matchingShows" :key="show.id">
          Name: {{ show.name }} - Rating: {{ show.rating }}
        </li>
      </ul>
    </div>
    <button @click="goToUserDashboard">Back to User Dashboard</button>
  </div>
</template>

<script>
import axios from "axios";
const API_BASE_URL = 'http://localhost:5000';

export default {
  data() {
    return {
      selectedShow: "",
      shows: [],
      matchingShows: [], // Store matching shows for display
      message: "",
    };
  },
  created() {
    this.getShows(); // Fetch shows when the component is created
  },
  methods: {
    getShows() {
      axios.get(`${API_BASE_URL}/show-data`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        },
      })
      .then((response) => {
        this.shows = response.data;
      });
    },
    searchShows() {
      axios.get(`${API_BASE_URL}/shows/search`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        },
        params: {
          name: this.selectedShow,
        },
      })
      .then((response) => {
        this.matchingShows = response.data.shows; // Store matching shows
        this.message = "";
        if (this.matchingShows.length === 0) {
          this.message = "No shows found for the given name";
        }
      })
      .catch((error) => {
        this.message = error.response.data;
      });
    },
    goToUserDashboard() {
      this.$router.push('/user-dashboard');
    },
  },
};
</script>

<style>
/* SearchShowPage.vue styles */
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
