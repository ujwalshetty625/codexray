import { useState } from "react"
import { useRouter } from "next/navigation"
import { api } from "@/lib/api"
import { usePolling } from "./usePolling"
import type { AnalysisStatus } from "@/types/repo"

export function useRepoAnalysis() {
  const router = useRouter()
  const [repoId, setRepoId] = useState<string | null>(null)
  const [status, setStatus] = useState<AnalysisStatus | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [submitting, setSubmitting] = useState(false)

  usePolling({
    fn: () => api.status(repoId!),
    condition: r => r.status === "completed" || r.status === "failed",
    onSuccess: result => {
      if (result.status === "completed") {
        router.push(`/dashboard/${repoId}`)
      } else {
        setError("Analysis failed. Please try again.")
        setStatus("failed")
      }
    },
    onFailure: () => {
      setError("Analysis timed out. Please try again.")
      setStatus("failed")
    },
    enabled: !!repoId && status === "processing",
  })

  const submit = async (url: string) => {
    setError(null)
    setSubmitting(true)
    try {
      const res = await api.analyze(url)
      setRepoId(res.repo_id)
      setStatus("processing")
    } catch (e: any) {
      setError(e?.response?.data?.detail ?? "Failed to submit repository.")
    } finally {
      setSubmitting(false)
    }
  }

  return { submit, status, error, submitting, repoId }
}