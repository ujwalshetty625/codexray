"use client"

import { useDashboardStore } from "@/store/dashboardStore"
import { ShieldCheck, HelpCircle } from "lucide-react"

const PATTERN_EXPLANATIONS: Record<string, string[]> = {
  MVC:            ["Model-View-Controller separation detected", "Distinct controller and view layers", "Centralized model definitions"],
  Layered:        ["Service and repository layers detected", "Clear separation between business and data logic", "Controller layer handles routing"],
  Microservices:  ["Multiple independent service directories", "Separate entrypoints per service", "Gateway or broker patterns present"],
  Monolithic:     ["Single unified application structure", "Shared utilities and core modules", "Centralized entry point"],
  Serverless:     ["Function-based handler structure", "Event-driven execution pattern", "Stateless compute modules"],
  "Event-Driven": ["Event publisher and consumer modules", "Listener-based architecture", "Async message passing patterns"],
}

const UNKNOWN_SIGNALS = [
  "Repository structure does not match standard architectural patterns",
  "May use a custom or hybrid architecture",
  "Consider reviewing the file structure manually for patterns",
]

export function ArchitectureReport() {
  const { architecture } = useDashboardStore()

  if (!architecture) {
    return (
      <div className="flex items-center justify-center h-48 text-zinc-600 text-sm font-mono">
        No architecture data available.
      </div>
    )
  }

  const isUnknown   = architecture.type === "Unknown" || architecture.confidence === 0
  const displayType = isUnknown ? "Custom Architecture" : architecture.type
  const confidence  = isUnknown ? null : architecture.confidence * 100
  const signals     = isUnknown ? UNKNOWN_SIGNALS : (PATTERN_EXPLANATIONS[architecture.type] ?? UNKNOWN_SIGNALS)

  return (
    <div className="bg-[#0d1117] border border-white/5 rounded-xl p-6 flex flex-col gap-6">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs text-zinc-500 font-mono uppercase tracking-widest mb-1">Detected Pattern</p>
          <h3 className="text-3xl font-mono font-bold text-white">{displayType}</h3>
          {isUnknown && (
            <p className="text-xs text-zinc-500 mt-1">
              No standard pattern matched. This may be a custom or hybrid structure.
            </p>
          )}
        </div>
        <div className={`w-10 h-10 rounded-xl border flex items-center justify-center ${
          isUnknown
            ? "border-zinc-700 bg-zinc-800/50"
            : "border-blue-500/20 bg-blue-500/5"
        }`}>
          {isUnknown
            ? <HelpCircle size={18} className="text-zinc-500" />
            : <ShieldCheck size={18} className="text-blue-400" />
          }
        </div>
      </div>

      {confidence !== null && (
        <div>
          <div className="flex justify-between text-xs font-mono mb-2">
            <span className="text-zinc-500">Confidence</span>
            <span className="text-white">{confidence.toFixed(1)}%</span>
          </div>
          <div className="h-2 bg-zinc-800 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-blue-600 to-blue-400 rounded-full transition-all duration-700"
              style={{ width: `${confidence}%` }}
            />
          </div>
        </div>
      )}

      <div>
        <p className="text-xs text-zinc-500 font-mono uppercase tracking-widest mb-3">
          {isUnknown ? "Analysis Notes" : "Detected Signals"}
        </p>
        <ul className="flex flex-col gap-2">
          {signals.map((signal, i) => (
            <li key={i} className="flex items-start gap-2.5 text-sm text-zinc-400">
              <span className={`mt-1.5 w-1 h-1 rounded-full shrink-0 ${isUnknown ? "bg-zinc-600" : "bg-blue-500"}`} />
              {signal}
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}