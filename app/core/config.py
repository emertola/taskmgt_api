from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  app_name: str = "Task API"
  debug: bool = False
  api_version: str = "v1"
  database_url: str

  class Config:
    env_file = ".env"

settings = Settings()