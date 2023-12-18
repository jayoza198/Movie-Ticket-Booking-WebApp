<template>
  <div>
    <h2>Theatre Export</h2>
    <p>Select a theatre to export its data to CSV:</p>
    <select v-model="selectedTheatre">
      <option value="">-- Select Theatre --</option>
      <option v-for="theatre in theatres" :key="theatre.id" :value="theatre.id">{{ theatre.name }}</option>
    </select>
    <button @click="exportTheatreData">Export Theatre Data</button>
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
    };
  },
  created() {
    this.fetchTheatres();
  },
  methods: {
    fetchTheatres() {
      axios.get(`${API_BASE_URL}/theatres-data`,
      { headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` } })
        .then((response) => {
          this.theatres = response.data;
        });
    },
    exportTheatreData() {
      if (this.selectedTheatre) {
        axios.get(`${API_BASE_URL}/theatre-export/${this.selectedTheatre}`, {
          responseType: 'blob', // Set response type to blob
        })
        .then((response) => {
          // Create a Blob object from the response data
          const blob = new Blob([response.data], { type: 'text/csv' });

          // Use the Blob object to create a URL for download
          const url = URL.createObjectURL(blob);

          // Create a link and trigger click to initiate download
          const link = document.createElement('a');
          link.href = url;
          link.download = `theatre_data.csv`;
          link.click();

          // Clean up the URL after download
          URL.revokeObjectURL(url);
        })
        .catch((error) => {
          console.error("Error exporting theatre data:", error);
        });
      }
    },
    goToAdminDashboard() {
      this.$router.push('/admin-dashboard');
    },
  },
};
</script>

<style>
/* TheatreExportPage.vue styles */
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

button {
  margin-top: 10px;
  padding: 8px 16px;
  font-size: 16px;
  border: none;
  border-radius: 4px;
  background-color: #4caf50;
  color: white;
  cursor: pointer;
}

select {
  margin-top: 10px;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  outline: none;
}
</style>
