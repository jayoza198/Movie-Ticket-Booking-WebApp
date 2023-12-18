<!-- <template>
    <div class="home">
      <h2>Welcome to Ticket Booking App</h2>
      <div>
        <button v-for="user in users" :key="user.type" @click="redirectTo(user.path)">
          {{ user.description }}
        </button>
      </div>
    </div>
  </template> -->
<template>
<div class="home">
  <h2>Welcome to Ticket Booking App</h2>

  <div>
    

    <button @click="redirectTo('/signup')">
      User Signup  
    </button>
    
    <button @click="redirectTo('/signup')">
      Admin Signup
    </button>

    <button @click="redirectTo('/login')">
      Login
    </button>

    
  </div>

</div>
</template>

<script>
  import axios from "axios";
  const API_BASE_URL = 'http://localhost:5000';
  export default {
    data() {
      return {
        users: [],
      };
    },
    created() {
      // this.fetchUserData();
    },
    methods: {
      fetchUserData() {
        axios.get(`${API_BASE_URL}/`).then((response) => {
          this.users = response.data.users;
        });
      },
      redirectTo(path) {
        this.$router.push(path);
      },
    },
  };
  </script>

<style>
.home {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start; /* Changed from "center" to "flex-start" */
  height: 100vh;
}

button {
  margin: 10px;
  padding: 10px 20px;
  font-size: 16px;
  border: none;
  border-radius: 4px;
  background-color: #2196f3;
  color: white;
  cursor: pointer;
}
</style>