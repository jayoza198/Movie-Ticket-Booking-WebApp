<template>
  <div class="user-dashboard">
    <h2>User Dashboard</h2>
    <div class="nav-buttons">
      <router-link to="/theatres/search/user" class="nav-link-button">Theatre Search</router-link>
      <router-link to="/shows/search/user" class="nav-link-button">Show Search</router-link>
      <router-link to="/user-booking" class="nav-link-button">Book Tickets</router-link>
      <router-link to="/view-user-bookings" class="nav-link-button">View Bookings</router-link>
      <router-link to="/schedule/daily-reminder" class="nav-link-button">Daily Reminder</router-link>
      
    </div>
    <button @click="logout" class="logout-button">Logout</button>
    <!-- Other user-specific content -->
  </div>
</template>
<script>
export default {
  name: "UserDashboard",
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
.user-dashboard {
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
