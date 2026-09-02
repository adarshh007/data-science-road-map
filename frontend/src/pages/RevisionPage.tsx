import { useState, useEffect } from 'react'
import { revisionsApi } from '../services/api'
import { AlertCircle, CheckCircle, Clock } from 'lucide-react'

export default function RevisionPage() {
  const [revisions, setRevisions] = useState<any[]>([])
  const [filter, setFilter] = useState<'all' | 'pending' | 'overdue' | 'completed'>('pending')
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    loadRevisions()
  }, [filter])

  const loadRevisions = async () => {
    try {
      let response
      if (filter === 'all') {
        response = await revisionsApi.getAll()
      } else {
        response = await revisionsApi.getDue(filter)
      }
      setRevisions(response.data)
    } catch (error) {
      console.error('Failed to load revisions:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleCompleteRevision = async (revisionId: number) => {
    try {
      await revisionsApi.update(revisionId, {
        is_completed: true,
        completed_date: new Date().toISOString(),
      })
      loadRevisions()
    } catch (error) {
      console.error('Failed to complete revision:', error)
    }
  }

  const handleSnoozeRevision = async (revisionId: number, days: number) => {
    try {
      await revisionsApi.snooze(revisionId, days)
      loadRevisions()
    } catch (error) {
      console.error('Failed to snooze revision:', error)
    }
  }

  const isOverdue = (dueDate: string) => new Date(dueDate) < new Date()

  return (
    <div className="p-4 md:p-8 space-y-8">
      <div>
        <h1 className="text-3xl font-bold mb-2">Revision Manager</h1>
        <p className="text-muted-foreground">Stay on top of your revisions</p>
      </div>

      {/* Filters */}
      <div className="flex gap-2 overflow-x-auto pb-2">
        {(['all', 'pending', 'overdue', 'completed'] as const).map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={`px-4 py-2 rounded-lg font-medium whitespace-nowrap transition ${
              filter === f
                ? 'bg-primary text-primary-foreground'
                : 'bg-card border border-border hover:bg-muted'
            }`}
          >
            {f.charAt(0).toUpperCase() + f.slice(1)}
          </button>
        ))}
      </div>

      {/* Revisions List */}
      <div className="space-y-4">
        {isLoading ? (
          <div className="text-center py-8">Loading revisions...</div>
        ) : revisions.length > 0 ? (
          revisions.map((revision) => {
            const overdue = isOverdue(revision.due_date)
            const icon = revision.is_completed ? (
              <CheckCircle className="w-6 h-6 text-green-500" />
            ) : overdue ? (
              <AlertCircle className="w-6 h-6 text-red-500" />
            ) : (
              <Clock className="w-6 h-6 text-yellow-500" />
            )

            return (
              <div
                key={revision.id}
                className={`bg-card rounded-lg p-6 border border-border flex items-start justify-between ${
                  revision.is_completed ? 'opacity-60' : ''
                }`}
              >
                <div className="flex gap-4 flex-1">
                  {icon}
                  <div className="flex-1">
                    <h3 className="font-semibold mb-1">Revision #{revision.revision_number}</h3>
                    <p className="text-sm text-muted-foreground mb-3">
                      Due: {new Date(revision.due_date).toLocaleDateString()}
                      {overdue && !revision.is_completed && ' (Overdue)'}
                    </p>
                    {revision.notes && (
                      <p className="text-sm text-foreground">{revision.notes}</p>
                    )}
                  </div>
                </div>

                {!revision.is_completed && (
                  <div className="flex gap-2 ml-4 flex-shrink-0">
                    <button
                      onClick={() => handleCompleteRevision(revision.id)}
                      className="px-3 py-2 bg-green-500 text-white rounded-lg text-sm font-medium hover:bg-green-600 transition"
                    >
                      Mark Done
                    </button>
                    <button
                      onClick={() => handleSnoozeRevision(revision.id, 7)}
                      className="px-3 py-2 bg-muted text-foreground rounded-lg text-sm font-medium hover:bg-muted/80 transition"
                    >
                      Snooze
                    </button>
                  </div>
                )}
              </div>
            )
          })
        ) : (
          <div className="text-center py-12 bg-card rounded-lg border border-border">
            <p className="text-muted-foreground">No revisions found</p>
          </div>
        )}
      </div>
    </div>
  )
}
