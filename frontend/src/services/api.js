import axios from 'axios'

// One shared axios instance so we don't repeat the base URL everywhere.
const api = axios.create({
  baseURL: 'http://localhost:8000',
})

// Before every request, if we have a saved login token, attach it.
// This is how the backend knows which user is making the request.
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default api
