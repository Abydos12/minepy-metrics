from src.tools.rcon_client import RconClient


class RconCollector:
    rcon_client: RconClient

    def __init__(self, rcon_client: RconClient):
        self.rcon_client = rcon_client

    def collect(self):
        pass
