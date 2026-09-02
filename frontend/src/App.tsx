import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import { useAppStore } from './store/appStore'
import { modulesApi, topicsApi } from './services/api'

// Pages
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import DashboardPage from './pages/DashboardPage'
import SyllabusPage from './pages/SyllabusPage'
import TopicDetailsPage from './pages/TopicDetailsPage'
import StudyLogPage from './pages/StudyLogPage'
import AnalyticsPage from './pages/AnalyticsPage'
import RevisionPage from './pages/RevisionPage'
import SettingsPage from './pages/SettingsPage'

// Layout
import Navbar from './components/Navbar'
import Sidebar from './components/Sidebar'

import './App.css'

function AppContent() {
  const { isAuthenticated, isLoading } = useAuth()
  const { setModules, setTopics } = useAppStore()
  const [dataLoading, setDataLoading] = useState(true)

  // Load data on app start
  useEffect(() => {
    if (isAuthenticated && !isLoading) {
      loadData()
    }
  }, [isAuthenticated, isLoading])

  const loadData = async () => {
    try {
      const [modulesRes, topicsRes] = await Promise.all([
        modulesApi.getAll(),
        topicsApi.getAll(),
      ])
      setModules(modulesRes.data)
      setTopics(topicsRes.data)
    } catch (error) {
      console.error('Failed to load data:', error)
    } finally {
      setDataLoading(false)
    }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen bg-background">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-foreground">Loading...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="flex h-screen bg-background">
      {isAuthenticated && <Sidebar />}
      <div className="flex flex-col flex-1 overflow-hidden">
        {isAuthenticated && <Navbar />}
        <main className="flex-1 overflow-auto">
          <Routes>
            {!isAuthenticated ? (
              <>
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />
                <Route path="*" element={<Navigate to="/login" />} />
              </>
            ) : (
              <>
                <Route path="/" element={<DashboardPage />} />
                <Route path="/dashboard" element={<DashboardPage />} />
                <Route path="/syllabus" element={<SyllabusPage />} />
                <Route path="/topics/:topicId" element={<TopicDetailsPage />} />
                <Route path="/study-log" element={<StudyLogPage />} />
                <Route path="/analytics" element={<AnalyticsPage />} />
                <Route path="/revision" element={<RevisionPage />} />
                <Route path="/settings" element={<SettingsPage />} />
                <Route path="*" element={<Navigate to="/" />} />
              </>
            )}
          </Routes>
        </main>
      </div>
    </div>
  )
}

function App() {
  return (
    <Router>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </Router>
  )
}

export default App
