import { useState, useEffect } from 'react'
import { studySessionsApi } from '../services/api'
import { Clock, Calendar } from 'lucide-react'

export default function StudyLogPage() {
  const [sessions, setSessions] = useState<any[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [filter, setFilter] = useState<'all' | 'week' | 'month'>('all')

  useEffect(() => {
    loadSessions()
  }, [filter])

  const loadSessions = async () => {
    try {
      let params = {}
      const now = new Date()
      
      if (filter === 'week') {
        const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000)
        params = { start_date: weekAgo.toISOString(), end_date: now.toISOString() }
      } else if (filter === 'month') {
        const monthAgo = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000)
        params = { start_date: monthAgo.toISOString(), end_date: now.toISOString() }
      }

      const response = await studySessionsApi.getAll()
      setSessions(response.data)
    } catch (error) {
      console.error('Failed to load sessions:', error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="p-4 md:p-8 space-y-8">
      <div>
        <h1 className="text-3xl font-bold mb-2">Study Log</h1>
        <p className="text-muted-foreground">Track all your study sessions</p>
      </div>

      {/* Filters */}
      <div className="flex gap-2">
        {(['all', 'week', 'month'] as const).map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={`px-4 py-2 rounded-lg font-medium transition ${
              filter === f
                ? 'bg-primary text-primary-foreground'
                : 'bg-card border border-border hover:bg-muted'
            }`}
          >
            {f.charAt(0).toUpperCase() + f.slice(1)}
          </button>
        ))}
      </div>

      {/* Sessions List */}
      <div className="space-y-4">
        {isLoading ? (
          <div className="text-center py-8">Loading...</div>
        ) : sessions.length > 0 ? (
          sessions.map((session) => (
            <div key={session.id} className="bg-card rounded-lg p-6 border border-border">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className="font-semibold text-lg mb-1">{session.topic_id}</h3>
                  <div className="flex items-center gap-4 text-sm text-muted-foreground">
                    <div className="flex items-center gap-2">
                      <Calendar className="w-4 h-4" />
                      {new Date(session.date).toLocaleDateString()}
                    </div>
                    <div className="flex items-center gap-2">
                      <Clock className="w-4 h-4" />
                      {session.duration_minutes} min
                    </div>
                  </div>
                </div>
                <span className="text-sm font-medium px-3 py-1 bg-primary/10 text-primary rounded">
                  {session.difficulty}/5
                </span>
              </div>
              
              {session.what_learned && (
                <div className="mb-3">
                  <p className="text-sm font-medium mb-1">What I learned:</p>
                  <p className="text-sm text-foreground">{session.what_learned}</p>
                </div>
              )}
              
              <div className="grid grid-cols-2 gap-4 text-xs text-muted-foreground">
                <div>Confidence: {session.confidence_before} → {session.confidence_after}</div>
                <div>Difficulty: {session.difficulty}/5</div>
              </div>
            </div>
          ))
        ) : (
          <div className="text-center py-12 bg-card rounded-lg border border-border">
            <p className="text-muted-foreground">No study sessions found</p>
          </div>
        )}
      </div>
    </div>
  )
}
