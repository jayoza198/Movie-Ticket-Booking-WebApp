<template>
  <div class="admin-dashboard">
    <h2>Admin Dashboard</h2>
    <div class="nav-buttons">
      <router-link to="/shows" class="nav-link-button">Show Management</router-link>
      <router-link to="/theatres" class="nav-link-button">Theatre Management</router-link>
      <router-link to="/shows/search" class="nav-link-button">Search Shows</router-link>
      <router-link to="/theatres/search" class="nav-link-button">Search Theatres</router-link>
      <router-link to="/admin-booking" class="nav-link-button">Admin View Booking</router-link>
      <router-link to="/schedule/monthly-report" class="nav-link-button">Monthly Report Page</router-link>
      <router-link to="/theatre-export" class="nav-link-button">Theatre Export</router-link>
    </div>
    <button @click="logout" class="logout-button">Logout</button>
    <!-- Other admin-specific content -->
  </div>
</template>

<script>
export default {
  name: "AdminDashboard",
  methods: {
    logout() {
      // Call your logout API endpoint or perform necessary logout actions
      // Example: Clear local storage or perform other actions
      // Then redirect to the login page
      localStorage.removeItem('access_token');
      this.$router.push('/');
    },
  },
};
</script>


<style>
/* Add CSS styles for buttons and divs here */
.admin-dashboard {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  height: 100vh;
  padding-top: 20px; /* Add padding to create space from the top */
}

.nav-buttons {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px; /* Add margin to separate from the title */
}

.nav-link-button {
  display: block;
  padding: 10px;
  width: 200px; /* Set a definite width for the buttons */
  background-color: #4caf50;
  color: white;
  text-align: center;
  text-decoration: none;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-bottom: 5px; /* Add space between buttons */
}

.nav-link-button:hover {
  background-color: #45a049;
}

.logout-button {
  display: block;
  margin-top: 20px;
  padding: 10px;
  width: 200px; /* Set a definite width for the button */
  background-color: #f44336;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.logout-button:hover {
  background-color: #d32f2f;
}
</style>


