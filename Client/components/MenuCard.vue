<template>
  <div class="custom-card">
    <v-card
        class="mx-auto elevation-24 rounded-xl"
        max-width="28vw"
        @click = "emitRouting()"
    >
      <v-img
          :src = "imageUrl"
          height="38vh"
      ></v-img>
      <v-card-title>
        {{ title }}
      </v-card-title>
    </v-card>
  </div>
</template>
<script>
export default {
  name: "MenuCard",
  props: ['title','imageUrl'],
  data: () => ({}),
  methods:{
    emitRouting(){
      this.$emit('goToRoute')
    }
  }
}
</script>

<style scoped>
.custom-card {
  padding: 2vw;
  font-family: "Roboto", sans-serif;

}

</style>