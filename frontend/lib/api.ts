import axios from "axios"
import type { Repository, JobStatus, RepoStructure, RepoDependencies, RepoArchitecture } from "@/types/repo"
import type { DependencyGraph } from "@/types/graph"
import type { EngineeringReview } from "@/store/dashboardStore"

const client = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000",
  headers: { "Content-Type": "application/json" },
})

export const api = {
  analyze:      (repo_url: string): Promise<Repository> =>
    client.post("/repos/analyze", { repo_url }).then(r => r.data),

  status:       (repo_id: string): Promise<JobStatus> =>
    client.get(`/repos/${repo_id}/status`).then(r => r.data),

  structure:    (repo_id: string): Promise<RepoStructure> =>
    client.get(`/repos/${repo_id}/structure`).then(r => r.data),

  dependencies: (repo_id: string): Promise<RepoDependencies> =>
    client.get(`/repos/${repo_id}/dependencies`).then(r => r.data),

  graph:        (repo_id: string): Promise<DependencyGraph> =>
    client.get(`/repos/${repo_id}/graph`).then(r => r.data),

  architecture: (repo_id: string): Promise<RepoArchitecture> =>
    client.get(`/repos/${repo_id}/architecture`).then(r => r.data),

  review:       (repo_id: string): Promise<EngineeringReview> =>
    client.get(`/repos/${repo_id}/review`).then(r => r.data),
}