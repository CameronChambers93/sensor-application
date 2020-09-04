<template>
  <div id="settings">
      <md-card>
        <md-card-header>
            <h2>Settings</h2>
        </md-card-header>
      <md-card-content>
        <md-field>
            <label for="device">Device</label>
            <md-select v-model="currentDevice" name="device" id="device">
                <md-option v-for="(device, index) in settings" v-bind:key="index" :value=index>{{ device.device_name }}</md-option>
            </md-select>
        </md-field>
        <div v-if="currentSettings != null">    
            
            <md-card class="md-layout-item md-size-100">
                <md-card-header>
                    <div>
                        <h2>Name: {{currentSettings.device_name}}</h2>
                        <h3>IP: {{currentSettings.ip}}</h3>

                        <button
                        type="button"
                        class="btn"
                        @click="showModal"
                        >
                            Edit Device Settings
                        </button>

                        <modal
                        v-if="isModalVisible"
                        @close="closeModal"
                        @save="saveModal"
                        >
                            <h3 slot="header">Edit Device</h3>
                            <div slot="body">
                                <md-field>
                                    <label>Name: </label>
                                    <md-input v-model="newDeviceName"></md-input>
                                </md-field>
                                <md-field>
                                    <label>IP: </label>
                                    <md-input v-model="newDeviceIP"></md-input>
                                </md-field>
                            </div>
                        </modal>
                    </div>
                    
                </md-card-header>
                <md-card-content>
                    
                    <div class="device-list">
                        <md-card class="settings-card md-layout-item md-large-size-30 md-medium-size-33 md-small-size-100 md-xsmall-size-100" v-for="(sensor, index) in currentSettings.sensors" v-bind:key="settingsRefreshKeys[index]">
                            <md-card-header>
                                {{sensor.sensor_name}}
                            </md-card-header>
                            <md-card-content>
                                <div v-if="readOnly[index]">
                                    <md-field>
                                    <label>GPIO Pin: {{sensor.gpio_pin}}</label>
                                    </md-field>
                                    <md-field>
                                        <label>Sensor Id: {{sensor.sensor_id}}</label>
                                    </md-field>
                                    <md-field>
                                        <label>Sensor Type: {{sensor.sensor_type}}</label>
                                    </md-field>
                                </div>
                                    
                                <div v-if="!readOnly[index]">
                                    <md-field>
                                        <label>Sensor Name: </label>
                                        <md-input v-model="currentSensorSettings[index].sensor_name" v-bind:disabled="readOnly[index]"></md-input>
                                    </md-field>
                                    <md-field>
                                        <label>GPIO Pin: </label>
                                        <md-input v-model="currentSensorSettings[index].gpio_pin" v-bind:disabled="readOnly[index]"></md-input>
                                    </md-field>
                                    <md-field>
                                        <label>Sensor Id: </label>
                                        <md-input v-model="currentSensorSettings[index].sensor_id" v-bind:disabled="readOnly[index]"></md-input>
                                    </md-field>
                                    <md-field>
                                        <label>Sensor Type: </label>
                                        <md-input v-model="currentSensorSettings[index].sensor_type" v-bind:disabled="readOnly[index]"></md-input>
                                    </md-field>
                                </div>
                                <md-button class="btn" v-if="readOnly[index]" @click="editSensor(index)">Edit</md-button>
                                <md-button class="btn" v-if="!readOnly[index]" @click="closeEdit(index)">Cancel</md-button>
                                <md-button class="btn" v-if="!readOnly[index]" @click="deleteSensor(index)">Delete</md-button>
                                <md-button class="btn" v-if="!readOnly[index]" @click="saveSensor(index)">Save</md-button>
                            </md-card-content>
                        </md-card>

                        
                        <md-card class="settings-card md-layout-item md-large-size-30 md-medium-size-33 md-small-size-100 md-xsmall-size-100" v-if="addingNewSensor">
                            <md-card-header>
                                Add Sensor
                            </md-card-header>
                            <md-card-content>

                                <md-field>
                                    <label>Sensor Name: </label>
                                    <md-input v-model="newSensor.sensor_name"></md-input>
                                </md-field>
                                <md-field>
                                    <label>GPIO Pin: </label>
                                    <md-input v-model="newSensor.gpio_pin"></md-input>
                                </md-field>
                                <md-field>
                                    <label>Sensor Id: </label>
                                    <md-input v-model="newSensor.sensor_id"></md-input>
                                </md-field>
                                <md-field>
                                    <label>Sensor Type: </label>
                                    <md-input v-model="newSensor.sensor_type"></md-input>
                                </md-field>
                                
                                <md-button class="md-primary md-raised" @click="addingNewSensor=false">Cancel</md-button>
                                <md-button class="md-primary md-raised" @click="addSensor()">Save</md-button>

                            </md-card-content>
                        </md-card>
                    <div v-else>
                        <md-button class="md-icon-button md-raised md-primary" @click="addingNewSensor=true"><md-icon>add</md-icon></md-button>
                    </div>
                        </div>
                    
                </md-card-content>
            </md-card>
            


        </div>
        <md-button class="md-primary md-raised" v-bind:disabled="!updateAvailable" @click="updateSettings()">Update</md-button>
      </md-card-content>
    </md-card>
  </div>
