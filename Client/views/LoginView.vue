<template>
  <div id="view_div">
    <Login
        v-on:checkLogin="checkLogin($event)"
    >
    </Login>
    <v-snackbar
        v-model="snackbar"
        :timeout="timeout"
        elevation="60"
    >
      Username or password are incorrect
    </v-snackbar>
  </div>

</template>

<script>

import Login from "../components/Login";

export default {
  name: "LoginPage",
  components: {Login},
  data: () => ({
    snackbar: false,
    timeout: 2000
  }),
  methods: {
    checkLogin(loginCredentials) {
      this.$axios.get('http://localhost:8000/users/login', {
        params: {username: loginCredentials.username, password: loginCredentials.password}
      })
          .then(response => {
            if (response.status === 200) {
              localStorage.approval = response.data.key
              this.$router.push(
                  {
                    name: "MenuView",
                    params: {id: response.data.id}
                  }
              )
            }
          })
          .catch(error => {
            if (error.response.status === 404) {
              this.snackbar = true
            }
          })
    }
  },
  mounted() {
    localStorage.approval = ""
  }

}
</script>

<style scoped>
#view_div {
  background-image: url('https://images.pexels.com/photos/245032/pexels-photo-245032.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260');
  -webkit-background-size: cover;
  -moz-background-size: cover;
  -o-background-size: cover;
  background-size: cover;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>