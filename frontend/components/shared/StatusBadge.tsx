import type { AnalysisStatus } from "@/types/repo"

const styles: Record<AnalysisStatus, string> = {
  pending:    "bg-zinc-800 text-zinc-400",
  processing: "bg-blue-900/40 text-blue-400 animate-pulse",
  completed:  "bg-emerald-900/40 text-emerald-400",
  failed:     "bg-red-900/40 text-red-400",
}

const labels: Record<AnalysisStatus, string> = {
  pending:    "Pending",
  processing: "Processing",
  completed:  "Completed",
  failed:     "Failed",
}

export function StatusBadge({ status }: { status: AnalysisStatus }) {
  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-mono font-medium ${styles[status]}`}>
      {labels[status]}
    </span>
  )
}