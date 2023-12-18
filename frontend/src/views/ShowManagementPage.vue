<template>
  <div>
    <h2>Show Management</h2>
    <button @click="showForm = true">Add Show</button>

    <div v-if="showForm">
      <h3>Create New Show</h3>
      <form @submit.prevent="createShow">
        <div>
          <label for="name">Name:</label>
          <input type="text" v-model="name" required />
        </div>
        <div>
          <label for="tags">Tags:</label>
          <input type="text" v-model="tags" required />
        </div>
        <div>
          <label for="rating">Rating:</label>
          <input type="number" v-model.number="rating" required />
        </div>
        <div>
          <label for="theatre_id">Theatre ID:</label>
          <input type="number" v-model.number="theatre_id" required />
        </div>
        <div>
          <label for="total_tickets">Total Tickets:</label>
          <input type="number" v-model.number="total_tickets" required />
        </div>
        <div>
          <label for="price">Price:</label>
          <input type="number" v-model.number="price" required />
        </div>
        <div>
          <label for="date">Date:</label>
          <input type="date" v-model="date" required />
        </div>
        <button type="submit">Create Show</button>
      </form>
    </div>

    <div v-if="message">{{ message }}</div>

    <div v-if="shows.length">
      <h3>Shows List</h3>
      <ul>
        <li v-for="show in shows" :key="show.id">
          {{ show.name }} - Tags: {{ show.tags }}, Rating: {{ show.rating }}, Theatre ID: {{ show.theatre_id }},
          Tickets Available: {{ show.total_tickets }}, Price: {{ show.price }}, Date: {{ show.date }}
          <button @click="editShow(show)">Edit</button>
          <button @click="deleteShow(show)">Delete</button>
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
      showForm: false,
      name: "",
      tags: "",
      rating: 0,
      theatre_id: 0,
      total_tickets: 0,
      price: 0,
      date: "",
      shows: [],
      message: "",
    };
  },
  mounted() {
    this.getShows();
  },
  methods: {
    getShows() {axios
      .get(`${API_BASE_URL}/show-data`, {
        headers: {
          Authorization: `${localStorage.getItem('access_token')}` // Corrected header format
        }
      }).then((response) => {
        this.shows = response.data;
      });
    },
    createShow() {
      axios
        .post(`${API_BASE_URL}/shows`, {
          name: this.name,
          tags: this.tags,
          rating: this.rating,
          theatre_id: this.theatre_id,
          total_tickets: this.total_tickets,
          price: this.price,
          date: this.date,
        },
        {headers: {Authorization: `Bearer ${localStorage.getItem('access_token')}`, }, })
        .then((response) => {
          this.message = response.data.message;
          this.showForm = false;
          this.name = "";
          this.tags = "";
          this.rating = 0;
          this.theatre_id = 0;
          this.total_tickets = 0;
          this.price = 0;
          this.date = "";
          this.getShows();
        })
        .catch((error) => {
          this.message = error.response.data.message;
        });
    },
    editShow(show) {
  this.$router.push({ name: "EditShow", params: { id: show.id } });
},

deleteShow(show) {
  if (confirm("Are you sure you want to delete this show?")) {
    axios
      .delete(`${API_BASE_URL}/shows/${show.id}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        },
      })
      .then((response) => {
        this.message = response.data.message;
        this.getShows();
      })
      .catch((error) => {
        if (error.response) {
          this.message = error.response.data;
        } else {
          this.message = "An error occurred while deleting the show.";
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

/* ShowManagement.vue styles */
.show-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 10px;
  margin-bottom: 10px;
}

.show-item button {
  background-color: #2196f3;
  color: white;
}
</style>
