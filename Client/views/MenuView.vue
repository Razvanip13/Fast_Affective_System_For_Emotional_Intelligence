<template>
  <div id="root-div">
    <div>
      <div id="logout">
        <v-btn  @click="goToLogin">
          Logout
        </v-btn>
      </div>
    </div>
    <div id="top-side">
      <div id="title">
        Welcome {{ this.firstName }} {{ this.lastName }}
      </div>
    </div>
    <div id="menu-div">
      <MenuCard
          title="Tests"
          imageUrl="https://images.pexels.com/photos/927022/pexels-photo-927022.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260"
          v-on:goToRoute="goToTestView()"
      >
      </MenuCard>
      <MenuCard
          title="Results"
          imageUrl="https://images.pexels.com/photos/6684373/pexels-photo-6684373.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260"
          v-on:goToRoute="goToResultsView()"
      >
      </MenuCard>
      <MenuCard
          title="Charts"
          imageUrl="https://images.pexels.com/photos/3183153/pexels-photo-3183153.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260"
          v-on:goToRoute="goToChartView()"
      >
      </MenuCard>
    </div>
  </div>
</template>

<script>
import MenuCard from "../components/MenuCard";
import axios from "axios";

export default {
  name: "MenuView",
  components: {MenuCard},
  data() {
    return {
      userId: this.$route.params.id,
      firstName: "",
      lastName: ""
    }
  },
  methods: {
    getUserName() {
      axios.get('http://localhost:8000/users/' + this.userId, {
        params: {id: this.userId}
      })
          .then(response => {
            if (response.status === 200) {
              this.lastName = response.data.lastName
              this.firstName = response.data.firstName
            }
          })
          .catch(error => {

            if (error.response.status === 404) {
              console.log('error')
            }
          })
    },
    goToTestView() {
      this.$router.push(
          {
            name: "TestsListView",
            params: {id: this.userId}
          }
      )
    },
    goToResultsView() {
      this.$router.push(
          {
            name: "ResultsListView",
            params: {id: this.userId}
          }
      )
    },
    goToChartView(){
      this.$router.push(
          {
            name: "ChartListView",
            params: {id: this.userId}
          }
      )
    },
    goToLogin(){
      this.$router.push(
          {
            name: "LoginView",
          }
      )
    }

  },
  mounted() {
    if(localStorage.approval!=="YGiLCuTay0SoYQIxh4APS18o/4YlH39wJyKyRtIIO7o="){
      this.$router.push(
          {
            name:"LoginView"
          }
      )
    }
    this.getUserName()
  }
}
</script>

<style scoped>
#root-div {
  height: 100vh;
  background-image: linear-gradient(to top, #e6e9f0 0%, #eef1f5 100%);
}

#menu-div {
  display: flex;
  height: 86vh;
  justify-content: center;
  align-items: center;
  -webkit-background-size: cover;
  -moz-background-size: cover;
  -o-background-size: cover;
  background-size: cover;
}

#top-side{
  display: flex;
  justify-content: center;
  font-family: "Roboto", sans-serif;
  width:100%
}

#title{
  padding-left: 2vh;
  padding-top: 2vh;
  font-family: "Roboto", sans-serif;
  font-size: 20pt;
}

#logout{
  padding-left: 2vh;
  padding-top: 2vh;
  padding-right: 8vh;
  display: flex;
  justify-content: flex-end;
}

</style>