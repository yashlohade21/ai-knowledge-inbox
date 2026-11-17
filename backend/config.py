import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))


class Settings(BaseSettings):
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    hf_api_key: str = os.getenv("HF_API_KEY", "")

    llm_model: str = "qwen/qwen3.8-27b"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    chunk_size: int = 500
    chunk_overlap: int = 50
    top_k: int = 5

    chroma_persist_dir: str = os.path.join(os.path.dirname(__file__), "chroma_data")


settings = Settings()
