<template>
  <div class="table-div">
    <v-data-table
        class="elevation-1 custom-table rounded-xl"
        :headers="headers"
        :items="tests"
    >
      <template v-slot:top>
        <v-toolbar
            class="rounded-xl"
            flat
        >
          <v-toolbar-title>Tests</v-toolbar-title>
          <v-divider
              class="mx-4"
              inset
              vertical
          ></v-divider>
          <v-spacer></v-spacer>

          <v-dialog v-model="dialogDelete" class="rounded-xl"  max-width="500px">
            <v-card >
              <v-card-title class="text-h5">Do you want to try the test?</v-card-title>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="closeTrial">No</v-btn>
                <v-btn color="blue darken-1" text @click="commenceTrialConfirmation">Yes</v-btn>
                <v-spacer></v-spacer>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-toolbar>
      </template>
      <template v-slot:item.actions="{ item }">
        <v-icon
            small
            color="black"
            @click="commenceTrial(item)"
        >
          mdi-play
        </v-icon>
      </template>
      <template v-slot:no-data>
        <v-btn
            color="primary"
            @click="initialize"
        >
          Reset
        </v-btn>
      </template>
    </v-data-table>
  </div>
</template>


<script>
export default {
  name: "TableTests",
  data: () => ({
    dialog: false,
    dialogDelete: false,
    headers: [
      {
        text: 'Title',
        align: 'start',
        sortable: false,
        value: 'name',
      },
      {
        text: 'Topic',
        sortable: false,
        value: 'topic.name',
      },
      {
        text: 'Type',
        sortable: false,
        value: 'testType.name',
      },

      {text: 'Actions', value: 'actions', sortable: false},
    ],
    tests: [],
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
      this.$axios.get('http://localhost:8000/tests')
          .then(response => {
            this.tests = response.data
          })
    },
    commenceTrial(item) {
      this.editedIndex = this.tests.indexOf(item)
      this.dialogDelete = true
    },
    commenceTrialConfirmation() {

      this.$emit('testTrial', this.tests[this.editedIndex])
      this.closeTrial()
    },

    close() {
      this.dialog = false
    },
    closeTrial() {
      this.dialogDelete = false
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