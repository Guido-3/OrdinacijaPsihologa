from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./ordinacija_psihologa.db"

    class Config:
        env_file = ".env"