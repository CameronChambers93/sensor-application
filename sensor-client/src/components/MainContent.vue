<template>
  <div class="hello">

    <current-readings></current-readings>


    <md-card>
      <md-card-header>
        <h2>Timelapse</h2>
        <p style="margin-bottom:0px;">
          {{tDelta[tDeltaSelection]['amount']}} {{tDelta[tDeltaSelection]['type']}}(s)
        </p>
      </md-card-header>
      <md-card-content>
        <div class="date_selection_outer md-layout md-gutter md-alignment-center">
          
          <md-button @click="fastRewind()"><md-icon>fast_rewind</md-icon></md-button>
          <md-button @click="rewind()"><md-icon>arrow_left</md-icon></md-button>
          <md-button @click="zoomOut()" :disabled="tDeltaSelection == 0"><md-icon>zoom_out</md-icon></md-button>
          <md-button @click="zoomIn()" :disabled="tDeltaSelection == tDelta.length - 1"><md-icon>zoom_in</md-icon></md-button>
          <md-button @click="forward()"><md-icon>arrow_right</md-icon></md-button>
          <md-button @click="fastForward()"><md-icon>fast_forward</md-icon></md-button>
        </div>
        <div class="graph_container">
          <temperature-chart class="graph" :temperatureDataCollection="temperatureDataCollection" :loaded="loaded"></temperature-chart>
          <humidity-chart class="graph" :humidityDataCollection="humidityDataCollection" :loaded="loaded"></humidity-chart>
        </div>
      </md-card-content>
    </md-card>
  </div>
</template>

<script>
import TemperatureChart from './TemperatureChart.vue'
import HumidityChart from './HumidityChart.vue'
import CurrentReadings from './CurrentReadings.vue'

