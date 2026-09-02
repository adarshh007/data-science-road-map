import { useState, useEffect } from 'react'
import { analyticsApi, topicsApi, recommendationsApi } from '../services/api'
import { useAppStore } from '../store/appStore'
import { BarChart3, BookOpen, CheckCircle, Clock, TrendingUp, Zap } from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import ProgressCard from '../components/ProgressCard'
import TopicCard from '../components/TopicCard'

export default function DashboardPage() {
  const { modules, topics } = useAppStore()
  const [analyticsData, setAnalyticsData] = useState<any>(null)
  const [chartData, setChartData] = useState<any[]>([])
  const [recommendations, setRecommendations] = useState<any[]>([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    loadDashboardData()
  }, [])

  const loadDashboardData = async () => {
    try {
      const [analyticsRes, chartRes, recRes] = await Promise.all([
        analyticsApi.getOverview(),
        analyticsApi.getStudyHoursOverTime(30),
        recommendationsApi.getRecommendations(3),
      ])

      setAnalyticsData(analyticsRes.data)
      setChartData(chartRes.data)
      setRecommendations(recRes.data.recommendations)
    } catch (error) {
      console.error('Failed to load dashboard data:', error)
    } finally {
      setIsLoading(false)
    }
  }

  if (isLoading || !analyticsData) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-foreground">Loading dashboard...</p>
        </div>
      </div>
    )
  }

  // Calculate completion percentage
  const completionPercentage = topics.length > 0
    ? Math.round((analyticsData.completed_topics / analyticsData.total_topics) * 100)
    : 0

  // Find currently learning topic
  const currentlyLearning = topics.find(t => t.status === 'LEARNING')

  return (
    <div className="p-4 md:p-8 space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold mb-2">Welcome back!</h1>
        <p className="text-muted-foreground">Track your 150-day Data Science learning journey</p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <ProgressCard
          title="Overall Progress"
          value={completionPercentage}
          icon={<TrendingUp className="w-5 h-5" />}
          subtext={`${analyticsData.completed_topics}/${analyticsData.total_topics} topics`}
        />
        <ProgressCard
          title="Study Hours"
          value={Math.round(analyticsData.total_study_hours)}
          unit="h"
          icon={<Clock className="w-5 h-5" />}
          subtext={`${Math.round(analyticsData.average_session_duration)}m per session`}
        />
        <ProgressCard
          title="Current Streak"
          value={analyticsData.current_streak}
          unit="days"
          icon={<Zap className="w-5 h-5" />}
          subtext={`Best: ${analyticsData.longest_streak} days`}
        />
        <ProgressCard
          title="Modules"
          value={analyticsData.modules_progress.length}
          icon={<BookOpen className="w-5 h-5" />}
          subtext={`${analyticsData.modules_progress.filter((m: any) => m.progress === 100).length} complete`}
        />
      </div>

      {/* Two-column layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left column - Chart and Currently Learning */}
        <div className="lg:col-span-2 space-y-8">
          {/* Study Hours Chart */}
          {chartData.length > 0 && (
            <div className="bg-card rounded-lg p-6 border border-border">
              <h2 className="text-lg font-semibold mb-4">Study Activity (Last 30 Days)</h2>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                  <XAxis
                    dataKey="date"
                    stroke="var(--muted-foreground)"
                    tick={{ fontSize: 12 }}
                  />
                  <YAxis stroke="var(--muted-foreground)" tick={{ fontSize: 12 }} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: 'var(--card)',
                      border: '1px solid var(--border)',
                      borderRadius: '6px',
                    }}
                  />
                  <Line
                    type="monotone"
                    dataKey="hours"
                    stroke="var(--primary)"
                    strokeWidth={2}
                    dot={false}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          )}

          {/* Currently Learning */}
          {currentlyLearning && (
            <div className="bg-card rounded-lg p-6 border border-border border-primary/50 bg-primary/5">
              <h2 className="text-lg font-semibold mb-4">Currently Learning</h2>
              <TopicCard
                topic={currentlyLearning}
                showAction={true}
                actionLabel="Continue"
              />
            </div>
          )}
        </div>

        {/* Right column - Recommendations and Progress */}
        <div className="space-y-8">
          {/* Recommendations */}
          <div className="bg-card rounded-lg p-6 border border-border">
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <BarChart3 className="w-5 h-5" />
              Recommended Next
            </h2>
            <div className="space-y-4">
              {recommendations.length > 0 ? (
                recommendations.map((rec, idx) => (
                  <div key={idx} className="p-3 bg-muted rounded-lg border border-border">
                    <h3 className="font-medium text-sm">{rec.topic_name}</h3>
                    <p className="text-xs text-muted-foreground mt-1">{rec.module_name}</p>
                    <div className="mt-2 flex items-center justify-between">
                      <span className={`text-xs font-medium px-2 py-1 rounded ${
                        rec.priority === 'HIGH' ? 'bg-red-100 text-red-700' :
                        rec.priority === 'MEDIUM' ? 'bg-yellow-100 text-yellow-700' :
                        'bg-blue-100 text-blue-700'
                      }`}>
                        {rec.priority} Priority
                      </span>
                      <span className="text-xs text-muted-foreground">
                        Score: {rec.confidence_score}
                      </span>
                    </div>
                    <p className="text-xs text-muted-foreground mt-2">{rec.reason}</p>
                  </div>
                ))
              ) : (
                <p className="text-sm text-muted-foreground">No recommendations at this time</p>
              )}
            </div>
          </div>

          {/* Module Progress */}
          <div className="bg-card rounded-lg p-6 border border-border">
            <h2 className="text-lg font-semibold mb-4">Module Progress</h2>
            <div className="space-y-3">
              {analyticsData.modules_progress.map((module: any, idx: number) => (
                <div key={idx}>
                  <div className="flex items-center justify-between mb-1">
                    <p className="text-sm font-medium truncate">{module.module_name}</p>
                    <span className="text-xs font-semibold text-primary">
                      {Math.round(module.progress)}%
                    </span>
                  </div>
                  <div className="w-full bg-muted rounded-full h-2">
                    <div
                      className="bg-primary rounded-full h-2 transition-all duration-300"
                      style={{ width: `${module.progress}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
