import { useState, useEffect } from 'react'
import { analyticsApi } from '../services/api'
import { BarChart, Bar, PieChart, Pie, Cell, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

export default function AnalyticsPage() {
  const [overviewData, setOverviewData] = useState<any>(null)
  const [chartData, setChartData] = useState<any[]>([])
  const [moduleData, setModuleData] = useState<any[]>([])
  const [isLoading, setIsLoading] = useState(true)

  const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']

  useEffect(() => {
    loadAnalyticsData()
  }, [])

  const loadAnalyticsData = async () => {
    try {
      const [overview, hours, modules] = await Promise.all([
        analyticsApi.getOverview(),
        analyticsApi.getStudyHoursOverTime(30),
        analyticsApi.getStudyHoursByModule(),
      ])

      setOverviewData(overview.data)
      setChartData(hours.data)
      setModuleData(modules.data)
    } catch (error) {
      console.error('Failed to load analytics:', error)
    } finally {
      setIsLoading(false)
    }
  }

  if (isLoading || !overviewData) {
    return <div className="p-8 text-center">Loading analytics...</div>
  }

  return (
    <div className="p-4 md:p-8 space-y-8">
      <div>
        <h1 className="text-3xl font-bold mb-2">Learning Analytics</h1>
        <p className="text-muted-foreground">Detailed insights into your learning progress</p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-card rounded-lg p-6 border border-border">
          <p className="text-muted-foreground text-sm mb-2">Total Study Hours</p>
          <p className="text-3xl font-bold text-primary">{overviewData.total_study_hours}</p>
        </div>
        <div className="bg-card rounded-lg p-6 border border-border">
          <p className="text-muted-foreground text-sm mb-2">Avg. Session Duration</p>
          <p className="text-3xl font-bold text-primary">{Math.round(overviewData.average_session_duration)}m</p>
        </div>
        <div className="bg-card rounded-lg p-6 border border-border">
          <p className="text-muted-foreground text-sm mb-2">Current Streak</p>
          <p className="text-3xl font-bold text-primary">{overviewData.current_streak}</p>
          <p className="text-xs text-muted-foreground">days</p>
        </div>
        <div className="bg-card rounded-lg p-6 border border-border">
          <p className="text-muted-foreground text-sm mb-2">Longest Streak</p>
          <p className="text-3xl font-bold text-primary">{overviewData.longest_streak}</p>
          <p className="text-xs text-muted-foreground">days</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Study Hours Over Time */}
        {chartData.length > 0 && (
          <div className="bg-card rounded-lg p-6 border border-border">
            <h2 className="text-lg font-semibold mb-4">Study Hours Over Time</h2>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                <XAxis dataKey="date" tick={{ fontSize: 12 }} />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip />
                <Line type="monotone" dataKey="hours" stroke="var(--primary)" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Topic Status Distribution */}
        {overviewData.topic_status_distribution.length > 0 && (
          <div className="bg-card rounded-lg p-6 border border-border">
            <h2 className="text-lg font-semibold mb-4">Topic Status</h2>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={overviewData.topic_status_distribution}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, value }) => `${name}: ${value}`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="count"
                >
                  {overviewData.topic_status_distribution.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Study Hours by Module */}
        {moduleData.length > 0 && (
          <div className="bg-card rounded-lg p-6 border border-border col-span-full">
            <h2 className="text-lg font-semibold mb-4">Study Hours by Module</h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={moduleData}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                <XAxis dataKey="module_name" tick={{ fontSize: 12 }} angle={-45} textAnchor="end" height={100} />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip />
                <Bar dataKey="hours" fill="var(--primary)" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>

      {/* Module Progress Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {overviewData.modules_progress.map((module: any, idx: number) => (
          <div key={idx} className="bg-card rounded-lg p-6 border border-border">
            <h3 className="font-semibold mb-2">{module.module_name}</h3>
            <div className="space-y-2">
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">Progress</span>
                <span className="font-bold text-primary">{Math.round(module.progress)}%</span>
              </div>
              <div className="w-full bg-muted rounded-full h-2">
                <div
                  className="bg-primary rounded-full h-2 transition-all"
                  style={{ width: `${module.progress}%` }}
                />
              </div>
              <div className="text-xs text-muted-foreground pt-2">
                {module.completed_topics} of {module.total_topics} topics
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
