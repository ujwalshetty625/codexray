"use client"

import { useEffect, useState } from "react"
import { PIPELINE_STEPS } from "@/lib/constants"
import { CheckCircle2, Circle, Loader2 } from "lucide-react"

export function LoadingPipeline() {
  const [activeStep, setActiveStep] = useState(0)

  useEffect(() => {
    const interval = setInterval(() => {
      setActiveStep(s => (s < PIPELINE_STEPS.length - 1 ? s + 1 : s))
    }, 2200)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-[#080c10]">
      <div className="mb-12 text-center">
        <h2 className="text-2xl font-mono font-bold text-white mb-2">Analyzing Repository</h2>
        <p className="text-zinc-500 text-sm">Running CodeXRay pipeline</p>
      </div>

      <div className="flex flex-col gap-3 w-full max-w-sm">
        {PIPELINE_STEPS.map((step, i) => {
          const done    = i < activeStep
          const current = i === activeStep

          return (
            <div
              key={step.id}
              className={`
                flex items-center gap-4 px-5 py-3.5 rounded-xl border transition-all duration-500
                ${done    ? "border-emerald-500/20 bg-emerald-500/5" : ""}
                ${current ? "border-blue-500/30 bg-blue-500/10"      : ""}
                ${!done && !current ? "border-white/5 bg-white/2 opacity-40" : ""}
              `}
            >
              <div className="shrink-0">
                {done    && <CheckCircle2 size={16} className="text-emerald-400" />}
                {current && <Loader2     size={16} className="text-blue-400 animate-spin" />}
                {!done && !current && <Circle size={16} className="text-zinc-700" />}
              </div>
              <span className={`text-sm font-mono ${
                done ? "text-emerald-400" : current ? "text-blue-300" : "text-zinc-600"
              }`}>
                {step.label}
              </span>
            </div>
          )
        })}
      </div>
    </div>
  )
}