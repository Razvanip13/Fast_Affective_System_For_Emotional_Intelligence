<template>
  <div class="table-div">
    <v-data-table
        class="elevation-1 custom-table rounded-xl"
        :headers="headers"
        :items="charts"
    >
      <template v-slot:top>
        <v-toolbar
            class="rounded-xl"
            flat
        >
          <v-toolbar-title>Emotion charts</v-toolbar-title>
          <v-divider
              class="mx-4"
              inset
              vertical
          ></v-divider>
          <v-spacer></v-spacer>
        </v-toolbar>
      </template>
      <template v-slot:item.actions="{ item }">
        <v-icon
            small
            color="blue"
            @click="showChart(item)"
        >
          mdi-poll
        </v-icon>
        <v-icon
            small
            color="blue"
            @click="showPieChart(item)"
        >
          mdi-chart-arc
        </v-icon>
      </template>
    </v-data-table>
    <dialog-chart
        :dialog="dialog"
        :is-bar-chart="isBarChart"
        :chart-data="chartData"
        v-on:dialogClosed="close"
    >
    </dialog-chart>
  </div>

</template>


<script>
import DialogChart from "./DialogChart";

export default {
  name: "TableCharts",
  components: {DialogChart},
  props: {
    userId: Number
  },
  data: () => ({
    dialog: false,
    dialogDelete: false,
    headers: [
      {
        text: 'Name',
        align: 'start',
        sortable: false,
        value: 'test.name',
      },
      {
        text: 'Type',
        sortable: false,
        value: 'chartType.name',
      },
      {
        text: 'Date',
        sortable: false,
        value: 'date',
      },
      {text: 'Actions', value: 'actions', sortable: false},


    ],
    charts: [],
    chartData: null,
    emotionColors: {
      'angry': 'rgba(240, 33, 33, 0.8)',
      'disgust': 'rgba(240, 152, 33, 0.8)',
      'fear': 'rgba(216, 33, 240, 0.8)',
      'happy': 'rgba(240, 216, 33, 0.8)',
      'neutral': 'rgba(33, 240, 91, 0.8)',
      'sad': 'rgba(33, 48, 240, 0.8)',
      'surprise': 'rgba(240, 33, 152, 0.8)',
      'calm': 'rgba(18, 212, 226, 0.8)'
    },
    isBarChart: true,
    editedIndex: -1,
  }),
  computed: {
    formTitle() {
      return this.editedIndex === -1 ? 'New Item' : 'Edit Item'
    },
  },
  watch: {
    dialog(val) {
      val || this.close()
    },
    dialogDelete(val) {
      val || this.closeTrial()
    },
  },
  created() {
    this.initialize()
  },
  methods: {
    initialize() {
      this.$axios.get('http://localhost:8000/users/' + this.userId + '/charts')
          .then(response => {
            this.charts = response.data
          })
    },

    editItem(item) {
      this.editedIndex = this.charts.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialog = true
    },

    showChart(item) {
      this.$axios.get('http://localhost:8000/charts/' + item.id)
          .then(response => {
            this.isBarChart = true
            let chartData = {}
            let labels = []
            let data = []
            let backgroundColors = []
            chartData.labels = labels


            response.data.captures.forEach(element => {
              labels.push(element.emotion.name)
              backgroundColors.push(this.emotionColors[element.emotion.name])
              data.push(element.confidence)
            })

            let datasets = []
            datasets.push({
              label: ['Emotions'],
              data: data,
              backgroundColor: backgroundColors
            })

            chartData.datasets = datasets
            chartData.labels = labels

            this.chartData = chartData
            this.dialog = true
          })
    },
    showPieChart(item) {
      this.$axios.get('http://localhost:8000/charts/' + item.id)
          .then(response => {
            this.isBarChart = false
            let chartData = {}
            let labels = [
              'Angry',
              'Disgust',
              'Fear',
              'Happy',
              'Neutral',
              'Sad',
              'Surprise',
              'Calm'
            ]
            let data = []
            let backgroundColors = []

            let emotionCount = {
              'angry': 0,
              'disgust': 0,
              'fear': 0,
              'happy': 0,
              'neutral': 0,
              'sad': 0,
              'surprise': 0,
              'calm': 0
            }

            response.data.captures.forEach(element => {
              emotionCount[element.emotion.name] += 1
            })

            for (const emotion in emotionCount) {
              data.push(emotionCount[emotion])
            }

            for (const emotionColor in this.emotionColors) {
              backgroundColors.push(this.emotionColors[emotionColor])
            }

            let datasets = []
            datasets.push({
              data: data,
              backgroundColor: backgroundColors
            })
            chartData.datasets = datasets
            chartData.labels = labels
            this.chartData = chartData
            this.dialog = true
          })
    },
    close() {
      this.dialog = false
      this.$nextTick(() => {
        this.editedIndex = -1
      })
    },
  },
}
</script>


<style scoped>
.table-div{
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-image: linear-gradient(to top, #e6e9f0 0%, #eef1f5 100%);
}

.custom-table{
  width: 70vw;

}
</style>