<template>
  <div>
    <div class="questions" v-if="test!==null">
      <div id="question_display">{{ currentQuestion.description }}</div>
      <div
          v-for="(choice,index) in currentQuestion.choices"
          :key="choice.id"
      >
        <div class="answers_div">
          <v-btn
              v-if="answers[testIndex]===index"
              class="answer_button"
              color="primary"
              block
              elevation="2"
              rounded
              @click="markTheAnswer(index)"
          >
            {{ choice.answer }}
          </v-btn>
          <v-btn
              class="answer_button"
              v-if="answers[testIndex]!==index"
              @click="markTheAnswer(index)"
              block
              elevation="2"
              rounded
          >
            {{ choice.answer }}
          </v-btn>
        </div>
      </div>
      <div class="navigation_buttons">
        <div class="navigation_padder">
          <v-btn
              :disabled="leftDisabled"
              @click="moveBackwards"
          >
            Back
          </v-btn>
        </div>
        <div class="navigation_padder">
          <v-btn
              :disabled="rightDisabled"
              @click="moveForward"
          >
            Next
          </v-btn>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: "QuestionScene",
  components: {},
  props: {
    test: Object,
    testEnd: Boolean,
    idUser: Number,
    idChart: Number
  },
  data: () => ({
    testIndex: 0,
    total: 0,
    leftDisabled : true,
    rightDisabled: false,
    questions: [],
    currentQuestion: null,
    answers: []
  }),
  methods: {
    markTheAnswer(choiceNumber) {
      this.answers[this.testIndex] = choiceNumber
      this.$forceUpdate();
    },
    moveBackwards() {


      if (this.testIndex > 0) {
        this.testIndex--

        if(this.testIndex === 0){
          this.leftDisabled = true
        }

        this.currentQuestion = this.questions[this.testIndex]
        this.rightDisabled = false
      }

    },
    moveForward() {
      if (this.testIndex < this.total - 1) {
        this.testIndex++

        if(this.testIndex === this.total -1){
          this.rightDisabled = true
        }

        this.currentQuestion = this.questions[this.testIndex]
        this.leftDisabled = false
      }
    }
  },
  watch: {
    'test': function () {
      if (this.test != null) {
        this.total = this.test.questions.length
        this.questions = this.test.questions
        this.currentQuestion = this.questions[0]
        this.testIndex = 0
        this.answers = new Array(this.total).fill(null)
      }
    },
    'testEnd': function () {
      if (this.test.testType.name !== 'Oral') {
        let options = []
        for (let i = 0; i < this.answers.length; i++) {
          if (this.answers[i] !== null) {
            options.push({
              'questionId': this.questions[i].id,
              'answerId': this.questions[i].choices[this.answers[i]].id
            })
          } else {
            options.push({
              'questionId': this.questions[i].id,
              'answerId': null
            })
          }
        }
        let post_package = {
          'idTest': this.test.id,
          'answers': options
        }
        this.$emit('evaluateResults', post_package)
      }
    }
  }

}
</script>

<style scoped>
.questions {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.navigation_buttons {
  display: flex;
  justify-content: center;
  align-items: center;

}

#question_display {
  font-family: "Roboto", sans-serif;
  font-size: 20px;
  padding-bottom: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.answer_button {
  max-width: 600px;


}

.answers_div {
  padding-bottom: 20px;
}

.navigation_padder {
  padding-top: 10px;
  padding-right: 20px;
  padding-left: 20px;
}
</style>