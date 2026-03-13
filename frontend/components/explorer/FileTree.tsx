"use client"

import { useMemo, useState } from "react"
import { useDashboardStore } from "@/store/dashboardStore"
import { FileCode2, Folder, FolderOpen, ChevronRight } from "lucide-react"
import type { FileRecord } from "@/types/repo"

interface TreeNode {
  name: string
  path: string
  type: "file" | "dir"
  children: TreeNode[]
  file?: FileRecord
}

function buildTree(files: FileRecord[]): TreeNode[] {
  const root: TreeNode = { name: "", path: "", type: "dir", children: [] }

  for (const file of files) {
    const parts = file.path.split("/")
    let node = root

    for (let i = 0; i < parts.length; i++) {
      const part = parts[i]
      const isLast = i === parts.length - 1
      let child = node.children.find(c => c.name === part)

      if (!child) {
        child = {
          name: part,
          path: parts.slice(0, i + 1).join("/"),
          type: isLast ? "file" : "dir",
          children: [],
          file: isLast ? file : undefined,
        }
        node.children.push(child)
      }
      node = child
    }
  }

  return root.children
}

function FileDetailPanel({ file, imports, reverseDeps }: {
  file: FileRecord
  imports: string[]
  reverseDeps: string[]
}) {
  return (
    <div className="border-t border-white/5 bg-[#080c10] p-4 flex flex-col gap-4">
      <div className="flex flex-col gap-1">
        <p className="text-xs text-zinc-500 font-mono uppercase tracking-widest">File Info</p>
        <div className="grid grid-cols-2 gap-2 mt-1">
          <div className="bg-[#0d1117] rounded-lg px-3 py-2">
            <p className="text-xs text-zinc-500">Language</p>
            <p className="text-sm font-mono text-white mt-0.5">{file.language}</p>
          </div>
          <div className="bg-[#0d1117] rounded-lg px-3 py-2">
            <p className="text-xs text-zinc-500">Size</p>
            <p className="text-sm font-mono text-white mt-0.5">{(file.size / 1024).toFixed(1)} KB</p>
          </div>
        </div>
      </div>

      {imports.length > 0 && (
        <div>
          <p className="text-xs text-zinc-500 font-mono uppercase tracking-widest mb-2">
            Imports ({imports.length})
          </p>
          <div className="flex flex-col gap-1 max-h-36 overflow-y-auto">
            {imports.map((imp, i) => (
              <div key={i} className="flex items-center gap-2 text-xs font-mono text-blue-400 bg-blue-500/5 border border-blue-500/10 rounded px-2 py-1">
                <span className="text-zinc-600">→</span>
                <span className="truncate">{imp}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {reverseDeps.length > 0 && (
        <div>
          <p className="text-xs text-zinc-500 font-mono uppercase tracking-widest mb-2">
            Used by ({reverseDeps.length})
          </p>
          <div className="flex flex-col gap-1 max-h-36 overflow-y-auto">
            {reverseDeps.map((dep, i) => (
              <div key={i} className="flex items-center gap-2 text-xs font-mono text-emerald-400 bg-emerald-500/5 border border-emerald-500/10 rounded px-2 py-1">
                <span className="text-zinc-600">←</span>
                <span className="truncate">{dep}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {imports.length === 0 && reverseDeps.length === 0 && (
        <p className="text-xs text-zinc-600 font-mono">No dependency relationships found for this file.</p>
      )}
    </div>
  )
}

function TreeNodeRow({
  node,
  depth = 0,
  selectedFile,
  onSelect,
  imports,
  reverseDeps,
}: {
  node: TreeNode
  depth?: number
  selectedFile: string | null
  onSelect: (file: FileRecord) => void
  imports: string[]
  reverseDeps: string[]
}) {
  const [open, setOpen] = useState(depth < 2)
  const isSelected = selectedFile === node.path

  if (node.type === "dir") {
    return (
      <div>
        <button
          onClick={() => setOpen(p => !p)}
          className="w-full flex items-center gap-1.5 px-2 py-1 text-zinc-500 hover:text-zinc-300 transition-colors"
          style={{ paddingLeft: `${depth * 12 + 8}px` }}
        >
          <ChevronRight
            size={11}
            className={`shrink-0 transition-transform ${open ? "rotate-90" : ""}`}
          />
          {open
            ? <FolderOpen size={13} className="shrink-0 text-amber-500/70" />
            : <Folder     size={13} className="shrink-0 text-amber-500/70" />
          }
          <span className="text-xs font-mono">{node.name}</span>
        </button>
        {open && node.children.map(child => (
          <TreeNodeRow
            key={child.path}
            node={child}
            depth={depth + 1}
            selectedFile={selectedFile}
            onSelect={onSelect}
            imports={imports}
            reverseDeps={reverseDeps}
          />
        ))}
      </div>
    )
  }

  return (
    <div>
      <button
        onClick={() => node.file && onSelect(node.file)}
        className={`
          w-full flex items-center gap-2 py-1 text-left transition-colors rounded
          ${isSelected
            ? "bg-blue-600/15 text-blue-400"
            : "text-zinc-400 hover:text-zinc-200 hover:bg-white/4"
          }
        `}
        style={{ paddingLeft: `${depth * 12 + 8}px` }}
      >
        <FileCode2 size={12} className="shrink-0" />
        <span className="text-xs font-mono truncate">{node.name}</span>
      </button>

      {isSelected && node.file && (
        <FileDetailPanel
          file={node.file}
          imports={imports}
          reverseDeps={reverseDeps}
        />
      )}
    </div>
  )
}

export function FileTree() {
  const { files, graph, selectedFile, setSelectedFile, setActivePanel } = useDashboardStore()
  const tree = useMemo(() => buildTree(files), [files])

  const imports = useMemo(() => {
    if (!selectedFile || !graph) return []
    return graph.edges
      .filter(e => e.source === selectedFile)
      .map(e => e.target)
  }, [selectedFile, graph])

  const reverseDeps = useMemo(() => {
    if (!selectedFile || !graph) return []
    return graph.edges
      .filter(e => e.target === selectedFile)
      .map(e => e.source)
  }, [selectedFile, graph])

  const handleSelect = (file: FileRecord) => {
    setSelectedFile(file.path === selectedFile ? null : file.path)
    setActivePanel("files")
  }

  if (!files.length) {
    return (
      <div className="flex items-center justify-center h-48 text-zinc-600 text-sm font-mono">
        No files indexed.
      </div>
    )
  }

  return (
    <div className="bg-[#0d1117] border border-white/5 rounded-xl overflow-hidden">
      <div className="px-4 py-3 border-b border-white/5 flex items-center justify-between">
        <p className="text-xs font-mono text-zinc-500 uppercase tracking-widest">File Explorer</p>
        <p className="text-xs font-mono text-zinc-600">{files.length} files</p>
      </div>
      <div className="overflow-y-auto max-h-[680px]">
        {tree.map(node => (
          <TreeNodeRow
            key={node.path}
            node={node}
            selectedFile={selectedFile}
            onSelect={handleSelect}
            imports={imports}
            reverseDeps={reverseDeps}
          />
        ))}
      </div>
    </div>
  )
}