"use client"

import { useEffect, useMemo } from "react"
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
  type Node,
  type Edge,
} from "reactflow"
import "reactflow/dist/style.css"
import { useDashboardStore } from "@/store/dashboardStore"
import { useGraphState } from "@/hooks/useGraphState"

const MAX_NODES = 300

function buildFlowNodes(
  graphNodes: { id: string }[],
  highlighted: Set<string>,
  selected: string | null
): Node[] {
  return graphNodes.slice(0, MAX_NODES).map((n, i) => {
    const isSelected    = n.id === selected
    const isHighlighted = highlighted.size > 0 && highlighted.has(n.id)
    const isDimmed      = highlighted.size > 0 && !highlighted.has(n.id)

    return {
      id: n.id,
      position: { x: (i % 12) * 200, y: Math.floor(i / 12) * 110 },
      data: { label: n.id.split("/").pop() ?? n.id },
      style: {
        background:  isSelected ? "#2563eb" : isHighlighted ? "#1e3a5f" : "#0d1117",
        border:      `1px solid ${isSelected ? "#3b82f6" : isHighlighted ? "#3b82f6" : "#ffffff10"}`,
        borderRadius: "8px",
        padding:     "6px 12px",
        fontSize:    "11px",
        fontFamily:  "JetBrains Mono, monospace",
        color:       isSelected ? "#fff" : isHighlighted ? "#93c5fd" : isDimmed ? "#333" : "#a1a1aa",
        minWidth:    "120px",
        transition:  "all 0.15s",
      },
    }
  })
}

function buildFlowEdges(
  edges: { source: string; target: string }[],
  highlighted: Set<string>,
  visibleIds: Set<string>
): Edge[] {
  return edges
    .filter(e => visibleIds.has(e.source) && visibleIds.has(e.target))
    .map((e, i) => {
      const isHighlighted = highlighted.size > 0 && highlighted.has(e.source) && highlighted.has(e.target)
      return {
        id:       `e-${i}`,
        source:   e.source,
        target:   e.target,
        style:    { stroke: isHighlighted ? "#3b82f6" : "#ffffff08", strokeWidth: isHighlighted ? 2 : 1 },
        animated: isHighlighted,
      }
    })
}

export function GraphViewer() {
  const { graph, selectedFile } = useDashboardStore()
  const { selectedNode, highlightedNodes, selectNode, highlightConnected } = useGraphState()

  const [nodes, setNodes, onNodesChange] = useNodesState([])
  const [edges, setEdges, onEdgesChange] = useEdgesState([])

  const activeNode  = selectedFile ?? selectedNode
  const visibleIds  = useMemo(
    () => new Set(graph?.nodes.slice(0, MAX_NODES).map(n => n.id) ?? []),
    [graph]
  )

  // Only re-run when graph data or selection changes — not when nodes/edges change
  useEffect(() => {
    if (!graph) return
    setNodes(buildFlowNodes(graph.nodes, highlightedNodes, activeNode))
    setEdges(buildFlowEdges(graph.edges, highlightedNodes, visibleIds))
  }, [graph, highlightedNodes, activeNode, visibleIds])

  if (!graph) {
    return (
      <div className="flex items-center justify-center h-96 text-zinc-600 text-sm font-mono">
        No graph data available.
      </div>
    )
  }

  const truncated = graph.nodes.length > MAX_NODES

  return (
    <div className="flex flex-col gap-2">
      {truncated && (
        <div className="flex items-center gap-2 px-4 py-2 bg-amber-500/10 border border-amber-500/20 rounded-lg text-amber-400 text-xs font-mono">
          Showing {MAX_NODES} of {graph.nodes.length} nodes. Large graphs are truncated for performance.
        </div>
      )}
      <div className="bg-[#0d1117] border border-white/5 rounded-xl overflow-hidden" style={{ height: 600 }}>
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onNodeClick={(_, node) => {
            const next = node.id === selectedNode ? null : node.id
            selectNode(next)
            if (next) highlightConnected(next, graph.edges)
          }}
          onPaneClick={() => selectNode(null)}
          fitView
          attributionPosition="bottom-right"
        >
          <Background color="#ffffff05" gap={24} />
          <Controls className="!bg-[#0d1117] !border-white/10" />
          <MiniMap
            style={{ background: "#080c10", border: "1px solid #ffffff10" }}
            nodeColor="#1e293b"
            maskColor="rgba(0,0,0,0.6)"
          />
        </ReactFlow>
      </div>
    </div>
  )
}