<template>
  <div>
    <video
        id="video"
        :width="image_width"
        :height="image_height"
        autoplay="true"
        style="display: none"
    >
    </video>
    <video
        id="shown_video"
        :width="400"
        :height="230"
        autoplay="true"
    >
    </video>
    <canvas
        id="canvas"
        style="display:none"
    >
    </canvas>
  </div>

</template>

<script>
import axios from "axios";

export default {
  name: "MyCamera",
  props: {
    testStart: Boolean,
    idUser: Number,
    idChart: Number
  },
  data() {
    return {
      image_width: 1920,
      image_height: 1080
    }
  },
  methods: {
    turn_on_camera: async function () {
      var video = document.querySelector("#video");
      var shown_video = document.querySelector("#shown_video");

      let constraints = {
        video: {
          width: {ideal: this.image_width},
          height: {ideal: this.image_height}
        }
      };

      try {
        const stream = await navigator.mediaDevices.getUserMedia(constraints)
        let stream_settings = stream.getVideoTracks()[0].getSettings();

        this.image_width = stream_settings.width;
        this.image_height = stream_settings.height;

        video.srcObject = stream;
        shown_video.srcObject = stream;
      } catch (e) {
        alert("CAMERA PERMISSION REJECTED")
      }
    },
    get_image: async function () {
      var canvas = document.getElementById('canvas');
      var video = document.getElementById('video');

      canvas.width = this.image_width;
      canvas.height = this.image_height;
      canvas.getContext('2d').drawImage(video, 0, 0, this.image_width, this.image_height);

      return canvas.toDataURL();
    },
    monitor_face: async function () {
      while (this.testStart) {
        const the_image = await this.get_image();
        axios.post(
            'http://localhost:8000/face_emotion',
            {
              "idChart": this.idChart,
              "idUser": this.idUser,
              "base64": the_image
            }
        )
        await new Promise(resolve => setTimeout(resolve, 5000));
      }
    }
  },
  mounted() {
    this.turn_on_camera()
  },
  watch: {
    'testStart': function () {
      if (this.testStart === true) {
        this.monitor_face()
      }
    }
  }
}
</script>

<style scoped>
#shown_video{
}
</style>