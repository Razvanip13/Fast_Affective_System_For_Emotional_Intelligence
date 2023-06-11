<template>
  <div class="text-center">
    <v-dialog
        v-if="isBarChart"
        v-model="dialog"
        width="80vw"
        height="50vh"
        @click:outside="closeDialog"
    >
      <v-card>
        <EmotionBarChart
            v-if="isBarChart"
            :chart-data="chartData"
        ></EmotionBarChart>
        <v-divider></v-divider>
      </v-card>
    </v-dialog>
    <v-dialog
        v-if="!isBarChart"
        v-model="dialog"
        width="40vw"
        height="50vh"
        @click:outside="closeDialog"
    >
      <v-card>
        <EmotionPieChart
            :chart-data="chartData"
        >
        </EmotionPieChart>
        <v-divider></v-divider>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>

import EmotionBarChart from "./EmotionBarChart";
import EmotionPieChart from "./EmotionPieChart";
export default {
  name: "DialogChart",
  components: {EmotionPieChart,EmotionBarChart},
  props: {
    dialog: Boolean,
    chartData: Object,
    isBarChart: Boolean

  },
  methods: {
    closeDialog() {
      this.$emit('dialogClosed')
    }
  }
}
</script>

<style scoped>

</style>