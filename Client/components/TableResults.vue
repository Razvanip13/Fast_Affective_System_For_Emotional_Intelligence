<template>
  <div class="table-div">
    <v-data-table
        class="elevation-1 rounded-xl custom-table"
        :headers="headers"
        :items="results"
    >
      <template v-slot:top>
        <v-toolbar
            class="rounded-xl"
            flat
        >
          <v-toolbar-title>Results</v-toolbar-title>
          <v-divider
              class="mx-4"
              inset
              vertical
          ></v-divider>
          <v-spacer></v-spacer>
        </v-toolbar>
      </template>
    </v-data-table>
  </div>
</template>

<script>
export default {
  name: "TableResults",
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
        text: 'Score (out of 100)',
        sortable: false,
        value: 'score',
      },
      {
        text: 'Date',
        sortable: false,
        value: 'date',
      }
    ],
    results: [],
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
      this.$axios.get('http://localhost:8000/users/' + this.userId + '/results')
          .then(response => {
            this.results = response.data
          })
    },
    editItem(item) {
      this.editedIndex = this.results.indexOf(item)
      this.dialog = true
    },

    commenceTrial(item) {
      this.editedIndex = this.results.indexOf(item)
      this.dialogDelete = true
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
.table-div {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-image: linear-gradient(to top, #e6e9f0 0%, #eef1f5 100%);
}

.custom-table {
  width: 70vw;
}
</style>