</template>

<script>
import axios from 'axios'
import Modal from './modal.vue'
export default {
  name: 'settings',
  calculated: {
  },
  components: {
    Modal
  },
  props: {
      originalSettings: {   // Stores all devices' info
          type: Array,
          default: () => {
              return []
          }
      }
  },
  created() {
    this.settings = this.originalSettings
  },
  data: () => ({
      settings: {},                               
      currentDevice: "",                                    // Stores the name of the current device
      currentSettings: null,                                  // Stores device info {device_name: String, sensors: Array}
      currentSensorSettings: [],                            // Clone of currentSettings.sensors; used to validate and update entries
      readOnly: [],                                         // Switches a sensor's settings from read only to writeable
      settingsRefreshKeys: [],                              // For refreshing individual sensor settings panels
      deviceSelect: false,
      updateAvailable: false,
      addingNewSensor: false,
      newSensor: {"sensor_name": "", "gpio_pin": null, "sensor_id": null, "sensor_type": ""},
      endpoint: "http://192.168.1.25:5000/",
      isModalVisible: false,
      newDeviceName: "",
      newDeviceIP: ""
  }),
  methods: {    // TODO: Add modal to replace edit pages
      editSensor(index) {   
        let tmpSettings = this.currentSettings.sensors[index]           // Reloads sensor data from permanent copy
        this.$set(this.currentSensorSettings, index, Object.assign({}, tmpSettings))
        this.$set(this.readOnly, index, false)
      },
      saveSensor(index) {
          let tmpSettings = this.currentSensorSettings[index]       // Edited settings for an individual sensor
          if (JSON.stringify(tmpSettings) !== JSON.stringify(this.currentSettings.sensors[index]))
            this.updateAvailable = true
          this.$set(this.currentSettings.sensors, index, tmpSettings)
          this.$set(this.readOnly, index, true)
          this.$set(this.settingsRefreshKeys, index, this.settingsRefreshKeys[index] + 1)
      },
      closeEdit(index) {
          this.$set(this.readOnly, index, true)
          this.$set(this.settingsRefreshKeys, index, this.settingsRefreshKeys[index] + 1)
      },
      updateSettings() {
        let bodyFormData = new FormData()
        bodyFormData.set('data', this.currentSettings)
        axios.post(this.endpoint + "set_settings", { data: this.currentSettings })
        .then(() => {
            alert("Upload successful")
            this.updateAvailable = false
        })
        .catch(error => {
            console.log('-----error-------');
            console.log(error);
            alert("Upload unsuccessful")
        })
        //this.getSettings()
      },
      addSensor() {
          this.readOnly.push(true)
          this.addingNewSensor = false
          this.updateAvailable = true
          this.currentSensorSettings.push(this.newSensor)
          this.currentSettings.sensors.push(this.newSensor)
          this.newSensor = {"sensor_name": "", "gpio_pin": null, "sensor_id": null, "sensor_type": ""}
      },
      deleteSensor(index) {
          this.currentSettings.sensors.splice(index,1)
          this.currentSensorSettings.splice(index,1)
          this.readOnly.splice(index,1)
          this.settingsRefreshKeys.splice(index,1)
          this.updateAvailable = true
      },
      showModal() {
        this.isModalVisible = true;
      },
      closeModal() {
        this.newDeviceIP = this.currentSettings.ip
        this.newDeviceName = this.currentSettings.device_name
            this.isModalVisible = false;
      },
      saveModal() {
          this.currentSettings.device_name = this.newDeviceName
          this.currentSettings.ip = this.newDeviceIP
            this.isModalVisible = false;
            this.updateAvailable = true
      }
  },
  watch: {
      currentDevice: function(val) {
        this.currentSettings = this.settings[val]
        this.newDeviceIP = this.currentSettings.ip
        this.newDeviceName = this.currentSettings.device_name
        let tmpReadOnly = []
        let tmpSettings = []
        this.settingsRefreshKeys = []
        for (const [key, value] of Object.entries(this.currentSettings['sensors'])) {
            tmpReadOnly.push(true)
            tmpSettings.push(value)
            this.settingsRefreshKeys.push(key*436 + 7 * key)
        }
        this.currentSensorSettings = tmpSettings
        this.readOnly = tmpReadOnly
      },
  }
}
</script>
<!-- styling for the component -->
<style>
#settings {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.device-list{
    display: flex;
    flex-wrap: wrap;
}

.settings-card{
    margin-bottom: 20px;
}

.btn {
  padding: 8px 16px;
  border-radius: 3px;
  font-size: 14px;
  cursor: pointer;
  color: white;
  background: #4aae9b;
  border: 1px solid #4aae9b;
  border-radius: 5px;
  margin: 0 0 0 10px;
}
</style>