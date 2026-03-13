import { useState, useCallback } from "react"

export function useGraphState() {
  const [selectedNode, setSelectedNode] = useState<string | null>(null)
  const [highlightedNodes, setHighlightedNodes] = useState<Set<string>>(new Set())

  const selectNode = useCallback((nodeId: string | null) => {
    setSelectedNode(nodeId)
    if (!nodeId) {
      setHighlightedNodes(new Set())
    }
  }, [])

  const highlightConnected = useCallback((nodeId: string, edges: { source: string; target: string }[]) => {
    const connected = new Set<string>([nodeId])
    edges.forEach(e => {
      if (e.source === nodeId) connected.add(e.target)
      if (e.target === nodeId) connected.add(e.source)
    })
    setHighlightedNodes(connected)
  }, [])

  return { selectedNode, highlightedNodes, selectNode, highlightConnected }
}