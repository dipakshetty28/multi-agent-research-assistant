from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

import chromadb
from chromadb.api.models.Collection import Collection

from app.core.config import get_settings
from app.models.schemas import DocumentIn, RetrievedChunk
from app.services.llm_service import llm_service


@dataclass
class ChunkRecord:
    chunk_id: str
    document_id: str
    title: str
    text: str
    metadata: Dict[str, Any]


class VectorService:
    def __init__(self) -> None:
        settings = get_settings()
        self.client = chromadb.PersistentClient(path=settings.chroma_persist_directory)
        self.collection: Collection = self.client.get_or_create_collection(
            name=settings.chroma_collection_name,
            metadata={"description": "Research source documents"},
        )

    @staticmethod
    def _chunk_text(text: str, chunk_size: int = 1200, overlap: int = 200) -> List[str]:
        chunks: List[str] = []
        start = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunks.append(text[start:end])
            if end == len(text):
                break
            start = max(0, end - overlap)
        return chunks

    def ingest_documents(self, documents: List[DocumentIn]) -> int:
        records: List[ChunkRecord] = []
        for doc in documents:
            for index, chunk in enumerate(self._chunk_text(doc.text)):
                chunk_id = f"{doc.id}-chunk-{index}"
                metadata = {**doc.metadata, "document_id": doc.id, "title": doc.title, "chunk_index": index}
                records.append(
                    ChunkRecord(
                        chunk_id=chunk_id,
                        document_id=doc.id,
                        title=doc.title,
                        text=chunk,
                        metadata=metadata,
                    )
                )

        if not records:
            return 0

        embeddings = llm_service.embedding_model.embed_documents([record.text for record in records])
        self.collection.upsert(
            ids=[record.chunk_id for record in records],
            documents=[record.text for record in records],
            metadatas=[record.metadata for record in records],
            embeddings=embeddings,
        )
        return len(documents)

    def search(self, query: str, top_k: int) -> List[RetrievedChunk]:
        query_embedding = llm_service.embedding_model.embed_query(query)
        result = self.collection.query(query_embeddings=[query_embedding], n_results=top_k)

        ids = result.get("ids", [[]])[0]
        documents = result.get("documents", [[]])[0]
        metadatas = result.get("metadatas", [[]])[0]
        distances = result.get("distances", [[]])[0] if result.get("distances") else [None] * len(ids)

        chunks: List[RetrievedChunk] = []
        for doc_id, text, metadata, distance in zip(ids, documents, metadatas, distances):
            safe_metadata = metadata or {}
            chunks.append(
                RetrievedChunk(
                    document_id=safe_metadata.get("document_id", doc_id),
                    title=safe_metadata.get("title", "Untitled"),
                    text=text,
                    metadata=safe_metadata,
                    score=distance,
                )
            )
        return chunks


vector_service = VectorService()
