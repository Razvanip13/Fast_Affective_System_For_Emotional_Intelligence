<template>
  <div>
    <TableTests v-on:testTrial="openTest($event)"></TableTests>
  </div>
</template>

<script>
import TableTests from "../components/TableTests";

export default {
  name: "TestsListView",
  components: {TableTests},
  data() {
    return {
      userId: this.$route.params.id,
    }
  },
  methods: {
    openTest(test) {

      this.$router.push(
          {
            name: "TestView",
            params: {
              idUser: this.userId,
              idTest: test.id
            }
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
  }
}
</script>

<style scoped>

</style>