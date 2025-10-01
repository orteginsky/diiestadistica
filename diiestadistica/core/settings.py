from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, EmailStr
from typing import List

class Settings(BaseSettings):
    # Scraping
    scraping_usuario: str = Field(..., description="Usuario scraping")
    scraping_password: str = Field(..., description="Password scraping")
    intranet_url: str = Field("https://intranet.sge.ipn.mx/", description="URL base intranet")
    intranet_home: str = Field("https://intranet.sge.ipn.mx/principal.cfm", description="URL home intranet")

    # Email
    email_remitente: str = Field(..., description="Correo remitente")
    email_password: str = Field(..., description="Password app gmail")
    email_destinatario: str = Field(..., description="Correo destino")
    emails_destinatarios: List[EmailStr] = Field(..., description="Lista de correos destino")
    # Configuración de carga de .env
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

# Instancia global
settings = Settings() # type: ignore

