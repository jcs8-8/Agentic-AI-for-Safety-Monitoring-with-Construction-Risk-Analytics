import axios from 'axios'
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'
export const api = axios.create({
  baseURL: API_URL,
  headers: { 'Content-Type': 'application/json' }
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('buildsure_access_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

export interface APIResponse<T = any> { success: boolean; data: T; message: string; timestamp: string }