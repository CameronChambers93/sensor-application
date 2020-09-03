<template>
    <div>
        <md-card class="outer_card">
            <md-card-header>
                <h2>Current Readings</h2>
            </md-card-header>

            <md-card-content class="outer_card_content">
                <div class="md-layout md-gutter md-alignment-center" v-if="loaded">
                    <md-card class="inner_card" v-for="room in data" v-bind:key="room.index">
                        <md-card-header>
                            <h2>{{room.room_name}}</h2>
                        </md-card-header>

                        <md-card-content class="inner_card_content">
                            <div v-for="(value, key) in room.readings" v-bind:key="key">

                                <md-card>
                                    <md-card-header>
                                        <h2>{{ value.name }}</h2>
                                        
                                    </md-card-header>

                                    <md-card-content class="room_card_content">
                                        <div v-if="!isRoomAlive(room.date_time)" style="color: red">
                                            <h2>Disconnected</h2>
                                        </div>
                                        <div v-else>
                                            <div>
                                                Humidity: {{value.humidity}}%
                                            </div>
                                            <div>
                                                Temperature: {{Math.round((value.temperature * 1.8 + 32)*10)/10 }} °F
                                            </div>      
                                        </div>     
                                    </md-card-content>
                                </md-card>
                            </div>
                        </md-card-content>

                    </md-card>
                </div>
            </md-card-content>
        </md-card>
    </div>
</template>

<script>
import axios from 'axios'
export default {
  components: {
  },
  props: {
  },
  data() {
      return {
        endpoint: "http://192.168.1.25:5000/",
        loaded: false,
        data: {},
        timer: '',
        lastUpdated: '',
      }
  },
  created()  {
      this.timer = setInterval(this.getSettings, 10000)
      this.getSettings()
  },
  methods: {
      getSettings() {
        axios.get(this.endpoint + "get_current_readings")
        .then(response => {
            this.loaded = false
            this.data = response.data.data
            this.lastUpdated = response.data.date_time
            this.loaded = true
        })
        .catch(error => {
            console.log('-----error-------');
            console.log(error);
        })
      },
      cancelAutoUpdate () { clearInterval(this.timer) },
      isRoomAlive(dt2) {
          let ct = new Date()
          ct.setMinutes(ct.getMinutes() - 2)
          ct.setHours(ct.getHours() - 5)    // Remove this when date_time is corrected in the DB
          let dt = new Date(dt2)
          return (dt > ct)
      }
  },
  beforeDestroy () {
      clearInterval(this.timer)
  },
  watch: {
  }
}
</script>

<style>
.md-card{
    margin: 10px;
}

.inner_card{
}

.outer_card_content{
    display: flex;
    flex-wrap: wrap;
}

.inner_card_content{
    display: flex;
}

.room_card_content{
    display: block;
}
</style>
