import os

ROOT_PATH = "/minecraft"
WORLD_NAME = os.getenv("WORLD_NAME", "world")
FORGE_SERVER = bool(os.getenv("FORGE_SERVER", False))

RCON_PASSWORD = os.getenv("RCON_PASSWORD", None)
RCON_HOST = os.getenv("RCON_HOST", None)
RCON_PORT = int(os.getenv("RCON_PORT", 25575))

RCON_ENABLED = RCON_PASSWORD and RCON_HOST
