<template lang="html">
  <v-app>
    <v-container fluid class="login-container">
      <v-flex xs12 md3 class="login-form">
        <v-alert color="error" icon="warning" value="true" class="login-form-alert" v-if="error">
          {{ error }}
        </v-alert>
        <v-text-field
          name="username"
          label="用户名"
          v-model="username"
          :error-messages="usernameError"
          @input="syncUsernameError"
        ></v-text-field>

        <v-text-field
          name="password"
          label="密码"
          v-model="password"
          :error-messages="passwordError"
          @input="syncPasswordError"
        ></v-text-field>

        <v-btn large class="submit-button" :loading="pending" color="primary" @click="handleSubmit">登录</v-btn>
      </v-flex>
    </v-container>
  </v-app>
</template>

<script>
import 'material-design-icons/iconfont/material-icons.css'
import axios from 'axios'

export default {
  name: 'LoginArea',
  data: function () {
    return {
      username: null,
      usernameError: [],
      password: null,
      passwordError: [],
      pending: false,
      error: null
    }
  },
  methods: {
    handleSubmit () {
      if (!this.handleFormVerification()) {
        return
      }
      this.pending = true
      this.error = null
      axios.post('/api/v1/auth/login/', {
        username: this.username,
        password: this.password
      }).then(json => {
        this.pending = false
        if (!json.data.token) {
          this.error = '未知的错误.'
        }
        localStorage.setItem('token', `JWT ${json.data.token}`)
        window.location.href = '/#/update-file-area'
      }).catch(error => {
        this.error = error.response.status < 500 ? '用户名密码错误' : '抱歉,服务器内部错误.'
        this.pending = false
      })
    },
    handleFormVerification () {
      let passed = true
      if (!this.username) {
        this.usernameError.push('请输入用户名！')
        passed = false
      }
      if (!this.password) {
        this.passwordError.push('请输入密码！')
        passed = false
      }

      return passed
    },
    syncUsernameError () {
      this.usernameError = []
    },
    syncPasswordError () {
      this.passwordError = []
    }
  }
}
</script>

<style lang="css">
  .login-container {
    width: 100%;
    min-height: 100%;
    background: #f0f2f5;
    background-image: url('/TVYTbAXWheQpRcWDaDMu.svg');
    background-repeat: no-repeat;
    background-position: center;
    background-size: 100%;
  }
  .login-form {
    position: relative;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }
  .login-title {
    text-align: center;
    margin-bottom: 2rem;
  }
  .login-form-alert {
    margin-bottom: 2rem;
  }
  .submit-button {
    margin: 2rem 0;
    width: 100%;
  }
</style>
