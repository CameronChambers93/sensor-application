// vue.config.js
module.exports = {
  // options...
  devServer: {
    disableHostCheck: true,
    proxy: {
      "/": {
         target: "",
         secure: false
      }
    }
  },
  configureWebpack: {
    devtool: 'source-map',
    resolve: {
      alias: {
        'vue$': 'vue/dist/vue.esm.js' // To enable runtime compiler
      }
    }
  },
}
