<template>
  <Bar
      :chart-options="chartOptions"
      :chart-data="chartData"
      :chart-id="chartId"
      :dataset-id-key="datasetIdKey"
      :plugins="plugins"
      :css-classes="cssClasses"
      :styles="styles"
      :width="width"
      :height="height"
  />
</template>

<script>
import {Bar} from 'vue-chartjs/legacy'
import {Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const emotionColors = {
      'angry': 'rgba(240, 33, 33, 0.8)',
      'disgust': 'rgba(240, 152, 33, 0.8)',
      'fear': 'rgba(216, 33, 240, 0.8)',
      'happy': 'rgba(240, 216, 33, 0.8)',
      'neutral': 'rgba(33, 240, 91, 0.8)',
      'sad': 'rgba(33, 48, 240, 0.8)',
      'surprise': 'rgba(240, 33, 152, 0.8)',
      'calm': 'rgba(18, 212, 226, 0.8)'
}

const emotionNames = ['angry','disgust','fear','happy','neutral','sad','surprise']

export default {
  name: 'EmotionBarChart',
  components: {Bar},
  props: {
    chartId: {
      type: String,
      default: 'bar-chart'
    },
    datasetIdKey: {
      type: String,
      default: 'label'
    },
    width: {
      type: Number,
      default: 400
    },
    height: {
      type: Number,
      default: 200
    },
    cssClasses: {
      default: '',
      type: String
    },
    styles: {
      type: Object,
      default: () => {
      }
    },
    plugins: {
      type: Object,
      default: () => {
      }
    },
    chartData:{
      type: Object,
      default: () => {

      }
    }
  },
  data() {
    return {
      chartOptions: {
        responsive: true,
        plugins:{
          legend: {
            display: true,
            labels: {
              generateLabels() {
                return emotionNames.map(label=> ({
                  text: label,
                  fillStyle: emotionColors[label]
                }))
              }
            }
          },
        }
      }
    }
  },

}
</script>