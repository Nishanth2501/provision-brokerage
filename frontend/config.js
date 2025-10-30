// API Configuration
// Use deployed backend URL in production, localhost in development
const API_BASE_URL = window.location.hostname === 'localhost' 
  ? 'http://localhost:8000'
  : 'https://provision-brokerage-1.onrender.com';

console.log('API Base URL:', API_BASE_URL);
