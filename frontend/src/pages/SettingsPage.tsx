import { useState, useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { usersApi } from '../services/api'
import { Moon, Sun, Monitor } from 'lucide-react'

export default function SettingsPage() {
  const { user, logout } = useAuth()
  const [fullName, setFullName] = useState(user?.full_name || '')
  const [theme, setTheme] = useState<'light' | 'dark' | 'system'>(user?.theme as any || 'system')
  const [dailyGoal, setDailyGoal] = useState(user?.daily_goal_hours || 2)
  const [weeklyGoal, setWeeklyGoal] = useState(user?.weekly_goal_hours || 10)
  const [isSaving, setIsSaving] = useState(false)
  const [saveMessage, setSaveMessage] = useState('')

  const handleSaveSettings = async () => {
    setIsSaving(true)
    try {
      await usersApi.updateProfile({
        full_name: fullName,
        theme,
        daily_goal_hours: dailyGoal,
        weekly_goal_hours: weeklyGoal,
      })
      setSaveMessage('Settings saved successfully!')
      setTimeout(() => setSaveMessage(''), 3000)
    } catch (error) {
      setSaveMessage('Failed to save settings')
    } finally {
      setIsSaving(false)
    }
  }

  return (
    <div className="p-4 md:p-8 space-y-8 max-w-2xl">
      <div>
        <h1 className="text-3xl font-bold mb-2">Settings</h1>
        <p className="text-muted-foreground">Manage your preferences and goals</p>
      </div>

      {saveMessage && (
        <div className="bg-green-100 border border-green-300 text-green-700 px-4 py-3 rounded-lg text-sm">
          {saveMessage}
        </div>
      )}

      {/* Profile Section */}
      <div className="bg-card rounded-lg p-6 border border-border space-y-4">
        <h2 className="text-lg font-semibold">Profile</h2>
        <div>
          <label className="block text-sm font-medium mb-2">Email</label>
          <input
            type="email"
            value={user?.email || ''}
            disabled
            className="w-full px-4 py-2 border border-border rounded-lg bg-muted"
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-2">Full Name</label>
          <input
            type="text"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            placeholder="Your full name"
            className="w-full px-4 py-2 border border-border rounded-lg bg-background focus:outline-none focus:ring-2 focus:ring-primary"
          />
        </div>
      </div>

      {/* Learning Goals */}
      <div className="bg-card rounded-lg p-6 border border-border space-y-4">
        <h2 className="text-lg font-semibold">Learning Goals</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-2">Daily Goal (hours)</label>
            <input
              type="number"
              min="0.5"
              max="12"
              step="0.5"
              value={dailyGoal}
              onChange={(e) => setDailyGoal(parseFloat(e.target.value))}
              className="w-full px-4 py-2 border border-border rounded-lg bg-background focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-2">Weekly Goal (hours)</label>
            <input
              type="number"
              min="5"
              max="100"
              step="5"
              value={weeklyGoal}
              onChange={(e) => setWeeklyGoal(parseFloat(e.target.value))}
              className="w-full px-4 py-2 border border-border rounded-lg bg-background focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>
        </div>
      </div>

      {/* Theme Selection */}
      <div className="bg-card rounded-lg p-6 border border-border space-y-4">
        <h2 className="text-lg font-semibold">Appearance</h2>
        <div className="space-y-3">
          {[
            { value: 'light' as const, label: 'Light', icon: Sun },
            { value: 'dark' as const, label: 'Dark', icon: Moon },
            { value: 'system' as const, label: 'System', icon: Monitor },
          ].map((option) => {
            const Icon = option.icon
            return (
              <label key={option.value} className="flex items-center gap-3 p-3 border border-border rounded-lg hover:bg-muted cursor-pointer transition">
                <input
                  type="radio"
                  name="theme"
                  value={option.value}
                  checked={theme === option.value}
                  onChange={(e) => setTheme(e.target.value as any)}
                  className="w-4 h-4"
                />
                <Icon className="w-5 h-5 text-muted-foreground" />
                <span className="font-medium">{option.label}</span>
              </label>
            )
          })}
        </div>
      </div>

      {/* Account Section */}
      <div className="bg-card rounded-lg p-6 border border-border space-y-4">
        <h2 className="text-lg font-semibold">Account</h2>
        <p className="text-sm text-muted-foreground mb-4">
          Logged in as <strong>{user?.username}</strong>
        </p>
        <button
          onClick={logout}
          className="w-full bg-red-500 text-white py-2 rounded-lg font-medium hover:bg-red-600 transition"
        >
          Logout
        </button>
      </div>

      {/* Save Button */}
      <div className="flex gap-3">
        <button
          onClick={handleSaveSettings}
          disabled={isSaving}
          className="flex-1 bg-primary text-primary-foreground py-2 rounded-lg font-medium hover:bg-primary/90 transition disabled:opacity-50"
        >
          {isSaving ? 'Saving...' : 'Save Changes'}
        </button>
      </div>

      {/* About Section */}
      <div className="bg-muted/50 rounded-lg p-6 border border-border text-center text-sm text-muted-foreground">
        <p className="font-medium mb-2">DS Journey v1.0</p>
        <p>Your personal 150-day Data Science learning tracker</p>
      </div>
    </div>
  )
}
