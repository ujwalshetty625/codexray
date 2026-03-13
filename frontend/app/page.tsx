"use client"

import { useState } from "react"
import { useRepoAnalysis } from "@/hooks/useRepoAnalysis"
import { LoadingPipeline } from "@/components/shared/LoadingPipeline"
import { SAMPLE_REPOS } from "@/lib/constants"
import { Zap, ArrowRight, Github } from "lucide-react"

export default function HomePage() {
  const [url, setUrl] = useState("")
  const { submit, status, error, submitting } = useRepoAnalysis()

  if (status === "processing") return <LoadingPipeline />

  return (
    <main className="min-h-screen bg-[#080c10] flex flex-col items-center justify-center px-4">
      <div
        className="absolute inset-0 opacity-20"
        style={{
          backgroundImage: "radial-gradient(circle at 50% 0%, #1d4ed820 0%, transparent 60%)",
        }}
      />

      <div className="relative z-10 flex flex-col items-center gap-8 w-full max-w-xl">
        <div className="flex flex-col items-center gap-3 text-center">
          <div className="flex items-center gap-2 mb-2">
            <Zap size={20} className="text-blue-400" />
            <span className="text-xs font-mono tracking-[0.3em] text-zinc-500 uppercase">CodeXRay</span>
          </div>
          <h1 className="text-4xl font-mono font-bold text-white leading-tight">
            Codebase Intelligence<br />
            <span className="text-blue-400">for Engineers</span>
          </h1>
          <p className="text-zinc-500 text-sm max-w-sm">
            Paste a GitHub repository URL to analyze its architecture, dependency graph, and file structure.
          </p>
        </div>

        <div className="w-full flex flex-col gap-3">
          <div className="flex gap-2">
            <div className="flex-1 flex items-center gap-2 bg-[#0d1117] border border-white/10 rounded-xl px-4 focus-within:border-blue-500/50 transition-colors">
              <Github size={15} className="text-zinc-600 shrink-0" />
              <input
                type="text"
                value={url}
                onChange={e => setUrl(e.target.value)}
                onKeyDown={e => e.key === "Enter" && url && submit(url)}
                placeholder="https://github.com/owner/repository"
                className="flex-1 bg-transparent py-3.5 text-sm text-white placeholder-zinc-600 font-mono outline-none"
              />
            </div>
            <button
              onClick={() => url && submit(url)}
              disabled={submitting || !url}
              className="px-5 bg-blue-600 hover:bg-blue-500 disabled:opacity-40 disabled:cursor-not-allowed text-white rounded-xl transition-colors flex items-center gap-2 text-sm font-medium"
            >
              {submitting ? "..." : <><span>Analyze</span><ArrowRight size={14} /></>}
            </button>
          </div>

          {error && (
            <p className="text-red-400 text-xs font-mono px-1">{error}</p>
          )}

          <div className="flex flex-wrap gap-2">
            {SAMPLE_REPOS.map(repo => (
              <button
                key={repo}
                onClick={() => setUrl(repo)}
                className="text-xs font-mono text-zinc-600 hover:text-zinc-300 border border-white/5 hover:border-white/15 rounded-lg px-3 py-1.5 transition-all"
              >
                {repo.replace("https://github.com/", "")}
              </button>
            ))}
          </div>
        </div>
      </div>
    </main>
  )
}