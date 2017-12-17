<template lang="html">
  <div class="">
    <h1>a</h1>
    <input type="file" name="" value="">
  </div>
</template>

<script>
import axios from 'axios'

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
