from functools import lru_cache
from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Multi-Agent Research Assistant"
    app_env: str = "development"
    api_v1_prefix: str = "/api/v1"
    debug: bool = True
    allowed_origins: List[str] = ["http://localhost:5173"]

    openai_api_key: str = ""
    openai_chat_model: str = "gpt-4.1-mini"
    openai_embedding_model: str = "text-embedding-3-small"

    chroma_collection_name: str = "research_documents"
    chroma_persist_directory: str = "./data/chroma"
    cache_directory: str = "./data/cache"
    max_chunks_per_query: int = 8

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_allowed_origins(cls, value):
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()