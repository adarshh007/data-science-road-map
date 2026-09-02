import { Link } from 'react-router-dom'
import { CheckCircle, Circle, Clock } from 'lucide-react'

interface TopicCardProps {
  topic: any
  showAction?: boolean
  actionLabel?: string
}

export default function TopicCard({
  topic,
  showAction = false,
  actionLabel = 'View',
}: TopicCardProps) {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'COMPLETED':
      case 'MASTERED':
        return 'bg-green-100 text-green-700'
      case 'LEARNING':
      case 'PRACTICING':
        return 'bg-blue-100 text-blue-700'
      case 'NEEDS_REVISION':
        return 'bg-orange-100 text-orange-700'
      default:
        return 'bg-gray-100 text-gray-700'
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'COMPLETED':
      case 'MASTERED':
        return <CheckCircle className="w-4 h-4" />
      default:
        return <Circle className="w-4 h-4" />
    }
  }

  return (
    <div className="bg-background rounded-lg p-4 border border-border hover:border-primary/50 transition">
      <div className="flex items-start justify-between mb-3">
        <h3 className="font-semibold text-foreground">{topic.title}</h3>
        <span className={`flex items-center gap-1 text-xs font-medium px-2 py-1 rounded ${getStatusColor(topic.status)}`}>
          {getStatusIcon(topic.status)}
          {topic.status}
        </span>
      </div>

      <p className="text-sm text-muted-foreground mb-4 line-clamp-2">{topic.description}</p>

      <div className="space-y-3 mb-4">
        {/* Progress Bar */}
        <div>
          <div className="flex items-center justify-between mb-1">
            <span className="text-xs text-muted-foreground">Progress</span>
            <span className="text-xs font-semibold text-primary">{Math.round(topic.progress)}%</span>
          </div>
          <div className="w-full bg-muted rounded-full h-2">
            <div
              className="bg-primary rounded-full h-2 transition-all"
              style={{ width: `${topic.progress}%` }}
            />
          </div>
        </div>

        {/* Confidence */}
        <div className="flex items-center justify-between text-xs">
          <span className="text-muted-foreground">Confidence</span>
          <div className="flex gap-1">
            {[...Array(5)].map((_, i) => (
              <div
                key={i}
                className={`w-2 h-2 rounded-full ${i < topic.confidence ? 'bg-primary' : 'bg-muted'}`}
              />
            ))}
          </div>
        </div>

        {/* Meta info */}
        <div className="flex items-center gap-4 text-xs text-muted-foreground">
          <div className="flex items-center gap-1">
            <Clock className="w-3 h-3" />
            <span>{Math.round(topic.actual_hours)}/{topic.estimated_hours}h</span>
          </div>
          <span>Days {topic.day_start}–{topic.day_end}</span>
        </div>
      </div>

      {showAction && (
        <Link
          to={`/topics/${topic.id}`}
          className="w-full bg-primary text-primary-foreground py-2 rounded-lg text-sm font-medium hover:bg-primary/90 transition inline-block text-center"
        >
          {actionLabel}
        </Link>
      )}
    </div>
  )
}
