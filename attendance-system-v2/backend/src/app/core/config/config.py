import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Attendance System"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "a9e3884ffb6b4c9aa07d3f6d503b6424f2cb5a34db2f4c21a77d5c68a9c5b8e1"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "attendance_db"
    DATABASE_URL: Optional[str] = None

    @property
    def sqlalchemy_database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(
        env_file=os.path.join(
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")),
            ".env",
        ),
        case_sensitive=True,
    )

settings = Settings()
