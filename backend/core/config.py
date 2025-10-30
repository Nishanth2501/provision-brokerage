"""
Configuration module for ProVision Brokerage
Loads environment variables and application settings
"""

import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings(BaseSettings):
    """Application settings"""

    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=True, extra="ignore"
    )

    # Groq AI Configuration
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.1-70b-versatile"

    # Cal.com Configuration
    CALCOM_API_KEY: str = ""
    CALCOM_EVENT_TYPE_ID: str = ""
    CALCOM_USERNAME: str = ""
    CALCOM_API_URL: str = "https://api.cal.com/v1"

    # Sinch Configuration
    SINCH_PROJECT_ID: str = ""
    SINCH_SERVICE_PLAN_ID: str = ""
    SINCH_ACCESS_KEY_ID: str = ""
    SINCH_KEY_SECRET: str = ""
    SINCH_PHONE_NUMBER: str = ""

    # Database Configuration
    DATABASE_URL: str = "sqlite:///./provision_brokerage.db"

    # Application Configuration
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # CORS Configuration - Use string and split it
    CORS_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000,http://localhost:8080,http://127.0.0.1:8080,*"

    @property
    def cors_origins_list(self) -> List[str]:
        """Get CORS origins as a list"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    # AI Configuration
    MAX_CONVERSATION_HISTORY: int = 20
    AI_TEMPERATURE: float = 0.7
    AI_MAX_TOKENS: int = 1000

    # Qualification Configuration
    QUALIFICATION_QUESTIONS_COUNT: int = 7
    HIGH_VALUE_THRESHOLD: int = 80
    QUALIFIED_THRESHOLD: int = 60
    WARM_THRESHOLD: int = 40


# Create global settings instance
settings = Settings()


def validate_config():
    """Validate that required configuration is present"""
    errors = []

    if not settings.GROQ_API_KEY:
        errors.append("GROQ_API_KEY is not set")

    if not settings.CALCOM_API_KEY:
        errors.append("CALCOM_API_KEY is not set")

    if not settings.CALCOM_EVENT_TYPE_ID:
        errors.append("CALCOM_EVENT_TYPE_ID is not set")

    if errors:
        raise ValueError(f"Configuration errors: {', '.join(errors)}")

    return True


if __name__ == "__main__":
    # Test configuration
    validate_config()
    print(" Configuration validated successfully!")
    print(f"Groq Model: {settings.GROQ_MODEL}")
    print(f"Cal.com Username: {settings.CALCOM_USERNAME}")
    print(f"Database: {settings.DATABASE_URL}")
    print(f"Debug Mode: {settings.DEBUG}")
