from fastapi import APIRouter

from app.core.config import get_settings
from app.models.schemas import IngestRequest, IngestResponse
from app.services.vector_service import vector_service

router = APIRouter(prefix="/knowledge", tags=["knowledge"])


@router.post("/ingest", response_model=IngestResponse)
def ingest_documents(request: IngestRequest) -> IngestResponse:
    ingested_count = vector_service.ingest_documents(request.documents)
    settings = get_settings()
    return IngestResponse(
        collection_name=settings.chroma_collection_name,
        ingested_count=ingested_count,
    )
