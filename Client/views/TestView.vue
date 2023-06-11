<template>
  <div class="mainBody">
    <div id="top_bar">
      <MyCamera
          :id-user="idUser"
          :id-chart="idChartFace"
          :test-start="testStart"
      >
      </MyCamera>
      <div id="top_buttons">
        <v-btn
            depressed
            color="primary"
            v-show="testStart===true"
            @click="openDialogStopTest"
        >
          Finish
        </v-btn>
      </div>
    </div>
    <div class="mic-check">
      <AudioButton

          :id-chart-voice="idChartVoice"
          :id-user="idUser"
          v-if="testStart===true && test.testType.name==='Oral'"
      >
      </AudioButton>
    </div>

    <QuestionScene
        class="question_scene"
        v-show="testStart===true"
        :test="test"
        :testEnd="testEnd"
        :id-user="idUser"
        :id-chart="idChartVoice"
        v-on:evaluateResults="evaluateResults($event)"
    >
    </QuestionScene>
    <div class="announcements">
      <div v-show="testStart===false && testEnd===false">
        If you want to start the test, press the button below.
        During the test, your face and voice will be analyzed to check your emotional states.
        Once you finished, press the finish button in the top right corner.
      </div>
      <div v-show="testEnd===true">
        You have finished the test.
        To check your results, go to the result section
        Press the button below to go back to the menu.
      </div>
    </div>
    <div id="bottom_buttons">
      <v-btn
          depressed
          color="primary"
          elevation="2"
          large
          rounded
          x-large
          v-show="testStart!==true && testEnd!==true"
          @click="openDialogStartTest"
      >
        Start
      </v-btn>
      <v-btn

          depressed
          color="primary"
          elevation="2"
          large
          rounded
          x-large
          v-show="testEnd===true"
          @click="goBackToMenu"
      >
        Menu
      </v-btn>
    </div>
    <v-dialog class="rounded-xl" v-model="dialogStartTest" max-width="500px">
      <v-card>
        <v-card-title class="text-h5">Do you want start?</v-card-title>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="closeDialogStartTest">No</v-btn>
          <v-btn color="blue darken-1" text @click="startTheTest">Yes</v-btn>
          <v-spacer></v-spacer>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog class="rounded-xl" v-model="dialogStopTest" max-width="500px">
      <v-card >
        <v-card-title class="text-h5">Do you want to finish?</v-card-title>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="closeDialogEndTest">No</v-btn>
          <v-btn color="blue darken-1" text @click="stopTheTest">Yes</v-btn>
          <v-spacer></v-spacer>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import MyCamera from "../components/MyCamera";
import AudioButton from "../components/audio/AudioButton";
import axios from "axios";
import QuestionScene from "../components/QuestionScene";

export default {
  name: "TestView",
  components: {QuestionScene, AudioButton, MyCamera},
  data() {
    return {
      testStart: false,
      idUser: parseInt(this.$route.params.idUser),
      idTest: parseInt(this.$route.params.idTest),
      idChartFace: 0,
      idChartVoice: 0,
      test: null,
      testEnd: false,
      dialogStartTest: false,
      dialogStopTest: false
    }
  },
  methods: {
    async startTheTest() {
      this.dialogStartTest = false
      await axios.post(
          'http://localhost:8000/users/' + this.idUser + '/tests/' + this.idTest + '/charts',
      )
          .then(response => {
            this.idChartFace = response.data.idChartFace
            this.idChartVoice = response.data.idChartVoice
          })

      this.testStart = true
    },
    stopTheTest() {
      this.dialogStopTest=false
      this.testStart = false
      this.testEnd = true
    },
    async getTestQuestions() {
      await axios.get(
          'http://localhost:8000/tests/' + this.idTest,
      )
          .then(response => {
            this.test = response.data
          })
    },
    async evaluateResults(answer_package) {
      answer_package.idUser = this.idUser

      await axios.post(
          'http://localhost:8000/results/',
          answer_package
      )
    },
    goBackToMenu(){
      this.$router.push(
          {
            name: "MenuView",
            params: {id:this.idUser}
          }
      )
    },
    openDialogStartTest(){
      this.dialogStartTest = true
    },
    closeDialogStartTest(){
      this.dialogStartTest = false
    },
    openDialogStopTest(){
      this.dialogStopTest = true
    },
    closeDialogEndTest(){
      this.dialogStopTest = false
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
    this.getTestQuestions()
  }
}
</script>

<style scoped>
.mainBody {
  width: 100%;
  background-image: linear-gradient(to top, #c4c5c7 0%, #dcdddf 52%, #ebebeb 100%);
  height: 100%;
}

#bottom_buttons {
  display: flex;
  justify-content: center;
  align-items: flex-end;
  height: 10em;
  width: 100%
}

#top_buttons {
  display: flex;
  justify-content: flex-end;
  width: 100%;
  padding-top: 15px;
  padding-right: 15px;

}

#top_bar {
  display: flex;
}

.question_scene {
  padding-top: 10px;
}

.announcements {
  font-family: "Roboto", sans-serif;
  font-size: 25px;
  display: flex;
  justify-content: center;
  text-align: center;
  width: 40em;
  margin-left: auto;
  margin-right: auto;
  padding-top: 3em;
}

.mic-check{
  display: flex;
  justify-content: center;

}


</style>