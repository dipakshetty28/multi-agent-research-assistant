from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class DocumentIn(BaseModel):
    id: str
    title: str
    text: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class IngestRequest(BaseModel):
    documents: List[DocumentIn]


class IngestResponse(BaseModel):
    collection_name: str
    ingested_count: int


class ReportRequest(BaseModel):
    query: str
    use_cache: bool = True
    top_k: int = 6


class RetrievedChunk(BaseModel):
    document_id: str
    title: str
    text: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    score: Optional[float] = None


class ReportResponse(BaseModel):
    query: str
    cached: bool
    draft: str
    final_report: str
    findings: List[str]
    retrieved_chunks: List[RetrievedChunk]


class HealthResponse(BaseModel):
    status: str
    app: str
    environment: str
