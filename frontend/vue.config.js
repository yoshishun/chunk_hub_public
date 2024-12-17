const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  assetsDir: "static",
  outputDir: "../dist",
  filenameHashing: false,
  pages: {
    
    index: {
      entry: 'src/pages/index/main.js', 
      template: 'public/index.html', 
      filename: 'index.html', 
    },
  },
  
  pwa: {
    name: 'Chunk Hub',
    themeColor: '#4DBA87',
    msTileColor: '#000000',
    appleMobileWebAppCapable: 'yes',
    appleMobileWebAppStatusBarStyle: 'black',
    manifestOptions: {
      name: 'Chunk Hub',
      short_name: 'Chunk Hub',
      start_url: '/',
      display: 'standalone',
      background_color: '#42B883',
      theme_color: '#4DBA87',
      icons: [
        {
          src: '/static/img/icons/chunk_hub-icon-192x192.png',
          sizes: '192x192',
          type: 'image/png'
        },
        {
          src: '/static/img/icons/chunk_hub-icon-512x512.png',
          sizes: '512x512',
          type: 'image/png'
        }
      ]
    },
    workboxPluginMode: 'GenerateSW',
    workboxOptions: {
      skipWaiting: true
    }
  }
})