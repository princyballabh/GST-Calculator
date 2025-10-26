// Environment configuration for different deployments
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? process.env.NEXT_PUBLIC_API_URL || 'https://your-backend-service.railway.app'
  : 'http://127.0.0.1:8000';

export default API_BASE_URL;