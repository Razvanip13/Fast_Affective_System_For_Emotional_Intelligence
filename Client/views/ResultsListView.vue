<template>
  <div>
    <TableResults
        :user-id="userId"
    >
    </TableResults>
  </div>
</template>

<script>
import TableResults from "../components/TableResults";
export default {
  name: "ResultsView",
  components: {TableResults},
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