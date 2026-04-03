export type IngestDocument = {
  id: string
  title: string
  text: string
  metadata?: Record<string, unknown>
}

export type ReportRequest = {
  query: string
  use_cache?: boolean
  top_k?: number
}

export type ReportResponse = {
  query: string
  cached: boolean
  draft: string
  final_report: string
  findings: string[]
  retrieved_chunks: Array<{
    document_id: string
    title: string
    text: string
    metadata: Record<string, unknown>
    score?: number | null
  }>
}

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'

export async function ingestDocuments(documents: IngestDocument[]) {
  const response = await fetch(`${API_BASE_URL}/knowledge/ingest`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ documents }),
  })

  if (!response.ok) {
    const errorText = await response.text()
    throw new Error(`Failed to ingest documents: ${response.status} ${errorText}`)
  }

  return response.json()
}

export async function generateReport(payload: ReportRequest): Promise<ReportResponse> {
  const response = await fetch(`${API_BASE_URL}/reports/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })

  if (!response.ok) {
    const errorText = await response.text()
    throw new Error(`Failed to generate report: ${response.status} ${errorText}`)
  }

  return response.json()
}