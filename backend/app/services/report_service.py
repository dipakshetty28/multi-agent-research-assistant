from typing import Dict

from app.graphs.research_graph import research_graph
from app.models.schemas import ReportRequest, ReportResponse
from app.services.cache_service import FileCacheService
from app.core.config import get_settings


class ReportService:
    def __init__(self) -> None:
        settings = get_settings()
        self.cache = FileCacheService(settings.cache_directory)

    def generate_report(self, request: ReportRequest) -> ReportResponse:
        cache_payload = {
            "query": request.query,
            "top_k": request.top_k,
        }
        cache_key = self.cache.build_key(cache_payload)

        if request.use_cache:
            cached = self.cache.get(cache_key)
            if cached:
                return ReportResponse(**cached, cached=True)

        result: Dict = research_graph.invoke(
            {
                "query": request.query,
                "top_k": request.top_k,
            }
        )

        response_payload = {
            "query": request.query,
            "cached": False,
            "draft": result.get("draft", ""),
            "final_report": result.get("final_report", ""),
            "findings": result.get("findings", []),
            "retrieved_chunks": [chunk.model_dump() for chunk in result.get("retrieved_chunks", [])],
        }
        self.cache.set(cache_key, response_payload)
        return ReportResponse(**response_payload)


report_service = ReportService()
