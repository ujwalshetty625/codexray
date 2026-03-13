"use client"

import { useEffect, useState } from "react"
import { useParams } from "next/navigation"
import { api } from "@/lib/api"
import { useDashboardStore } from "@/store/dashboardStore"
import { Sidebar } from "@/components/shared/Sidebar"
import { OverviewCards } from "@/components/dashboard/OverviewCards"
import { ArchitectureReport } from "@/components/dashboard/ArchitectureReport"
import { EngineeringReviewPanel } from "@/components/dashboard/EngineeringReviewPanel"
import { FileTree } from "@/components/explorer/FileTree"
import { GraphViewer } from "@/components/graph/GraphViewer"

export default function DashboardPage() {
  const { repo_id } = useParams<{ repo_id: string }>()
  const [loading, setLoading]   = useState(true)
  const [error, setError]       = useState<string | null>(null)

  const { activePanel, setFiles, setGraph, setArchitecture, setReview } = useDashboardStore()

  useEffect(() => {
    if (!repo_id) return

    const load = async () => {
      try {
        const [structure, graph, architecture, review] = await Promise.allSettled([
          api.structure(repo_id),
          api.graph(repo_id),
          api.architecture(repo_id),
          api.review(repo_id),
        ])

        if (structure.status === "fulfilled") setFiles(structure.value.files)
        if (graph.status === "fulfilled")     setGraph(graph.value)
        if (architecture.status === "fulfilled") setArchitecture(architecture.value.architecture)
        if (review.status === "fulfilled")    setReview(review.value)
      } catch (e: any) {
        setError(e?.response?.data?.detail ?? "Failed to load analysis data.")
      } finally {
        setLoading(false)
      }
    }

    load()
  }, [repo_id])

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-[#080c10] text-zinc-500 text-sm font-mono">
        Loading analysis...
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-[#080c10] text-red-400 text-sm font-mono">
        {error}
      </div>
    )
  }

  return (
    <div className="flex min-h-screen bg-[#080c10]">
      <Sidebar />

      <main className="flex-1 overflow-y-auto p-6 flex flex-col gap-6">
        <div>
          <p className="text-xs text-zinc-500 font-mono uppercase tracking-widest mb-1">Analysis</p>
          <h1 className="text-xl font-mono font-bold text-white">{repo_id}</h1>
        </div>

        {activePanel === "overview"      && <div className="flex flex-col gap-6"><OverviewCards /><ArchitectureReport /></div>}
        {activePanel === "graph"         && <GraphViewer />}
        {activePanel === "files"         && <FileTree />}
        {activePanel === "architecture"  && <ArchitectureReport />}
        {activePanel === "review"        && <EngineeringReviewPanel />}
      </main>
    </div>
  )
}