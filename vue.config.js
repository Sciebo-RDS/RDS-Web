module.exports = {
  transpileDependencies: [
    'vuetify',
    'vue-oidc-client'
  ],
  devServer: {
    proxy: 'http://localhost:8080'
  },
}
