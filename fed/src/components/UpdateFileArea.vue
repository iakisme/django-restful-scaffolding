<template lang="html">
  <Upload
    type="drag"
    action="/api/v1/monitor/upload_file/"
    :headers="headers"
    name="template">
    <div style="padding: 20px 0">
      <Icon type="ios-cloud-upload" size="52" style="color: #3399ff"></Icon>
      <p>Click or drag files here to upload</p>
    </div>
  </Upload>
</template>

<script>
import axios from 'axios'
import 'iview/dist/styles/iview.css'

export default {
  name: 'UpdateFileArea',
  data: function () {
    return {
      headers: {
        Authorization: localStorage.getItem('token')
      }
    }
  },
  mounted: function () {
    this.$nextTick(() => {
      axios.get('/api/v1/monitor/dream/', {
        headers: {
          Authorization: localStorage.getItem('token')
        }
      }).then(json => {
        console.log(json)
      }).catch(error => {
        console.error(error)
      })
    })
  }
}
</script>

<style lang="css">
</style>
