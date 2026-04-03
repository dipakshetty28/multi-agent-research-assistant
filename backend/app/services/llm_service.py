from functools import cached_property

from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from app.core.config import get_settings


class LLMService:
    @cached_property
    def chat_model(self) -> ChatOpenAI:
        settings = get_settings()
        return ChatOpenAI(
            api_key=settings.openai_api_key,
            model=settings.openai_chat_model,
            temperature=0.2,
        )

    @cached_property
    def embedding_model(self) -> OpenAIEmbeddings:
        settings = get_settings()
        return OpenAIEmbeddings(
            api_key=settings.openai_api_key,
            model=settings.openai_embedding_model,
        )


llm_service = LLMService()