import axios from 'axios'
export default {
  name: 'MainContent',
  components: {
    TemperatureChart, HumidityChart, CurrentReadings
  },
  props: {
    msg: String,
    originalSettings: {   // Stores all devices' info
        type: Array,
        default: () => {
            return []
        }
    }
  },
  created() {
    this.toDate = new Date()
    this.fromDate = new Date()
    this.fromDate.setHours(this.fromDate.getHours() - 6)
    for (const [key, value] of Object.entries(this.originalSettings)) {
      this.rooms[value['device_name']] = {}
      this.sensorLookup[value['device_name']] = {}
      for (const sensor of Object.values(value.sensors)) {
          this.sensorLookup[value['device_name']][sensor.sensor_id] = sensor.sensor_name
          this.rooms[value.device_name][sensor.sensor_name] = {'temperature': {}, 'humidity': {}}
        }
      key == 5
    }
    this.getReadings()
  },
  computed: {
    ctDelta: function() {
      return this.tDelta[this.tDeltaSelection]
    }
  },
  data () {
    return {
      apiUrl: "http://192.168.1.25:5000/get_readings?",
      temperatureDataCollection: null,
      humidityDataCollection: null,
      loaded: false,
      fromDate: "2020-06-01 0:0:0",
      toDate: "2020-06-01 0:0:0",
      tDelta: [{'type': 'day', 'amount': 7, 'small': 3}, {'type': 'day', 'amount': 3, 'small': 1}, {'type': 'hour', 'amount': 24, 'small': 12}, {'type': 'hour', 'amount': 12, 'small': 6}, {'type': 'hour', 'amount': 6, 'small': 3}, {'type': 'hour', 'amount': 2, 'small': 1}, {'type': 'hour', 'amount': 1, 'small': 1}],
      tDeltaSelection: 4,
      rooms: {},
      sensorLookup: {}
    }
  },
  mounted() {
  },
  watch: {
    tDeltaSelection: function(newVal) {
      newVal == false
    }
  },
  methods: {
    rewind() {
      let t1 = new Date(this.fromDate)
      let t2 = new Date(this.toDate)
      if (this.ctDelta['type'] == 'day'){  // Does time interval span hours or days?
        t2.setDate(t2.getDate() - this.ctDelta['small'])
        t1.setDate(t1.getDate() - this.ctDelta['small'])
      }
      else {
        t2.setHours(t2.getHours() - this.ctDelta['small'])
        t1.setHours(t1.getHours() - this.ctDelta['small'])
      }
      this.fromDate = t1
      this.toDate = t2
      this.getReadings()
    },
    fastRewind() {
      let t1 = new Date(this.fromDate)
      let t2 = new Date(this.toDate)
      if (this.ctDelta['type'] == 'day'){  // Does time interval span hours or days?
        t2.setDate(t2.getDate() - this.ctDelta['amount'])
        t1.setDate(t1.getDate() - this.ctDelta['amount'])
      }
      else {
        t2.setHours(t2.getHours() - this.ctDelta['amount'])
        t1.setHours(t1.getHours() - this.ctDelta['amount'])
      }
      this.fromDate = t1
      this.toDate = t2
      this.getReadings()
    },
    fastForward() {
      let t1 = new Date(this.fromDate)
      let t2 = new Date(this.toDate)
      let t3 = new Date()
      if (this.ctDelta['type'] == 'day'){  // Does time interval span hours or days?
        t2.setDate(t2.getDate() + this.ctDelta['amount'])
        if (t2 > t3) {
          t1.setDate(t3.getDate() - this.ctDelta['amount'])
          t2 = t3
        }
        else
          t1.setDate(t1.getDate() + this.ctDelta['small'])
      }
      else {
        t2.setHours(t2.getHours() + this.ctDelta['amount'])
        if (t2 > t3) {
          t1.setHours(t3.getHours() - this.ctDelta['amount'])
          t2 = t3
        }
        else
          t1.setHours(t1.getHours() + this.ctDelta['small'])
      }
      this.fromDate = t1
      this.toDate = t2
      this.getReadings()
    },
    forward() {
      let t1 = new Date(this.fromDate)
      let t2 = new Date(this.toDate)
      let t3 = new Date()
      if (this.ctDelta['type'] == 'day'){  // Does time interval span hours or days?
        t2.setDate(t2.getDate() + this.ctDelta['small'])
        if (t2 > t3) {
          t1.setDate(t3.getDate() - this.ctDelta['small'])
          t2 = t3
        }
        else
          t1.setDate(t1.getDate() + this.ctDelta['small'])
      }
      else {
        t2.setHours(t2.getHours() + this.ctDelta['small'])
        if (t2 > t3) {
          t1.setHours(t3.getHours() - this.ctDelta['small'])
          t2 = t3
        }
        else
          t1.setHours(t1.getHours() + this.ctDelta['small'])
      }
      this.fromDate = t1
      this.toDate = t2
      this.getReadings()
    },
    zoomOut() {
      this.tDeltaSelection -= 1
      let tmpDate = this.fromDate
      if (this.tDelta[this.tDeltaSelection]['type'] == 'day'){  // Does new time interval span hours or days
        let t2 = new Date(tmpDate)
        if (t2.setDate(tmpDate.getDate() + this.tDelta[this.tDeltaSelection]['amount']) > Date.now()) {  // Is the interval too large?
          this.toDate = new Date()
          tmpDate = new Date()
          tmpDate.setDate(tmpDate.getDate() - this.tDelta[this.tDeltaSelection]['amount'])
          this.fromDate = tmpDate
        }
        else {
          this.toDate = t2
        }
      }
      else {
        let t3 = new Date(tmpDate)
        if (t3.setHours(tmpDate.getHours() + this.tDelta[this.tDeltaSelection]['amount']) > Date.now()) { // Is the interval too large?
          this.toDate = new Date()
          tmpDate = new Date()
          tmpDate.setHours(tmpDate.getDate() - this.tDelta[this.tDeltaSelection]['amount'])
          this.fromDate = tmpDate

        }
        else {
          this.toDate = t3
        }
      }
      this.getReadings()
    },
    zoomIn() {
      this.tDeltaSelection += 1
      let tmpDate = this.fromDate
      if (this.tDelta[this.tDeltaSelection]['type'] == 'day'){  // Does new time interval span hours or days
        tmpDate = new Date(this.toDate)
        tmpDate.setDate(tmpDate.getDate() - this.tDelta[this.tDeltaSelection]['amount'])
        this.fromDate = tmpDate
      }
      else {
        tmpDate = new Date(this.toDate)
        tmpDate.setHours(tmpDate.getHours() - this.tDelta[this.tDeltaSelection]['amount'])
        this.fromDate = tmpDate
      }
      this.getReadings()
    },
    getReadings() {
      this.loaded = false;
      this.humidityDataCollection = []
      this.temperatureDataCollection = []
      let fromDate = this.formatDate(this.fromDate)
      let toDate = this.formatDate(this.toDate)
        for (const room of Object.keys(this.rooms)) {
          let tmp = `room_name=${room}&from_date=${fromDate}&to_date=${toDate}`
          axios.get(this.apiUrl + tmp, { headers: { 'Access-Control-Allow-Origin': true }})
          .then(response => { 
              this.processReadings(room, response.data)
          })
        }
    },
    processReadings(room, data) {
      let c_room = this.rooms[room]
      let lookups = this.sensorLookup[room]
      //let date_time_set = []
      for (const packet of Object.values(data)) {
        for (const record of Object.values(packet.data)) {
          if (record.type == "humidity") {
            c_room[lookups[record.sensor_id]].humidity[packet.date_time] = record.value
          }
          else {
            c_room[lookups[record.sensor_id]].temperature[packet.date_time] = Math.round((record.value*1.8+32)*10)/10   // TODO: Implement C/F degree switch
          }
        }
      }
      for (const [key, value] of Object.entries(c_room)) {
        console.log(key)
        console.log(value)
        this.temperatureDataCollection.push({'name': room + ": " + key, 'data': value.temperature})
        this.humidityDataCollection.push({'name': room + ": " + key, 'data': value.humidity})
      }
    },
    formatDate(_date) {
      let months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
      return months[_date.getMonth()] + '-' + _date.getDate() + '-' + _date.getFullYear() + ' ' + _date.getHours() + ':' + _date.getMinutes() + ':' + _date.getSeconds()
    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h2 {
  margin: 10px 0 0 0;
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

.date_selection_outer{
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 10px;
}

.graph_container{
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

.graph{
  width: 100%;
}
</style>
