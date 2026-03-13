export type AnalysisStatus = "pending" | "processing" | "completed" | "failed"

export interface Repository {
  repo_id: string
  status: AnalysisStatus
}

export interface FileRecord {
  path: string
  extension: string
  language: string
  size: number
}

export interface Dependency {
  source: string
  target: string
  type: string
}

export interface ArchitectureResult {
  type: string
  confidence: number
}

export interface RepoStructure {
  repo_id: string
  files: FileRecord[]
}

export interface RepoDependencies {
  repo_id: string
  dependencies: Dependency[]
}

export interface RepoArchitecture {
  repo_id: string
  architecture: ArchitectureResult
}

export interface JobStatus {
  repo_id: string
  status: AnalysisStatus
  job_status: string | null
  started_at: string | null
  completed_at: string | null
}