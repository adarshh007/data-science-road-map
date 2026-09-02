import { create } from 'zustand'

export interface Module {
  id: number
  number: number
  title: string
  description: string
  total_days: number
  order: number
  created_at: string
  updated_at: string
}

export interface Topic {
  id: number
  module_id: number
  day_id: number | null
  day_start: number
  day_end: number
  title: string
  description: string
  status: string
  progress: number
  confidence: number
  importance: number
  estimated_hours: number
  actual_hours: number
  notes: string
  last_studied: string | null
  next_revision: string | null
  revision_count: number
  created_at: string
  updated_at: string
  subtopics: any[]
}

export interface StudySession {
  id: number
  user_id: number
  module_id: number | null
  topic_id: number
  date: string
  start_time: string
  end_time: string
  duration_minutes: number
  what_learned: string
  what_practiced: string
  difficulty: number
  confidence_before: number
  confidence_after: number
  notes: string
  created_at: string
  updated_at: string
}

interface AppStore {
  // Modules
  modules: Module[]
  setModules: (modules: Module[]) => void
  addModule: (module: Module) => void
  
  // Topics
  topics: Topic[]
  setTopics: (topics: Topic[]) => void
  addTopic: (topic: Topic) => void
  updateTopic: (id: number, topic: Partial<Topic>) => void
  currentTopic: Topic | null
  setCurrentTopic: (topic: Topic | null) => void
  
  // Study Sessions
  studySessions: StudySession[]
  setStudySessions: (sessions: StudySession[]) => void
  addStudySession: (session: StudySession) => void
  
  // UI State
  sidebarOpen: boolean
  setSidebarOpen: (open: boolean) => void
  theme: 'light' | 'dark' | 'system'
  setTheme: (theme: 'light' | 'dark' | 'system') => void
  
  // Loading states
  isLoading: boolean
  setIsLoading: (loading: boolean) => void
  error: string | null
  setError: (error: string | null) => void
}

export const useAppStore = create<AppStore>((set) => ({
  // Modules
  modules: [],
  setModules: (modules) => set({ modules }),
  addModule: (module) => set((state) => ({
    modules: [...state.modules, module]
  })),
  
  // Topics
  topics: [],
  setTopics: (topics) => set({ topics }),
  addTopic: (topic) => set((state) => ({
    topics: [...state.topics, topic]
  })),
  updateTopic: (id, updates) => set((state) => ({
    topics: state.topics.map((t) => t.id === id ? { ...t, ...updates } : t)
  })),
  currentTopic: null,
  setCurrentTopic: (topic) => set({ currentTopic: topic }),
  
  // Study Sessions
  studySessions: [],
  setStudySessions: (sessions) => set({ studySessions: sessions }),
  addStudySession: (session) => set((state) => ({
    studySessions: [...state.studySessions, session]
  })),
  
  // UI State
  sidebarOpen: true,
  setSidebarOpen: (open) => set({ sidebarOpen: open }),
  theme: 'system',
  setTheme: (theme) => set({ theme }),
  
  // Loading states
  isLoading: false,
  setIsLoading: (loading) => set({ isLoading: loading }),
  error: null,
  setError: (error) => set({ error }),
}))
