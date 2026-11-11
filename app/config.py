"""Application configuration."""

import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "local-development-key-change-me")
    POWERBI_EMBED_URL = os.getenv("POWERBI_EMBED_URL", "").strip()
