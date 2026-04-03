import type { ReportResponse } from '../lib/api'
import SectionCard from './SectionCard'

type Props = {
  report: ReportResponse
}

export default function ReportView({ report }: Props) {
  return (
    <div className="grid two-col">
      <SectionCard title="Final Report" subtitle={report.cached ? 'Loaded from cache' : 'Freshly generated'}>
        <pre className="report-text">{report.final_report}</pre>
      </SectionCard>

      <SectionCard title="Agent Findings" subtitle="Researcher output before drafting">
        <ul className="findings-list">
          {report.findings.map((item, index) => (
            <li key={`${index}-${item}`}>{item}</li>
          ))}
        </ul>
      </SectionCard>

      <SectionCard title="Draft" subtitle="Writer output before editing">
        <pre className="report-text">{report.draft}</pre>
      </SectionCard>

      <SectionCard title="Retrieved Chunks" subtitle="RAG context used by the researcher agent">
        <div className="chunk-list">
          {report.retrieved_chunks.map((chunk, index) => (
            <article className="chunk-card" key={`${chunk.document_id}-${index}`}>
              <strong>{chunk.title}</strong>
              <p className="chunk-meta">document_id: {chunk.document_id}</p>
              <p className="chunk-content">{chunk.text}</p>
            </article>
          ))}
        </div>
      </SectionCard>
    </div>
  )
}
