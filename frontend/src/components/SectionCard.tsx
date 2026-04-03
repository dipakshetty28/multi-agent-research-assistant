import type { ReactNode } from 'react'

type Props = {
  title: string
  subtitle?: string
  children: ReactNode
}

export default function SectionCard({ title, subtitle, children }: Props) {
  return (
    <section className="card">
      <div className="card-header">
        <h2>{title}</h2>
        {subtitle ? <p>{subtitle}</p> : null}
      </div>
      <div>{children}</div>
    </section>
  )
}
