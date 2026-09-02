import { Link, useLocation } from 'react-router-dom'
import { useAppStore } from '../store/appStore'
import {
  BarChart3,
  BookOpen,
  Home,
  RotateCcw,
  Settings,
  Zap,
  FileText,
  X,
} from 'lucide-react'
import { useEffect } from 'react'

const navItems = [
  { icon: Home, label: 'Dashboard', path: '/' },
  { icon: BookOpen, label: 'Syllabus', path: '/syllabus' },
  { icon: Zap, label: 'Study Log', path: '/study-log' },
  { icon: BarChart3, label: 'Analytics', path: '/analytics' },
  { icon: RotateCcw, label: 'Revision', path: '/revision' },
  { icon: Settings, label: 'Settings', path: '/settings' },
]

export default function Sidebar() {
  const location = useLocation()
  const { sidebarOpen, setSidebarOpen } = useAppStore()

  // Close sidebar on mobile when navigating
  useEffect(() => {
    setSidebarOpen(false)
  }, [location.pathname])

  return (
    <>
      {/* Mobile overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-30 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`fixed lg:static w-64 h-screen bg-card border-r border-border overflow-y-auto transition-all duration-300 z-40 ${
          sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        }`}
      >
        <div className="p-6 border-b border-border">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
                <span className="text-primary-foreground font-bold">DS</span>
              </div>
              <h2 className="font-bold text-lg">Journey</h2>
            </div>
            <button
              onClick={() => setSidebarOpen(false)}
              className="lg:hidden p-1 hover:bg-muted rounded"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        <nav className="p-4 space-y-2">
          {navItems.map((item) => {
            const Icon = item.icon
            const isActive = location.pathname === item.path
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-3 px-4 py-3 rounded-lg transition ${
                  isActive
                    ? 'bg-primary text-primary-foreground'
                    : 'text-foreground hover:bg-muted'
                }`}
              >
                <Icon className="w-5 h-5" />
                <span className="font-medium">{item.label}</span>
              </Link>
            )
          })}
        </nav>

        {/* Footer info */}
        <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-border bg-muted/50">
          <div className="text-xs text-muted-foreground space-y-2">
            <p className="font-semibold">DS Journey v1.0</p>
            <p>150-day Data Science learning path</p>
          </div>
        </div>
      </aside>
    </>
  )
}
