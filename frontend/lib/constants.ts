export const POLL_INTERVAL_MS = 2500
export const POLL_MAX_ATTEMPTS = 60

export const PIPELINE_STEPS = [
  { id: "clone",    label: "Cloning repository" },
  { id: "scan",     label: "Scanning files" },
  { id: "parse",    label: "Parsing dependencies" },
  { id: "graph",    label: "Building dependency graph" },
  { id: "arch",     label: "Detecting architecture" },
] as const

export const SAMPLE_REPOS = [
  "https://github.com/pallets/flask",
  "https://github.com/encode/starlette",
  "https://github.com/tiangolo/fastapi",
]