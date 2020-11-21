import os


__all__ = ["RCON_PASSWORD", "RCON_HOST", "RCON_PORT", "RCON_ENABLED", "ROOT_PATH"]

RCON_PASSWORD = os.getenv("RCON_PASSWORD", "")
RCON_HOST = os.getenv("RCON_HOST", "")
RCON_PORT = os.getenv("RCON_PORT", 25575)

RCON_ENABLED = RCON_PASSWORD and RCON_HOST

ROOT_PATH = "/minecraft"
