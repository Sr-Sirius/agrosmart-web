"""Application configuration."""

import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "local-development-key-change-me")
    POWERBI_EMBED_URL = os.getenv("POWERBI_EMBED_URL", "").strip()

    # API del ESP32 y monitoreo en vivo: solo en la red local (equipo BELLATOR).
    ENABLE_DEVICE_API = os.getenv("ENABLE_DEVICE_API", "0").strip() == "1"
    DEVICE_API_KEY = os.getenv("DEVICE_API_KEY", "").strip()
    DEVICE_RATE_LIMIT = int(os.getenv("DEVICE_RATE_LIMIT", "120"))
    AGROSMART_DB_CONN = os.getenv("AGROSMART_DB_CONN", "").strip()
