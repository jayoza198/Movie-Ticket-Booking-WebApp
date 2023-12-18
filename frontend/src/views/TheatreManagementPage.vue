<template>
  <div>
    <h2>Theatre Management</h2>
    <button @click="showForm = true">Add Theatre</button>

    <div class="showForm">
      <h3>Create New Theatre</h3>
      <form @submit.prevent="createTheatre">
        <div>
          <label for="name">Name:</label>
          <input type="text" v-model="name" required />
        </div>
        <div>
          <label for="place">Place:</label>
          <input type="text" v-model="place" required />
        </div>
        <div>
          <label for="capacity">Capacity:</label>
          <input type="number" v-model.number="capacity" required />
        </div>
        <button type="submit">Create Theatre</button>
      </form>
    </div>

    <div v-if="message">{{ message }}</div>

    <div v-if="theatres.length">
      <h3>Theatres List</h3>
      <ul>
        <li v-for="theatre in theatres" :key="theatre.id">
          {{ theatre.name }} - {{ theatre.place }} (Capacity: {{ theatre.capacity }})
          <button @click="editTheatre(theatre)">Edit</button>
          <button @click="deleteTheatre(theatre)">Delete</button>
        </li>
      </ul>
    </div>
    <button @click="goToAdminDashboard">Back to Admin Dashboard</button>>
  </div>
</template>

<script>
import axios from "axios";
const API_BASE_URL = 'http://localhost:5000';
export default {
  data() {
    return {
      showForm: false,
      name: "",
      place: "",
      capacity: 0,
      theatres: [],
      message: "",
    };
  },
  mounted() {
    this.getTheatres();
  },
  methods: {
    getTheatres() {
      axios.get(`${API_BASE_URL}/theatres-data`,
      {headers: {Authorization: `Bearer ${localStorage.getItem('access_token')}`, }, }).then((response) => {
        this.theatres = response.data;
      });
    },
    createTheatre() {
      axios
  .post(
    `${API_BASE_URL}/theatres`,
    {
      name: this.name,
      place: this.place,
      capacity: this.capacity,
      role: localStorage.getItem('current_user'),
    },
    {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`,
      },
    }
  )
  .then((response) => {
    this.message = response.data.message;
    this.showForm = false;
    this.name = "";
    this.place = "";
    this.capacity = 0;
    this.getTheatres();
  })
  .catch((error) => {
    this.message = error.response.data;
  });
    },
    editTheatre(theatre) {
      // Implement edit theatre logic
      // Redirect to edit theatre page or show a modal
      // For example, you can use Vue Router to navigate to the edit theatre page
      this.$router.push({ name: "EditTheatre", params: { id: theatre.id } });
    },
    deleteTheatre(theatre) {
  // Show a confirmation modal
  if (confirm("Are you sure you want to delete this theatre?")) {
    axios
      .delete(`${API_BASE_URL}/theatres/${theatre.id}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        },
      })
      .then((response) => {
        this.message = response.data.message;
        // Optionally, remove the deleted theatre from the local theatres array
        this.theatres = this.theatres.filter(t => t.id !== theatre.id);
      })
      .catch((error) => {
        if (error.response && error.response.data) {
          this.message = error.response.data;
        } else {
          this.message = "An error occurred while deleting the theatre.";
        }
      });
      }
    },
    // Add this method to handle the "Back" button
    goToAdminDashboard() {
      this.$router.push('/admin-dashboard');
    },
  },
};
</script>

<style>
/* Styles unchanged */
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

</style>
