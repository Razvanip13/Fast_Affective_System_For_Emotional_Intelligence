<template>
  <div>
    <table-charts
        :user-id="userId"
    >
    </table-charts>
  </div>
</template>

<script>
import TableCharts from "../components/TableCharts";
export default {
  name: "ChartListView",
  components: {TableCharts},
  data() {
    return {
      userId: parseInt(this.$route.params.id),
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