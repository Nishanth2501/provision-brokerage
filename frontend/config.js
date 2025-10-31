// API Configuration
// Use deployed backend URL in production, localhost in development
const API_BASE_URL = window.location.hostname === 'localhost' 
  ? 'http://localhost:8000'
  : 'https://provision-brokerage-30.onrender.com';

// Make it globally available
window.API_BASE_URL = API_BASE_URL;

console.log('✅ Config.js loaded');
console.log('🌐 API Base URL:', API_BASE_URL);
console.log('🖥️ Current hostname:', window.location.hostname);
