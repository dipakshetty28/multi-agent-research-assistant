import { useMemo, useState } from 'react'
import ReportView from './components/ReportView'
import SectionCard from './components/SectionCard'
import { generateReport, ingestDocuments, type ReportResponse } from './lib/api'

const SAMPLE_DOCUMENT = `Artificial intelligence coding assistants are increasingly adopted by mid-size B2B software teams. Teams value faster boilerplate generation, code explanation, onboarding acceleration, and documentation support. Key concerns include security, hallucinated code, weak repo context, and limited governance. Buyers increasingly prefer tools that integrate with source control, issue trackers, and internal documentation. Pricing pressure is rising as foundation model access becomes cheaper.`

export default function App() {
  const [query, setQuery] = useState('Analyze the AI coding assistant market for mid-size B2B teams.')
  const [report, setReport] = useState<ReportResponse | null>(null)
  const [status, setStatus] = useState('Ready')
  const [isLoading, setIsLoading] = useState(false)

  const sampleDocuments = useMemo(
    () => [
      {
        id: 'sample-doc-1',
        title: 'AI Coding Assistant Market Note',
        text: SAMPLE_DOCUMENT,
        metadata: { source: 'sample_seed' },
      },
    ],
    [],
  )

  const handleSeed = async () => {
    try {
      setStatus('Ingesting sample knowledge...')
      await ingestDocuments(sampleDocuments)
      setStatus('Sample knowledge ingested.')
    } catch (error) {
      setStatus(error instanceof Error ? error.message : 'Failed to ingest data')
    }
  }

  const handleGenerate = async () => {
    try {
      setIsLoading(true)
      setStatus('Running researcher, writer, and editor agents...')
      const result = await generateReport({ query, top_k: 6, use_cache: true })
      setReport(result)
      setStatus(result.cached ? 'Loaded cached report.' : 'Generated new report.')
    } catch (error) {
      setStatus(error instanceof Error ? error.message : 'Failed to generate report')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <main className="page-shell">
      <header className="hero">
        <div>
          <p className="eyebrow">LangGraph + RAG + FastAPI</p>
          <h1>Multi-Agent Research Assistant</h1>
          <p className="hero-copy">
            A production-style starter app for structured report generation using researcher, writer, and editor agents.
          </p>
        </div>
      </header>

      <div className="grid two-col">
        <SectionCard title="1. Seed Knowledge" subtitle="Load demo content into the vector database">
          <button className="primary-button" onClick={handleSeed}>Ingest Sample Document</button>
        </SectionCard>

        <SectionCard title="2. Run Research" subtitle="Generate a structured report with caching">
          <label className="label" htmlFor="query">Research query</label>
          <textarea
            id="query"
            className="textarea"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            rows={5}
          />
          <button className="primary-button" onClick={handleGenerate} disabled={isLoading}>
            {isLoading ? 'Generating...' : 'Generate Report'}
          </button>
        </SectionCard>
      </div>

      <SectionCard title="System Status">
        <p>{status}</p>
      </SectionCard>

      {report ? <ReportView report={report} /> : null}
    </main>
  )
}
