"use client"

import { useDashboardStore } from "@/store/dashboardStore"
import { ThumbsUp, ThumbsDown, Lightbulb, FileText } from "lucide-react"

interface SectionProps {
  title: string
  icon: React.ReactNode
  items: string[]
  accent: "emerald" | "red" | "blue" | "zinc"
}

const accentMap = {
  emerald: { dot: "bg-emerald-500",    card: "border-emerald-500/10 bg-emerald-500/5",  text: "text-emerald-400" },
  red:     { dot: "bg-red-500",        card: "border-red-500/10 bg-red-500/5",          text: "text-red-400"     },
  blue:    { dot: "bg-blue-500",       card: "border-blue-500/10 bg-blue-500/5",        text: "text-blue-400"    },
  zinc:    { dot: "bg-zinc-500",       card: "border-zinc-500/10 bg-zinc-800/40",       text: "text-zinc-400"    },
}

function ReviewSection({ title, icon, items, accent }: SectionProps) {
  const { dot, card, text } = accentMap[accent]

  return (
    <div className="flex flex-col gap-3">
      <div className={`flex items-center gap-2 ${text}`}>
        {icon}
        <p className="text-xs font-mono uppercase tracking-widest">{title}</p>
      </div>
      <ul className="flex flex-col gap-2">
        {items.map((item, i) => (
          <li key={i} className={`flex items-start gap-3 border rounded-xl px-4 py-3 ${card}`}>
            <span className={`mt-1.5 w-1.5 h-1.5 rounded-full shrink-0 ${dot}`} />
            <span className="text-sm text-zinc-300 leading-relaxed">{item}</span>
          </li>
        ))}
      </ul>
    </div>
  )
}

export function EngineeringReviewPanel() {
  const { review } = useDashboardStore()

  if (!review) {
    return (
      <div className="flex items-center justify-center h-48 text-zinc-600 text-sm font-mono">
        No engineering review available.
      </div>
    )
  }

  return (
    <div className="flex flex-col gap-6">
      <div className="bg-[#0d1117] border border-white/5 rounded-xl p-6">
        <div className="flex items-center gap-2 text-zinc-400 mb-3">
          <FileText size={15} />
          <p className="text-xs font-mono uppercase tracking-widest">Summary</p>
        </div>
        <p className="text-sm text-zinc-300 leading-relaxed">{review.summary}</p>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
        <ReviewSection
          title="Strengths"
          icon={<ThumbsUp size={14} />}
          items={review.strengths}
          accent="emerald"
        />
        <ReviewSection
          title="Weaknesses"
          icon={<ThumbsDown size={14} />}
          items={review.weaknesses}
          accent="red"
        />
      </div>

      <ReviewSection
        title="Suggestions"
        icon={<Lightbulb size={14} />}
        items={review.suggestions}
        accent="blue"
      />
    </div>
  )
}