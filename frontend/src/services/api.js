import axios from 'axios'

// ── Base Axios Instance ────────────────────────────────────────────────────────
const api = axios.create({
  baseURL: '/api',                // Vite proxy forwards → http://localhost:8000/api
  timeout: 15000,
  headers: { 'Content-Type': 'application/json' },
})

// ── Request Interceptor: attach JWT token ─────────────────────────────────────
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('agrogen_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error),
)

// ── Response Interceptor: handle 401 globally ────────────────────────────────
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('agrogen_token')
      localStorage.removeItem('agrogen_user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  },
)

// ── Helper to extract server error message ────────────────────────────────────
export const getErrorMessage = (error) => {
  if (error.response?.data?.detail) {
    const detail = error.response.data.detail
    if (typeof detail === 'string') return detail
    if (Array.isArray(detail)) return detail.map((d) => d.msg).join(', ')
  }
  return error.message || 'Something went wrong. Please try again.'
}

// ═══════════════════════════════════════════════════════════════════════════════
//  AUTH ENDPOINTS
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Register a new farmer account.
 * @param {{ full_name, email, phone, password, preferred_lang }} data
 */
export const registerUser = (data) => api.post('/auth/register', data)

/**
 * Login with email + password, returns { access_token, token_type }.
 * @param {{ email, password }} data
 */
export const loginUser = (data) => api.post('/auth/login', data)

/**
 * Fetch the authenticated user's profile.
 * Requires Authorization header (attached automatically by interceptor).
 */
export const fetchMe = () => api.get('/auth/me')

/**
 * Google OAuth: Get authorization URL.
 */
export const getGoogleAuthUrl = () => api.get('/auth/google/url').then((res) => res.data?.url || res.data)

/**
 * Google OAuth: Verify GIS credential (ID token) or custom user profile.
 */
export const verifyGoogleCredential = (payload) => {
  const body = typeof payload === 'string' ? { credential: payload } : payload
  return api.post('/auth/google/verify', body).then((res) => res.data)
}

/**
 * Exchange Google authorization code for JWT token and user profile.
 */
export const exchangeGoogleCode = (code) => {
  return api.post('/auth/google/exchange', { code }).then((res) => res.data)
}

/**
 * Logout user session.
 */
export const logoutUser = () => api.post('/auth/logout').catch(() => {})

/**
 * Complete authService matching Omkar and AgroGEN API expectations.
 */
export const authService = {
  login: async (email, password) => {
    const res = await api.post('/auth/login', { email, password })
    return res.data
  },
  register: async (fullName, email, password, role = 'farmer') => {
    const res = await api.post('/auth/register', {
      full_name: fullName,
      email,
      password,
      role,
    })
    return res.data
  },
  getGoogleAuthUrl: async () => {
    const res = await api.get('/auth/google/url')
    return res.data?.url || res.data
  },
  verifyGoogleCredential: async (payload) => {
    const body = typeof payload === 'string' ? { credential: payload } : payload
    const res = await api.post('/auth/google/verify', body)
    return res.data
  },
  exchangeGoogleCode: async (code) => {
    const res = await api.post('/auth/google/exchange', { code })
    return res.data
  },
  getCurrentUser: async () => {
    const res = await api.get('/auth/me')
    return res.data
  },
  logout: async () => {
    try {
      await api.post('/auth/logout')
    } finally {
      localStorage.removeItem('agrogen_token')
      localStorage.removeItem('agrogen_user')
    }
  },
}

// ═══════════════════════════════════════════════════════════════════════════════
//  FARMER PROFILE ENDPOINTS
// ═══════════════════════════════════════════════════════════════════════════════

export const getFarmerProfile = () => api.get('/farmer/profile')
export const upsertFarmerProfile = (data) => api.post('/farmer/profile', data)

// ═══════════════════════════════════════════════════════════════════════════════
//  CROPS ENDPOINTS
// ═══════════════════════════════════════════════════════════════════════════════

export const getCrops = () => api.get('/crops')
export const getCrop = (id) => api.get(`/crops/${id}`)
export const createCrop = (data) => api.post('/crops', data)
export const updateCrop = (id, data) => api.put(`/crops/${id}`, data)
export const deleteCrop = (id) => api.delete(`/crops/${id}`)

// ═══════════════════════════════════════════════════════════════════════════════
//  DISEASE ENDPOINTS
// ═══════════════════════════════════════════════════════════════════════════════

export const detectDisease = (cropId, formData) =>
  api.post(`/disease/detect/${cropId}`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })

export const getDiseaseHistory = (cropId) => api.get(`/disease/history/${cropId}`)

// ═══════════════════════════════════════════════════════════════════════════════
//  WEATHER ENDPOINTS
// ═══════════════════════════════════════════════════════════════════════════════

export const getCurrentWeather = (city) =>
  api.get('/weather/current', { params: { city } })

export const getWeatherHistory = () => api.get('/weather/history')

// ═══════════════════════════════════════════════════════════════════════════════
//  MARKET PRICES ENDPOINTS
// ═══════════════════════════════════════════════════════════════════════════════

export const getMarketPrices = (crop_name) =>
  api.get('/market/prices', { params: crop_name ? { crop_name } : {} })

export const getLatestMarketPrice = (cropName) =>
  api.get(`/market/prices/${cropName}/latest`)

// ═══════════════════════════════════════════════════════════════════════════════
//  GOVERNMENT SCHEMES ENDPOINTS
// ═══════════════════════════════════════════════════════════════════════════════

export const getSchemes = (search) =>
  api.get('/schemes', { params: search ? { search } : {} })

export const getScheme = (id) => api.get(`/schemes/${id}`)

// ═══════════════════════════════════════════════════════════════════════════════
//  CHATBOT ENDPOINTS
// ═══════════════════════════════════════════════════════════════════════════════

export const sendChatMessage = (data) => api.post('/chatbot/chat', data)
export const getChatHistory = (limit = 50) =>
  api.get('/chatbot/history', { params: { limit } })

// ═══════════════════════════════════════════════════════════════════════════════
//  YIELD PREDICTION ENDPOINTS
// ═══════════════════════════════════════════════════════════════════════════════

export const predictYield = (data) => api.post('/yield/predict', data)

// ═══════════════════════════════════════════════════════════════════════════════
//  VOICE AI ENDPOINTS
// ═══════════════════════════════════════════════════════════════════════════════

export const voiceChat = (data) => api.post('/voice/chat', data)
export const generateTTS = (data) => api.post('/voice/tts', data)
export const uploadVoiceAudio = (formData) =>
  api.post('/voice/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })

// ═══════════════════════════════════════════════════════════════════════════════
//  NOTIFICATIONS ENDPOINTS
// ═══════════════════════════════════════════════════════════════════════════════

export const getNotifications = () => api.get('/notifications')
export const markNotificationRead = (id) =>
  api.post(`/notifications/${id}/read`)

// ═══════════════════════════════════════════════════════════════════════════════
//  RECOMMENDATIONS ENDPOINTS
// ═══════════════════════════════════════════════════════════════════════════════

export const getRecommendation = (diseaseId) =>
  api.get(`/recommendations/disease/${diseaseId}`)

export default api
