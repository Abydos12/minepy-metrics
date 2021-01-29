import os

__all__ = ["RCON_PASSWORD", "RCON_HOST", "RCON_PORT", "RCON_ENABLED", "ROOT_PATH"]

RCON_PASSWORD = os.getenv("RCON_PASSWORD", "")
RCON_HOST = os.getenv("RCON_HOST", "")
RCON_PORT = int(os.getenv("RCON_PORT", 25575))
WORLD_NAME = os.getenv("WORLD_NAME", "world")

RCON_ENABLED = RCON_PASSWORD and RCON_HOST

# ROOT_PATH = "C:/Users/Guillaume/Desktop/Valhelsia_SERVER-3.1.6"
ROOT_PATH = "C:/Users/Guillaume/Desktop/FeedTheBeast"
