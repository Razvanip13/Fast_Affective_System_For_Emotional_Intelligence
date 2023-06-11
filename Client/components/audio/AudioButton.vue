<template>
  <div id="app">
    <main class="container has-text-centered">
      <section id="example-audio">
        <div class="columns">
          <div class="column">
            <div class="record-settings">
              <SecondAudioRecorder :mode="recordMode.audio" @stream="onStream" @result="onResult"/>
              <div class="field">
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import SecondAudioRecorder from "./SecondAudioRecorder";
import axios from "axios";

export default {
  name: 'AudioButton',
  components: {SecondAudioRecorder},
  props:{
    idUser: Number,
    idChartVoice: Number
  },
  data() {
    return {
      recordMode: {
        audio: 'hold',
        video: 'press'
      },
      recordings: []
    }
  },
  methods: {
    removeRecord(index) {
      this.recordings.splice(index, 1)
    },
    onStream(stream) {
      console.log('Got a stream object:', stream);
    },
    onVideoStream(stream) {
      console.log('Got a video stream object:', stream);
    },
    onVideoResult(data) {
      this.$refs.Video.srcObject = null
      this.$refs.Video.src = window.URL.createObjectURL(data)
    },
    onResult(data) {
      const the_user = this.idUser
      const the_chart = this.idChartVoice
      this.recordings.push({
        src: window.URL.createObjectURL(data)
      })

      var reader = new FileReader();

      reader.readAsDataURL(data);
      var base64data = null
      reader.onloadend = function () {
        base64data = reader.result;
        axios.post(
            'http://localhost:8000/voice_emotion',
            {
              "idUser": the_user,
              "idChart": the_chart,
              "base64": base64data.split(",")[1]
            }
        )
      }
    }
  },
  watch:{
    'idChartVoice': function () {
    }
  }
}
</script>

<style lang="scss">

.vue-audio-recorder, .vue-video-recorder {
  //margin-right: 16px;
}


.footer {
  background-color: #eee;
}
</style>