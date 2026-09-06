import axios, { AxiosInstance } from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api'

const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add token to requests if available
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default apiClient

// Module APIs
export const modulesApi = {
  getAll: () => apiClient.get('/modules'),
  getById: (id: number) => apiClient.get(`/modules/${id}`),
  getProgress: (id: number) => apiClient.get(`/modules/${id}/progress`),
}

// Topic APIs
export const topicsApi = {
  getAll: (moduleId?: number, status?: string) => 
    apiClient.get('/topics', { params: { module_id: moduleId, status_filter: status } }),
  getById: (id: number) => apiClient.get(`/topics/${id}`),
  update: (id: number, data: any) => apiClient.put(`/topics/${id}`, data),
  getSubtopics: (id: number) => apiClient.get(`/topics/${id}/subtopics`),
  addSubtopic: (id: number, data: any) => apiClient.post(`/topics/${id}/subtopics`, data),
  updateSubtopic: (subtopicId: number, data: any) => 
    apiClient.put(`/topics/subtopics/${subtopicId}`, data),
  getStudySessions: (id: number) => apiClient.get(`/topics/${id}/study-sessions`),
}

// Study Session APIs
export const studySessionsApi = {
  create: (data: any) => apiClient.post('/study-sessions', data),
  getAll: (topicId?: number, moduleId?: number, startDate?: string, endDate?: string, limit?: number) =>
    apiClient.get('/study-sessions', { params: { topic_id: topicId, module_id: moduleId, start_date: startDate, end_date: endDate, limit } }),
  getById: (id: number) => apiClient.get(`/study-sessions/${id}`),
  update: (id: number, data: any) => apiClient.put(`/study-sessions/${id}`, data),
  delete: (id: number) => apiClient.delete(`/study-sessions/${id}`),
  getTodayStats: () => apiClient.get('/study-sessions/stats/today'),
  getStreak: () => apiClient.get('/study-sessions/stats/streak'),
}

// Analytics APIs
export const analyticsApi = {
  getOverview: () => apiClient.get('/analytics/overview'),
  getStudyHoursOverTime: (days?: number) => 
    apiClient.get('/analytics/study-hours-over-time', { params: { days } }),
  getStudyHoursByModule: () => apiClient.get('/analytics/study-hours-by-module'),
  getStudyHoursByTopic: (limit?: number) => 
    apiClient.get('/analytics/study-hours-by-topic', { params: { limit } }),
  getWeeklyStats: () => apiClient.get('/analytics/weekly-stats'),
}

// Revision APIs
export const revisionsApi = {
  create: (data: any) => apiClient.post('/revisions', data),
  getAll: () => apiClient.get('/revisions'),
  getById: (id: number) => apiClient.get(`/revisions/${id}`),
  getDue: (status?: string) => apiClient.get('/revisions/due', { params: { status_filter: status } }),
  update: (id: number, data: any) => apiClient.put(`/revisions/${id}`, data),
  delete: (id: number) => apiClient.delete(`/revisions/${id}`),
  snooze: (id: number, days?: number) => 
    apiClient.post(`/revisions/${id}/snooze`, null, { params: { days } }),
  scheduleRevision: (topicId: number, daysUntil?: number) =>
    apiClient.post(`/revisions/schedule/${topicId}`, null, { params: { days_until: daysUntil } }),
}

// Recommendations API
export const recommendationsApi = {
  getRecommendations: (limit?: number) => 
    apiClient.get('/recommendations', { params: { limit } }),
}

// Users API
export const usersApi = {
  getMe: () => apiClient.get('/users/me'),
  updateProfile: (data: any) => apiClient.put('/users/me', data),
  getById: (id: number) => apiClient.get(`/users/${id}`),
}

// Auth API
export const authApi = {
  register: (data: any) => apiClient.post('/auth/register', data),
  login: (email: string, password: string) => 
    apiClient.post('/auth/token', null, { params: { username: email, password } }),
  getToken: (username: string, password: string) =>
    apiClient.post('/auth/token', null, { params: { username, password } }),
}
