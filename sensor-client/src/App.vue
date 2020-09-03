<template>
  <div id="app">
    <md-app>
      <md-app-toolbar>
        <md-button class="md-icon-button" @click="toggleMenu" v-if="!menuVisible">
          <md-icon>menu</md-icon>
        </md-button>
        <img style="margin-left:.5rem; height:60px;" alt="Vue logo" src="./assets/logo.png">
        Sensor Application
      </md-app-toolbar>

      <md-app-drawer class="app-drawer" :md-active.sync="menuVisible" :md-persistent=mini>
        <md-toolbar class="md-transparent" md-elevation="0">
          <span>Navigation</span>

          <div class="md-toolbar-section-end">
            <md-button class="md-icon-button md-dense" @click="toggleMenu">
              <md-icon>keyboard_arrow_left</md-icon>
            </md-button>
          </div>
        </md-toolbar>

        <md-list>
          <router-link v-bind:to="'/'">
            <md-list-item>
              <md-icon>insights</md-icon>
              <span class="md-list-item-text">View Data</span>
            </md-list-item>
          </router-link>

          <router-link v-bind:to="'/settings'">
            <md-list-item >
              <md-icon>settings</md-icon>
              <span class="md-list-item-text">Settings</span>
            </md-list-item>
          </router-link>
        </md-list>
      </md-app-drawer>

      <md-app-content>
        <router-view v-if="settings != null" :originalSettings="settings">
        </router-view>

        
      </md-app-content>

    </md-app>
    
        <portal-target name="modal"/>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'App',
  data: () => ({
    menuVisible: false,
    settings: null,
    endpoint: "http://192.168.1.25:5000/",
  }),
  created() {
    this.getSettings()
  },
  computed: {
    mini: function() {
    return ((window.innerWidth > 500) ? "mini" : "full")
    }
  },
  methods: {
    toggleMenu() {
      this.menuVisible = !this.menuVisible;
    },
    loadSettings() {
      /*
        this.settings = data
        let tmpReadOnly = []
        let tmpSettings = []
        this.settingsRefreshKeys = []
        for (const [key, value] of Object.entries(data)) {
          let entries = value.sensors
          for (let i = 0; i < entries.length; i++) {
            tmpReadOnly.push(true)
            tmpSettings.push(entries[i])
            this.settingsRefreshKeys.push(i*436 + 7)
          }
        }
        this.currentSensorSettings = tmpSettings
        this.readOnly = tmpReadOnly
        */
    },
    getSettings() {
      axios.get(this.endpoint + "get_settings")
      .then(response => {
        this.settings = response.data
      })
      .catch(error => {
          console.log('-----error-------');
          console.log(error);
      })
    },
    updateSettings() {
      let bodyFormData = new FormData()
      bodyFormData.set('data', this.currentSettings)
      axios.post(this.endpoint + "set_settings", { data: this.currentSettings })
      .then(response => {
          alert("Upload successful")
          this.updateAvailable = false
          this.loadSettings(response.data)
      })
      .catch(error => {
          console.log('-----error-------');
          console.log(error);
          alert("Upload unsuccessful")
      })
      //this.getSettings()
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  justify-content: center;
  display: flex;
  height: 100%;
}

.md-persistent-mini{
}

.md-app{
  width: 100%;
}

html, body {
  height: 100%;
}

</style>
