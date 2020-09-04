<template>
<div>
    <line-chart class="chart" v-if="loaded" width="100%" ytitle="Temperature (°F)" :min="null" :data="temperatureDataCollection"></line-chart>
</div>
</template>

<script>
export default {
  components: {
  },
  props: {
    temperatureDataCollection: {
        type: Array,
        default: () => {return []}
    }
  },
  data() {
      return {
        apiUrl: "http://192.168.1.25:5000/get_readings?",
        labels: [],
        records: [],
        chartOptions: {responsive: true, maintainAspectRatio: false},
        loaded: false
      }
  },
  watch: {
    temperatureDataCollection: function(val) {
      if (val != null) {
        this.loaded = true
      }
    }
  },
  methods: {
  }
}
</script>

<style>
.chart{
    width: 100%;
}
</style>
