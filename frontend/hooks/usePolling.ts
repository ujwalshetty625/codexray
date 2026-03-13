import { useEffect, useRef, useCallback } from "react"
import { POLL_INTERVAL_MS, POLL_MAX_ATTEMPTS } from "@/lib/constants"

interface UsePollingOptions<T> {
  fn: () => Promise<T>
  condition: (result: T) => boolean
  onSuccess: (result: T) => void
  onFailure?: () => void
  enabled: boolean
}

export function usePolling<T>({
  fn,
  condition,
  onSuccess,
  onFailure,
  enabled,
}: UsePollingOptions<T>) {
  const attempts = useRef(0)
  const timer = useRef<NodeJS.Timeout | null>(null)

  const stop = useCallback(() => {
    if (timer.current) clearInterval(timer.current)
  }, [])

  useEffect(() => {
    if (!enabled) return

    attempts.current = 0

    timer.current = setInterval(async () => {
      attempts.current++

      if (attempts.current > POLL_MAX_ATTEMPTS) {
        stop()
        onFailure?.()
        return
      }

      try {
        const result = await fn()
        if (condition(result)) {
          stop()
          onSuccess(result)
        }
      } catch {
        stop()
        onFailure?.()
      }
    }, POLL_INTERVAL_MS)

    return stop
  }, [enabled])
}