<template>
  <div class="container">
    <h2>Daily Reminder</h2>
    <button class="schedule-button" @click="scheduleReminder">Schedule Daily Reminder</button>
    <div v-if="message" class="message">{{ message }}</div>
    <button @click="goToUserDashboard">Back to User Dashboard</button>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      message: "",
    };
  },
  methods: {
    scheduleReminder() {
      const access_token = localStorage.getItem("access_token");
      if (!access_token) {
        this.message = "Please login to schedule the daily reminder";
        return;
      }

      axios
        .post("/schedule/daily-reminder", null, {
          headers: {
            Authorization: `Bearer ${access_token}`,
          },
        })
        .then((response) => {
          this.message = response.data.message;
        })
        .catch((error) => {
          this.message = error.response.data.message;
        });
    },
    goToUserDashboard() {
      this.$router.push('/user-dashboard');
    },
  },
};
</script>

<style>
/* DailyReminderPage.vue styles */
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

.schedule-button {
  background-color: #e91e63;
}
</style>
