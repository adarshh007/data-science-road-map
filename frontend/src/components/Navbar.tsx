import { Link } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { useAppStore } from '../store/appStore'
import { Menu, LogOut, Settings, User } from 'lucide-react'

export default function Navbar() {
  const { user, logout } = useAuth()
  const { sidebarOpen, setSidebarOpen } = useAppStore()

  return (
    <nav className="bg-card border-b border-border h-16 flex items-center justify-between px-6 sticky top-0 z-40">
      <div className="flex items-center gap-4">
        <button
          onClick={() => setSidebarOpen(!sidebarOpen)}
          className="lg:hidden p-2 hover:bg-muted rounded-lg"
        >
          <Menu className="w-5 h-5" />
        </button>
        <h1 className="text-xl font-bold text-primary">DS Journey</h1>
      </div>
      
      <div className="flex items-center gap-4">
        {user && (
          <>
            <div className="text-sm text-muted-foreground">
              <p className="font-medium text-foreground">{user.full_name || user.username}</p>
              <p className="text-xs">{user.email}</p>
            </div>
            <div className="flex items-center gap-2">
              <Link
                to="/settings"
                className="p-2 hover:bg-muted rounded-lg transition"
                title="Settings"
              >
                <Settings className="w-5 h-5" />
              </Link>
              <button
                onClick={logout}
                className="p-2 hover:bg-muted rounded-lg transition text-red-500"
                title="Logout"
              >
                <LogOut className="w-5 h-5" />
              </button>
            </div>
          </>
        )}
      </div>
    </nav>
  )
}
