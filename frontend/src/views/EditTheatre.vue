<template>
  <div>
    <h3>Edit Theatre</h3>
    <form @submit.prevent="updateTheatre">
      <div>
        <label for="name">Name:</label>
        <input type="text" v-model="editedTheatre.name"  />
      </div>
      <div>
        <label for="place">Place:</label>
        <input type="text" v-model="editedTheatre.place" />
      </div>
      <div>
        <label for="capacity">Capacity:</label>
        <input type="integer" v-model="editedTheatre.capacity" />
      </div>
      <button type="submit">Update Theatre</button>
    </form>
    <button @click="goToTheatreManagementPage">Back to Theatre Management</button>
  </div>
</template>

<script>
import axios from "axios";
const API_BASE_URL = 'http://localhost:5000';
export default {
  data() {
    return {
    // const theatreId = this.$route.params.id;
      editedTheatre: {
        id: null,
        name: "",
        place: "",
        capacity: 0,
      },
      message: "",
    };
  },
  mounted() {
     // Fetch theatre details using the provided ID and populate editedTheatre
    // const theatreId = this.$route.params.id; // Get the theatre ID from the route parameter
    // this.fetchTheatreDetails(theatreId);
  },
  methods: {
    updateTheatre() {
      axios
        .put(
          `${API_BASE_URL}/theatres/${this.$route.params.id}`,
          this.editedTheatre,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('access_token')}`,
            },
          }
        )
        .then((response) => {
          this.message = response.data.message;
          // Optionally, you can navigate back to the theatres list page
        })
        .catch((error) => {
          this.message = error.response.data;
        });
    },
    goToTheatreManagementPage() {
      // Navigate to the /theatres page
      this.$router.push("/theatres");
    },
  },
};
</script>
