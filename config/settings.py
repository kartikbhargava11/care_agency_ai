import os

class Settings:
    PROJECT_NAME: str = 'Care Agency AI'
    VERSION: str = '1.0'

    OLLAMA_URL: str = os.getenv('OLLAMA_URL', 'http://localhost:11431/api/generate')
    AI_MODEL: str = os.getenv('AI_MODEL', 'qwen2.5:1.5b')

    DATABASE_URL: str = os.getenv('DATABASE_URL', 'sqlite:///./care_agency_logs.db')

settings = Settings()