from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "QueryPilot AI"
    app_version: str = "0.1.0"
    retailstar_docs_path: str = "data/retailstar_docs"
    openai_embedding_model: str
    embedding_dimensions: int
    rag_top_k: int = Field(ge=1, le=20)

    database_url: str
    openai_api_key: str
    openai_model: str

    google_api_key: str
    google_genai_use_vertexai: bool = False


    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()