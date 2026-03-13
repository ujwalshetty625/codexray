"use client"

import { useState } from "react"
import { useDashboardStore } from "@/store/dashboardStore"
import { FileCode2, GitMerge, Cpu, ChevronDown, ChevronUp, Terminal, Braces, Hash } from "lucide-react"

const LANGUAGE_ICONS: Record<string, string> = {
  Python:          "🐍",
  JavaScript:      "🟨",
  TypeScript:      "🔷",
  "C++":           "⚙️",
  C:               "⚙️",
  "C#":            "🟣",
  Java:            "☕",
  Go:              "🐹",
  Rust:            "🦀",
  Ruby:            "💎",
  PHP:             "🐘",
  Swift:           "🧡",
  Kotlin:          "🟠",
  Scala:           "🔴",
  Shell:           "💻",
  PowerShell:      "💙",
  HTML:            "🌐",
  CSS:             "🎨",
  SCSS:            "🎨",
  JSON:            "📋",
  YAML:            "📄",
  TOML:            "📄",
  Markdown:        "📝",
  SQL:             "🗄️",
  GraphQL:         "🔗",
  Dockerfile:      "🐳",
  Terraform:       "🏗️",
  R:               "📊",
  Dart:            "🎯",
  Elixir:          "💜",
  Haskell:         "🔵",
  Lua:             "🌙",
}

function getLanguageIcon(lang: string): string {
  return LANGUAGE_ICONS[lang] ?? "📄"
}

function LanguageBreakdown({ files }: { files: { language: string }[] }) {
  const counts: Record<string, number> = {}
  for (const f of files) {
    if (f.language && f.language !== "Unknown") {
      counts[f.language] = (counts[f.language] ?? 0) + 1
    }
  }

  const total = Object.values(counts).reduce((a, b) => a + b, 0)
  const sorted = Object.entries(counts).sort((a, b) => b[1] - a[1])

  return (
    <div className="mt-3 flex flex-col gap-2">
      {sorted.map(([lang, count]) => {
        const pct = total > 0 ? ((count / total) * 100).toFixed(1) : "0"
        return (
          <div key={lang} className="flex flex-col gap-1">
            <div className="flex items-center justify-between text-xs font-mono">
              <span className="flex items-center gap-1.5 text-zinc-300">
                <span>{getLanguageIcon(lang)}</span>
                {lang}
              </span>
              <span className="text-zinc-500">{count} files · {pct}%</span>
            </div>
            <div className="h-1 bg-zinc-800 rounded-full overflow-hidden">
              <div
                className="h-full bg-blue-500/60 rounded-full"
                style={{ width: `${pct}%` }}
              />
            </div>
          </div>
        )
      })}
    </div>
  )
}

export function OverviewCards() {
  const { files, graph, architecture } = useDashboardStore()
  const [showLanguages, setShowLanguages] = useState(false)

  const languages = [...new Set(
    files.map(f => f.language).filter(l => l && l !== "Unknown")
  )]

  const isUnknownArch = !architecture || architecture.type === "Unknown" || architecture.confidence === 0

  const cards = [
    {
      label:  "Architecture",
      value:  isUnknownArch ? "Custom" : (architecture?.type ?? "—"),
      sub:    isUnknownArch ? "No standard pattern matched" : `${((architecture?.confidence ?? 0) * 100).toFixed(0)}% confidence`,
      icon:   Cpu,
      accent: "blue",
    },
    {
      label:  "Files",
      value:  files.length.toLocaleString(),
      sub:    "indexed",
      icon:   FileCode2,
      accent: "violet",
    },
    {
      label:  "Dependencies",
      value:  graph?.edges.length.toLocaleString() ?? "—",
      sub:    `${graph?.nodes.length ?? 0} nodes`,
      icon:   GitMerge,
      accent: "emerald",
    },
  ]

  const accentMap: Record<string, string> = {
    blue:   "border-blue-500/20 bg-blue-500/5 text-blue-400",
    violet: "border-violet-500/20 bg-violet-500/5 text-violet-400",
    emerald:"border-emerald-500/20 bg-emerald-500/5 text-emerald-400",
  }

  return (
    <div className="flex flex-col gap-4">
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {cards.map(({ label, value, sub, icon: Icon, accent }) => (
          <div key={label} className="bg-[#0d1117] border border-white/5 rounded-xl p-5 flex flex-col gap-3">
            <div className={`w-8 h-8 rounded-lg border flex items-center justify-center ${accentMap[accent]}`}>
              <Icon size={15} />
            </div>
            <div>
              <p className="text-2xl font-mono font-bold text-white">{value}</p>
              <p className="text-xs text-zinc-500 mt-0.5">{label}</p>
              {sub && <p className="text-xs text-zinc-600 mt-1 font-mono">{sub}</p>}
            </div>
          </div>
        ))}
      </div>

      {/* Languages panel */}
      <div className="bg-[#0d1117] border border-white/5 rounded-xl p-5">
        <button
          onClick={() => setShowLanguages(p => !p)}
          className="w-full flex items-center justify-between"
        >
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg border border-amber-500/20 bg-amber-500/5 text-amber-400 flex items-center justify-center">
              <Hash size={15} />
            </div>
            <div className="text-left">
              <p className="text-2xl font-mono font-bold text-white">{languages.length}</p>
              <p className="text-xs text-zinc-500 mt-0.5">Languages</p>
              <p className="text-xs text-zinc-600 mt-1 font-mono">
                {languages.slice(0, 3).map(l => `${getLanguageIcon(l)} ${l}`).join(" · ")}
              </p>
            </div>
          </div>
          {showLanguages
            ? <ChevronUp size={15} className="text-zinc-500" />
            : <ChevronDown size={15} className="text-zinc-500" />
          }
        </button>

        {showLanguages && <LanguageBreakdown files={files} />}
      </div>
    </div>
  )
}