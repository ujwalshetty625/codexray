export interface GraphNode {
  id: string
}

export interface GraphEdge {
  source: string
  target: string
}

export interface DependencyGraph {
  repo_id: string
  nodes: GraphNode[]
  edges: GraphEdge[]
}