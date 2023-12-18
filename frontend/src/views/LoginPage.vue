<template>
  <div>
    <h2>Login</h2>
    <form @submit.prevent="login">
      <div>
        <label for="username">Username:</label>
        <input type="text" v-model="username" required />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" v-model="password" required />
      </div>
      <div>
        <label for="role">Role:</label>
        <select v-model="role">
          <option value="user">User</option>
          <option value="admin">Admin</option>
        </select>
      </div>
      <button type="submit">Login</button>
    </form>
    <div v-if="message">{{ message }}</div>
  </div>
</template>

<script>
import axios from "axios";
const API_BASE_URL = 'http://localhost:5000';
export default {
  data() {
    return {
      username: "",
      password: "",
      role: "user", // Default role is "user"
      message: "",
    };
  },
  methods: {
  login() {
    axios
      .post(`${API_BASE_URL}/login`, {
        username: this.username,
        password: this.password,
        role: this.role,
      })
      .then((response) => {
        // Save the access token in local storage or session storage
        // For simplicity, we are not including the complete token management here
        // You should use a secure approach to handle tokens in your application
        localStorage.setItem("access_token", response.data.access_token);
        localStorage.setItem("current_user", response.data.role);
        this.message = "Login successful";
        if (this.role === "user") {
          this.$router.push("/user-dashboard");
        } else if (this.role === "admin") {
          this.$router.push("/admin-dashboard");
        }
      })
      .catch((error) => {
        console.log("Login error:", error.response);
        this.message = "Login failed";
      });
  },
},
};
</script>


<style>
/* Common styles for all components */

/* Global styles */
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
