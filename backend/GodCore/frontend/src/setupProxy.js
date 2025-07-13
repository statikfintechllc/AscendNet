const { createProxyMiddleware } = require('http-proxy-middleware');

// Proxy all API requests to your router running on port 8088
module.exports = function(app) {
  app.use(
    '/api',
    createProxyMiddleware({
      target: 'http://localhost:8088',
      changeOrigin: true,
      pathRewrite: { '^/api': '' }, // Remove `/api` prefix when forwarding
    })
  );
};
