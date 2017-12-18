<template lang="html">
  <Upload
    multiple
    type="drag"
    action="/api/v1/monitor/upload_file/"
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
