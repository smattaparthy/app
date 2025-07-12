const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000', // Your Flask backend URL
        changeOrigin: true,
        ws: true, // good for websockets if needed later
      },
    },
  },
  // Output built static files to a directory Flask can serve
  outputDir: '../backend/static/vue',
  // Adjust public path if assets are not found,
  // for SPA, this is usually fine.
  // publicPath: process.env.NODE_ENV === 'production' ? '/static/vue/' : '/'
});
