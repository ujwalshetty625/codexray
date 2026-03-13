import { create } from "zustand"
import type { FileRecord, ArchitectureResult } from "@/types/repo"
import type { DependencyGraph } from "@/types/graph"

export interface EngineeringReview {
  summary:     string
  strengths:   string[]
  weaknesses:  string[]
  suggestions: string[]
}

interface DashboardState {
  files:        FileRecord[]
  graph:        DependencyGraph | null
  architecture: ArchitectureResult | null
  review:       EngineeringReview | null
  selectedFile: string | null
  activePanel:  "overview" | "graph" | "files" | "architecture" | "review"

  setFiles:        (files: FileRecord[]) => void
  setGraph:        (graph: DependencyGraph) => void
  setArchitecture: (arch: ArchitectureResult) => void
  setReview:       (review: EngineeringReview) => void
  setSelectedFile: (path: string | null) => void
  setActivePanel:  (panel: DashboardState["activePanel"]) => void
}

export const useDashboardStore = create<DashboardState>(set => ({
  files:        [],
  graph:        null,
  architecture: null,
  review:       null,
  selectedFile: null,
  activePanel:  "overview",

  setFiles:        files        => set({ files }),
  setGraph:        graph        => set({ graph }),
  setArchitecture: architecture => set({ architecture }),
  setReview:       review       => set({ review }),
  setSelectedFile: selectedFile => set({ selectedFile }),
  setActivePanel:  activePanel  => set({ activePanel }),
}))