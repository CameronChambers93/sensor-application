<template>
<div>

    <line-chart v-if="loaded" :min="null" ytitle="Relative Humidity (%)" :data="humidityDataCollection"></line-chart>
</div>
</template>

<script>
export default {
  components: {},
  props: {
    humidityDataCollection: {
        type: Array,
        default: () => {return []}
    }
  },
  data() {
      return {
        labels: [],
        records: [],
        chartOptions: {responsive: true, maintainAspectRatio: false},
        loaded: false
      }
  },
  methods: {
  },
  watch: { 
    humidityDataCollection: function(val) {
      if (val != null) {
        this.loaded = true
      }
    }
  }
}
</script>

<style>

</style>