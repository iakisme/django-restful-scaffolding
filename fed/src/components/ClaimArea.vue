<template lang="html">
  <v-app>
    <v-toolbar class="primary">
      <v-btn icon>
        <v-icon color="white">arrow_back</v-icon>
      </v-btn>
      <v-toolbar-title class="white--text" slot="extension">认领心愿</v-toolbar-title>
    </v-toolbar>

    <v-container fluid>
      <v-text-field
        name="name"
        label="姓名"
        v-model="name"
        @input="syncNameError"
        :error-messages="nameError"
      ></v-text-field>

      <v-text-field
        name="phone"
        label="手机号"
        v-model="phone"
        @input="syncPhoneError"
        @change="verifiyPhone"
        :error-messages="phoneError"
      ></v-text-field>

      <v-layout>
        <v-text-field
          name="verificationCode"
          label="短信验证码"
          v-model="verificationCode"
          @input="syncVerificationCodeError"
          :error-messages="verificationCodeError"
        ></v-text-field>
        <v-btn flat outline :loading="sendPending" :disabled="sendDisabled" color="primary" @click="handleSendVerificationCode">{{ sendButtonText }}</v-btn>
      </v-layout>

      <v-btn large class="submit-button" :loading="submitPending" color="primary" @click="handleSubmit">确认认领</v-btn>
    </v-container>
  </v-app>
</template>

<script>
import 'material-design-icons/iconfont/material-icons.css'
import axios from 'axios'

export default {
  name: 'ClaimArea',
  data: function () {
    return {
      name: null,
      phone: null,
      verificationCode: null,
      nameError: [],
      phoneError: [],
      verificationCodeError: [],
      // send verification code
      sendPending: false,
      sendStatus: null,
      sendDisabled: false,
      sendButtonText: '发送验证码',
      // submit form
      submitPending: false,
      submitStatus: null
    }
  },
  methods: {
    handleSubmit () {
      if (!this.handleFormVerification()) {
        return
      }
      this.submitPending = true
      setTimeout(() => {
        this.submitPending = false
      }, 1000)
    },
    handleSendVerificationCode () {
      if (!this.phone) {
        this.phoneError.push('请输入手机号！')
        return
      }

      this.sendPending = true
      axios.post('/api/v1/monitor/send_code/', {
        phone_num: this.phone
      }).then(json => {
        if (json.status === 200) {
          this.sendPending = false
          this.sendDisabled = true
          this.handleSyncSendButtonText(60)
        }
      }).catch(error => {
        this.phoneError.push('抱歉，发生了未知的错误，请尝试重新发送验证码.')
        throw new TypeError(error)
      })
    },
    syncPhoneError () {
      this.phoneError = []
    },
    verifiyPhone (e) {
      if (!/^1[0-9]{10}$/.test(e)) {
        this.phoneError.push('请输入正确的手机号!')
      }
    },
    syncNameError () {
      this.nameError = []
    },
    syncVerificationCodeError () {
      this.verificationCodeError = []
    },
    handleFormVerification () {
      let passed = true
      if (!this.phone) {
        this.phoneError.push('请输入手机号！')
        passed = false
      }
      if (!this.name) {
        this.nameError.push('请输入姓名！')
        passed = false
      }
      if (!this.verificationCode) {
        this.verificationCodeError.push('请输入短信验证码！')
        passed = false
      }

      return passed
    },
    handleSyncSendButtonText (interval) {
      let copy = interval
      const timer = setInterval(() => {
        copy -= 1
        this.sendButtonText = `${copy}s 后重新获取`
        if (copy < 0) {
          clearInterval(timer)
          this.sendButtonText = `发送验证码`
          this.sendDisabled = false
        }
      }, 1000)
    }
  }
}
</script>

<style lang="css">
  .submit-button {
    margin: 2rem 0;
    width: 100%;
  }
</style>
