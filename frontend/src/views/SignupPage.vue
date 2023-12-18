<template>
  <div>
    <h2>Sign Up</h2>
    <form @submit.prevent="signup">
      <div>
        <label for="email">Email:</label>
        <input type="email" v-model="email" required />
      </div>
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
      <button type="submit">Sign Up</button>
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
      email: "", // Add email field
      username: "",
      password: "",
      role: "user", // Default role is "user"
      message: "",
    };
  },
  methods: {
  signup() {
    axios
      .post(`${API_BASE_URL}/signup`, {
        email: this.email,
        username: this.username,
        password: this.password,
        role: this.role,
      })
      .then((response) => {
        if (this.role === 'user') {
          this.message = `User ${this.username} signed up successfully. Please log in.`;
        } else if (this.role === 'admin') {
          this.message = `Admin ${this.username} signed up successfully. Please log in.`;
        }
        
        // Redirect to the login page
        this.$router.push('/login');
      })
      .catch((error) => {
        this.message = error.response.data;
      });
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
/* Add any necessary styling here */
</style>
