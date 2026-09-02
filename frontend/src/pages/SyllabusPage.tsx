import { useState } from 'react'
import { useAppStore } from '../store/appStore'
import { ChevronDown, ChevronUp } from 'lucide-react'
import TopicCard from '../components/TopicCard'

export default function SyllabusPage() {
  const { modules, topics } = useAppStore()
  const [expandedModules, setExpandedModules] = useState<number[]>([])

  const toggleModule = (moduleId: number) => {
    setExpandedModules((prev) =>
      prev.includes(moduleId)
        ? prev.filter((id) => id !== moduleId)
        : [...prev, moduleId]
    )
  }

  const getModuleTopics = (moduleId: number) => {
    return topics.filter((t) => t.module_id === moduleId)
  }

  const getModuleProgress = (moduleId: number) => {
    const moduleTopics = getModuleTopics(moduleId)
    if (!moduleTopics.length) return 0
    const completed = moduleTopics.filter((t) => t.status === 'COMPLETED' || t.status === 'MASTERED').length
    return Math.round((completed / moduleTopics.length) * 100)
  }

  return (
    <div className="p-4 md:p-8 space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold mb-2">150-Day Syllabus</h1>
        <p className="text-muted-foreground">11 modules, 75 topics, comprehensive data science learning path</p>
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-card rounded-lg p-6 border border-border">
          <p className="text-muted-foreground text-sm mb-2">Total Modules</p>
          <p className="text-3xl font-bold text-primary">{modules.length}</p>
        </div>
        <div className="bg-card rounded-lg p-6 border border-border">
          <p className="text-muted-foreground text-sm mb-2">Total Topics</p>
          <p className="text-3xl font-bold text-primary">{topics.length}</p>
        </div>
        <div className="bg-card rounded-lg p-6 border border-border">
          <p className="text-muted-foreground text-sm mb-2">Learning Days</p>
          <p className="text-3xl font-bold text-primary">150</p>
        </div>
      </div>

      {/* Modules */}
      <div className="space-y-4">
        {modules.map((module) => {
          const isExpanded = expandedModules.includes(module.id)
          const moduleTopics = getModuleTopics(module.id)
          const progress = getModuleProgress(module.id)

          return (
            <div
              key={module.id}
              className="bg-card rounded-lg border border-border overflow-hidden"
            >
              {/* Module Header */}
              <button
                onClick={() => toggleModule(module.id)}
                className="w-full p-6 hover:bg-muted/50 transition flex items-start justify-between"
              >
                <div className="text-left flex-1">
                  <h2 className="text-lg font-semibold mb-2">{module.title}</h2>
                  <div className="flex flex-wrap items-center gap-4 text-sm text-muted-foreground">
                    <span>{moduleTopics.length} topics</span>
                    <span>Days {moduleTopics[0]?.day_start || '?'} – {moduleTopics[moduleTopics.length - 1]?.day_end || '?'}</span>
                  </div>
                  
                  {/* Progress Bar */}
                  <div className="mt-4 w-full max-w-xs">
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-xs font-medium">Progress</span>
                      <span className="text-xs font-bold text-primary">{progress}%</span>
                    </div>
                    <div className="w-full bg-muted rounded-full h-2">
                      <div
                        className="bg-primary rounded-full h-2 transition-all"
                        style={{ width: `${progress}%` }}
                      />
                    </div>
                  </div>
                </div>

                {isExpanded ? (
                  <ChevronUp className="w-6 h-6 text-muted-foreground mt-1 flex-shrink-0" />
                ) : (
                  <ChevronDown className="w-6 h-6 text-muted-foreground mt-1 flex-shrink-0" />
                )}
              </button>

              {/* Module Topics */}
              {isExpanded && (
                <div className="border-t border-border p-6 space-y-4 bg-muted/50">
                  {moduleTopics.length > 0 ? (
                    moduleTopics.map((topic) => (
                      <TopicCard key={topic.id} topic={topic} showAction={true} />
                    ))
                  ) : (
                    <p className="text-sm text-muted-foreground text-center py-8">
                      No topics available for this module
                    </p>
                  )}
                </div>
              )}
            </div>
          )
        })}
      </div>

      {/* Empty State */}
      {modules.length === 0 && (
        <div className="text-center py-12 bg-card rounded-lg border border-border">
          <p className="text-muted-foreground mb-4">No modules loaded yet</p>
          <p className="text-sm text-muted-foreground">Please refresh the page or contact support</p>
        </div>
      )}
    </div>
  )
}
