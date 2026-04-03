from __future__ import annotations

from typing import List, TypedDict

from langgraph.graph import END, START, StateGraph

from app.models.schemas import RetrievedChunk
from app.services.llm_service import llm_service
from app.services.vector_service import vector_service


class GraphState(TypedDict, total=False):
    query: str
    top_k: int
    retrieved_chunks: List[RetrievedChunk]
    findings: List[str]
    draft: str
    final_report: str


def researcher_node(state: GraphState) -> GraphState:
    query = state["query"]
    top_k = state.get("top_k", 6)
    chunks = vector_service.search(query=query, top_k=top_k)

    context = "\n\n".join(
        [f"Source: {chunk.title}\nMetadata: {chunk.metadata}\nContent: {chunk.text}" for chunk in chunks]
    )

    prompt = f"""
You are a senior researcher.

User query:
{query}

Retrieved context:
{context}

Task:
- extract the strongest evidence
- list 5 to 8 concrete findings
- be factual and concise
- if context is weak, say what is missing

Return plain text with one finding per line.
""".strip()

    response = llm_service.chat_model.invoke(prompt)
    findings = [line.strip("- ").strip() for line in response.content.splitlines() if line.strip()]

    return {
        "retrieved_chunks": chunks,
        "findings": findings,
    }


def writer_node(state: GraphState) -> GraphState:
    query = state["query"]
    findings = state.get("findings", [])

    prompt = f"""
You are a report writer.

Write a structured research report for this query:
{query}

Use these findings:
{chr(10).join(f'- {item}' for item in findings)}

Required sections:
1. Executive Summary
2. Key Findings
3. Analysis
4. Risks / Gaps
5. Recommended Next Steps

Keep the writing professional and clear.
""".strip()

    response = llm_service.chat_model.invoke(prompt)
    return {"draft": response.content}


def editor_node(state: GraphState) -> GraphState:
    draft = state.get("draft", "")

    prompt = f"""
You are a careful editor.

Improve the draft below:
- remove repetition
- tighten language
- keep claims grounded
- improve formatting
- keep it suitable for a product demo or enterprise starter system

Draft:
{draft}
""".strip()

    response = llm_service.chat_model.invoke(prompt)
    return {"final_report": response.content}


def build_graph():
    graph = StateGraph(GraphState)
    graph.add_node("researcher", researcher_node)
    graph.add_node("writer", writer_node)
    graph.add_node("editor", editor_node)
    graph.add_edge(START, "researcher")
    graph.add_edge("researcher", "writer")
    graph.add_edge("writer", "editor")
    graph.add_edge("editor", END)
    return graph.compile()


research_graph = build_graph()
