import { useParams } from 'react-router-dom'
import { useAppStore } from '../store/appStore'
import { useState, useEffect } from 'react'
import { topicsApi, studySessionsApi } from '../services/api'
import { ChevronDown, ChevronUp, Plus, Clock } from 'lucide-react'

export default function TopicDetailsPage() {
  const { topicId } = useParams<{ topicId: string }>()
  const { topics, updateTopic } = useAppStore()
  const [topic, setTopic] = useState<any>(null)
  const [subtopics, setSubtopics] = useState<any[]>([])
  const [sessions, setSessions] = useState<any[]>([])
  const [showAddSession, setShowAddSession] = useState(false)
  const [expandedSections, setExpandedSections] = useState({
    checklist: true,
    subtopics: true,
    sessions: true,
  })

  useEffect(() => {
    if (topicId) {
      loadTopicData()
    }
  }, [topicId])

  const loadTopicData = async () => {
    try {
      const topicData = topics.find((t) => t.id === parseInt(topicId!))
      if (topicData) {
        setTopic(topicData)
        
        const [subtopicsRes, sessionsRes] = await Promise.all([
          topicsApi.getSubtopics(parseInt(topicId!)),
          topicsApi.getStudySessions(parseInt(topicId!)),
        ])
        
        setSubtopics(subtopicsRes.data)
        setSessions(sessionsRes.data)
      }
    } catch (error) {
      console.error('Failed to load topic data:', error)
    }
  }

  if (!topic) {
    return <div className="p-8 text-center">Loading...</div>
  }

  const checklist = [
    { label: 'Understand theory', completed: topic.progress > 10 },
    { label: 'Watch/read learning material', completed: topic.progress > 25 },
    { label: 'Take notes', completed: topic.progress > 40 },
    { label: 'Practice examples', completed: topic.progress > 50 },
    { label: 'Solve exercises', completed: topic.progress > 60 },
    { label: 'Write code independently', completed: topic.progress > 75 },
    { label: 'Apply to a dataset', completed: topic.progress > 85 },
    { label: 'Use in a project', completed: topic.progress > 90 },
    { label: 'Revise', completed: topic.status === 'MASTERED' },
  ]

  return (
    <div className="p-4 md:p-8 space-y-8 max-w-4xl">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold mb-4">{topic.title}</h1>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div className="bg-card rounded-lg p-4 border border-border">
            <p className="text-xs text-muted-foreground mb-1">Status</p>
            <p className="font-semibold">{topic.status}</p>
          </div>
          <div className="bg-card rounded-lg p-4 border border-border">
            <p className="text-xs text-muted-foreground mb-1">Progress</p>
            <p className="font-semibold">{Math.round(topic.progress)}%</p>
          </div>
          <div className="bg-card rounded-lg p-4 border border-border">
            <p className="text-xs text-muted-foreground mb-1">Confidence</p>
            <p className="font-semibold">{'⭐'.repeat(topic.confidence)}{'☆'.repeat(5 - topic.confidence)}</p>
          </div>
          <div className="bg-card rounded-lg p-4 border border-border">
            <p className="text-xs text-muted-foreground mb-1">Study Time</p>
            <p className="font-semibold">{Math.round(topic.actual_hours)}h / {topic.estimated_hours}h</p>
          </div>
        </div>
      </div>

      {/* Learning Checklist */}
      <div className="bg-card rounded-lg border border-border overflow-hidden">
        <button
          onClick={() => setExpandedSections(prev => ({...prev, checklist: !prev.checklist}))}
          className="w-full p-6 hover:bg-muted/50 transition flex items-center justify-between"
        >
          <h2 className="text-lg font-semibold">Learning Checklist</h2>
          {expandedSections.checklist ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
        </button>
        
        {expandedSections.checklist && (
          <div className="border-t border-border p-6 space-y-3 bg-muted/50">
            {checklist.map((item, idx) => (
              <label key={idx} className="flex items-center gap-3 cursor-pointer">
                <input
                  type="checkbox"
                  checked={item.completed}
                  readOnly
                  className="w-5 h-5 rounded border-border"
                />
                <span className={item.completed ? 'line-through text-muted-foreground' : 'font-medium'}>
                  {item.label}
                </span>
              </label>
            ))}
          </div>
        )}
      </div>

      {/* Subtopics */}
      {subtopics.length > 0 && (
        <div className="bg-card rounded-lg border border-border overflow-hidden">
          <button
            onClick={() => setExpandedSections(prev => ({...prev, subtopics: !prev.subtopics}))}
            className="w-full p-6 hover:bg-muted/50 transition flex items-center justify-between"
          >
            <h2 className="text-lg font-semibold">Subtopics ({subtopics.length})</h2>
            {expandedSections.subtopics ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
          </button>
          
          {expandedSections.subtopics && (
            <div className="border-t border-border p-6 space-y-4 bg-muted/50">
              {subtopics.map((subtopic) => (
                <div key={subtopic.id} className="p-4 bg-background rounded-lg border border-border">
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="font-semibold">{subtopic.title}</h3>
                    <span className="text-xs font-medium px-2 py-1 bg-primary/10 text-primary rounded">
                      {subtopic.status}
                    </span>
                  </div>
                  <div className="w-full bg-muted rounded-full h-2">
                    <div
                      className="bg-primary rounded-full h-2"
                      style={{ width: `${subtopic.progress}%` }}
                    />
                  </div>
                  <div className="text-xs text-muted-foreground mt-2">
                    Progress: {Math.round(subtopic.progress)}% | Confidence: {subtopic.confidence}/5
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Study Sessions */}
      <div className="bg-card rounded-lg border border-border overflow-hidden">
        <button
          onClick={() => setExpandedSections(prev => ({...prev, sessions: !prev.sessions}))}
          className="w-full p-6 hover:bg-muted/50 transition flex items-center justify-between"
        >
          <h2 className="text-lg font-semibold">Study Sessions ({sessions.length})</h2>
          {expandedSections.sessions ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
        </button>
        
        {expandedSections.sessions && (
          <div className="border-t border-border p-6 space-y-4 bg-muted/50">
            {sessions.length > 0 ? (
              sessions.map((session) => (
                <div key={session.id} className="p-4 bg-background rounded-lg border border-border">
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-medium">{new Date(session.date).toLocaleDateString()}</span>
                    <div className="flex items-center gap-2 text-sm text-muted-foreground">
                      <Clock className="w-4 h-4" />
                      <span>{session.duration_minutes}m</span>
                    </div>
                  </div>
                  {session.what_learned && (
                    <p className="text-sm text-foreground mb-1"><strong>Learned:</strong> {session.what_learned}</p>
                  )}
                  <div className="flex items-center gap-4 text-xs text-muted-foreground">
                    <span>Confidence: {session.confidence_before} → {session.confidence_after}</span>
                    <span>Difficulty: {session.difficulty}/5</span>
                  </div>
                </div>
              ))
            ) : (
              <p className="text-center text-muted-foreground py-4">No study sessions yet</p>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
