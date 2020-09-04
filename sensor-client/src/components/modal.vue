<template>
   <portal to="modal">
  <transition name="modal">
        <div class="modal-mask" @click="close">
          <div class="modal-wrapper">
            <div class="modal-container fixed bottom-0 inset-x-0 px-4 pb-4 sm:inset-0 sm:flex sm:items-center sm:justify-center" @click.stop>
                <header class="modal-header">
                <slot name="header">
                    This is the default tile!
                </slot>
                </header>

                <section class="modal-body">
                <slot name="body">
                    I'm the default body!
                </slot>
                </section>

                <footer class="modal-footer">
                <slot name="footer">
                    <button type="button" class="btn btn-green" @click="close" aria-label="Close modal">
                    Cancel
                    </button>
                    <button type="button" class="btn btn-green" @click="save" aria-label="Save modal">
                    Save
                    </button>
                </slot>
                </footer>
            </div>
          </div>
        </div>
      </transition>
   </portal>
</template>
<script>
  export default {
    name: 'modal',
    methods: {
      close() {
        this.$emit('close');
      },
      save() {
        this.$emit('save');
      },
      keyPress(e) {
          if (e.keyCode == 27) {    // Listens for 'Escape' key
              this.close()
              document.removeEventListener("keyup", this.keyPress);
          }
      }
    },
    created() {
        document.addEventListener("keyup", this.keyPress)
    },
    destroyed() {
    }
  };
</script>
<style>
  .modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: table;
  transition: opacity 0.3s ease;
}

.modal-wrapper {
  display: table-cell;
  vertical-align: middle;
}

.modal-container {
  width: 400px;
  margin: 0px auto;
  padding: 10px 30px;
  background-color: #fff;
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
  transition: all 0.3s ease;
  font-family: Helvetica, Arial, sans-serif;
}

.modal-header {
  color: #4aae9b;
  justify-content: space-between;
  padding: 0px 0px;
  display: flex;
  align-items: center;
  padding: 5px 0px;
}


.modal-body {
  position: relative;
  padding: 20px 0px;
  text-align: left;
  min-height: 5rem;
}

.modal-footer {
  justify-content: flex-end;
  padding: 10px 0px;
  display: flex;
}

.modal-header h3 {
  margin: 0;
  color: #42b983;
  text-align: left;
}


.modal-default-button {
  float: right;
}

.btn-close {
  border: none;
  font-size: 20px;
  padding: 20px;
  cursor: pointer;
  font-weight: bold;
  color: #4aae9b;
  background: transparent;
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

/*
 * The following styles are auto-applied to elements with
 * transition="modal" when their visibility is toggled
 * by Vue.js.
 *
 * You can easily play with the modal transition by editing
 * these styles.
 */

.modal-enter {
  opacity: 0;
}

.modal-leave-active {
  opacity: 0;
}

.modal-enter .modal-container,
.modal-leave-active .modal-container {
  -webkit-transform: scale(1.1);
  transform: scale(1.1);
}

</style>