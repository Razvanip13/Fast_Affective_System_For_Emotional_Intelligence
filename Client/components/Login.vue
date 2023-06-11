<template>
  <div id="flex_div" class="elevation-24 rounded-xl">
    <form id="login-form">
      <v-text-field
          v-model="username"
          class ="text_field_login"
          label="Username"
      ></v-text-field>
      <v-text-field
          v-model="password"
          class ="text_field_login"
          :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
          :type="show1 ? 'text' : 'password'"
          name="input-10-1"
          label="Password"
          @click:append="show1 = !show1"
      ></v-text-field>
      <v-btn
          class="mr-4"
          @click="submitLogin"
      >
        Login
      </v-btn>
      <v-btn @click="clear">
        clear
      </v-btn>
    </form>
  </div>
</template>

<script>
import { validationMixin } from 'vuelidate'
import { required, maxLength, password } from 'vuelidate/lib/validators'

export default {
  mixins: [validationMixin],
  validations: {
    username: { required, maxLength: maxLength(20) },
    password: { required, password },
    select: { required },
    checkbox: {
      checked (val) {
        return val
      },
    },
  },
  data: () => ({
    username: '',
    password: '',
    show1:false
  }),
  computed: {

  },
  methods: {
    submitLogin () {
      this.$emit('checkLogin',{username:this.username,password:this.password})
    },
    clear () {
      this.$v.$reset()
      this.username = ''
      this.password = ''

    },
  },
}
</script>

<style scoped>
  #login-form{
    text-align: center;
    width:50%;
  }
  #flex_div{
    width: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    padding:20px;
    padding-bottom:60px;
    background: rgba(246, 243, 237, 0.6)
  }
</style>