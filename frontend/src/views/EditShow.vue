<template>
  <div>
    <h2>Edit Show</h2>

    <form @submit.prevent="updateShow">
      <div>
        <label for="name">Name:</label>
        <input type="text" v-model="updatedShow.name" required />
      </div>
      <div>
        <label for="tags">Tags:</label>
        <input type="text" v-model="updatedShow.tags" />
      </div>
      <div>
        <label for="rating">Rating:</label>
        <input type="number" v-model.number="updatedShow.rating" min="0" max="10" />
      </div>
      <div>
        <label for="theatre_id">Theatre ID:</label>
        <input type="number" v-model.number="updatedShow.theatre_id" required />
      </div>
      <div>
        <label for="total_tickets">Total Tickets:</label>
        <input type="number" v-model.number="updatedShow.total_tickets" required />
      </div>
      <div>
        <label for="price">Price:</label>
        <input type="number" v-model.number="updatedShow.price" required />
      </div>
      <div>
        <label for="date">Date:</label>
        <input type="date" v-model="updatedShow.date" required />
      </div>
      <button type="submit">Update Show</button>
    </form>
    <div v-if="message">{{ message }}</div>
    <button @click="goToShowManagementPage">Back to Show Management</button>
  </div>
</template>

<script>
import axios from "axios";
const API_BASE_URL = 'http://localhost:5000';

export default {
  data() {
    return {
      updatedShow: {
        name: "",
        tags: "",
        rating: 0,
        theatre_id: 0,
        total_tickets: 0,
        price: 0,
        date: null,
      },
      message: "",
    };
  },
  created() {
    const showId = this.$route.params.id;
    // this.fetchShow(showId);
  },
  methods: {
    fetchShow(showId) {
      const id = this.$route.params.id;
      axios.get(`${API_BASE_URL}/shows/${this.id}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        },
      })
      .then((response) => {
        this.updatedShow = response.data;
      })
      .catch((error) => {
        if (error.response) {
          this.message = error.response.data;
        } else if (error.message) {
          this.message = error.message;
        } else {
          this.message = 'An error occurred while fetching the show.';
        }
      });
    },
    updateShow() {
      axios
        .put(`${API_BASE_URL}/shows/${this.$route.params.id}`, this.updatedShow, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          },
        })
        .then((response) => {
          this.message = response.data.message;
        })
        .catch((error) => {
          if (error.response) {
            this.message = error.response.data;
          } else if (error.message) {
            this.message = error.message;
          } else {
            this.message = 'An error occurred while updating the show.';
          }
        });
    },
    goToShowManagementPage() {
      this.$router.push("/shows");
    },
  },
};
</script>

