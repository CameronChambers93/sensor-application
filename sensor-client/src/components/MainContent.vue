<template>
  <div class="hello">
    {{html}}
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'MainContent',
  props: {
    msg: String
  },
  created() {
    this.getReadings();
  },
  data () {
    return {
      endpoint: 'http://192.168.1.25:5000/get_readings?sensor_id=1&from_date=2020-06-09&to_date=2020-06-16',
      html: ""
    }
  },
  methods: {
    getReadings() {
      axios.get(this.endpoint, { headers: { 'Access-Control-Allow-Origin': true }})
        .then(response => {
          this.html = response.data;
        })
        .catch(error => {
          console.log('-----error-------');
          console.log(error);
        })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
