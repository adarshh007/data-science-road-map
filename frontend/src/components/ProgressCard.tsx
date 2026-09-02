interface ProgressCardProps {
  title: string
  value: number
  unit?: string
  icon: React.ReactNode
  subtext?: string
}

export default function ProgressCard({
  title,
  value,
  unit,
  icon,
  subtext,
}: ProgressCardProps) {
  return (
    <div className="bg-card rounded-lg p-6 border border-border hover:border-primary/50 transition">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-muted-foreground text-sm font-medium mb-2">{title}</p>
          <div className="flex items-baseline gap-1">
            <span className="text-3xl font-bold text-primary">{value}</span>
            {unit && <span className="text-lg text-muted-foreground">{unit}</span>}
          </div>
          {subtext && (
            <p className="text-xs text-muted-foreground mt-2">{subtext}</p>
          )}
        </div>
        <div className="p-3 bg-primary/10 rounded-lg text-primary">
          {icon}
        </div>
      </div>
    </div>
  )
}
