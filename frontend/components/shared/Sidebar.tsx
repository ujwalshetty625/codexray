"use client"

import { useState } from "react"
import { useDashboardStore } from "@/store/dashboardStore"
import {
  LayoutDashboard,
  GitBranch,
  FolderTree,
  Building2,
  MessageSquareCode,
  ChevronLeft,
  Zap,
} from "lucide-react"

const navItems = [
  { id: "overview",     label: "Overview",     icon: LayoutDashboard },
  { id: "graph",        label: "Graph",        icon: GitBranch },
  { id: "files",        label: "Files",        icon: FolderTree },
  { id: "architecture", label: "Architecture", icon: Building2 },
  { id: "review",       label: "Review",       icon: MessageSquareCode },
] as const

export function Sidebar() {
  const [collapsed, setCollapsed] = useState(false)
  const { activePanel, setActivePanel } = useDashboardStore()

  return (
    <aside className={`
      flex flex-col bg-[#0d1117] border-r border-white/5 transition-all duration-300
      ${collapsed ? "w-16" : "w-56"}
    `}>
      <div className="flex items-center justify-between px-4 py-5 border-b border-white/5">
        {!collapsed && (
          <div className="flex items-center gap-2">
            <Zap size={16} className="text-blue-400" />
            <span className="text-sm font-mono font-semibold text-white tracking-wider">CODEXRAY</span>
          </div>
        )}
        <button
          onClick={() => setCollapsed(p => !p)}
          className="text-zinc-500 hover:text-white transition-colors ml-auto"
        >
          <ChevronLeft size={16} className={`transition-transform duration-300 ${collapsed ? "rotate-180" : ""}`} />
        </button>
      </div>

      <nav className="flex flex-col gap-1 p-2 flex-1">
        {navItems.map(({ id, label, icon: Icon }) => (
          <button
            key={id}
            onClick={() => setActivePanel(id)}
            className={`
              flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-all duration-150
              ${activePanel === id
                ? "bg-blue-600/20 text-blue-400 border border-blue-500/20"
                : "text-zinc-500 hover:text-zinc-200 hover:bg-white/5"
              }
            `}
          >
            <Icon size={16} className="shrink-0" />
            {!collapsed && <span className="font-medium">{label}</span>}
          </button>
        ))}
      </nav>
    </aside>
  )
}