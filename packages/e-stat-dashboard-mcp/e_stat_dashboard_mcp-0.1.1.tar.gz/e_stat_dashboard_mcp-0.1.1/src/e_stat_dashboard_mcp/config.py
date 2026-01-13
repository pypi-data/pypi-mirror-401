from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    API_BASE_URL: str = "https://dashboard.e-stat.go.jp/api/1.0/Json"
    LANG: str = "JP"
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", env_prefix="ESTAT_")

settings = Settings()
