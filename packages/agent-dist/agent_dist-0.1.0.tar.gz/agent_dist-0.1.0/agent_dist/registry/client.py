import requests

class RegistryClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def list_intent_groups(self) -> dict:
        return requests.get(f"{self.base_url}/vocab/intent_groups").json()

    def list_capability_clusters(self) -> dict:
        return requests.get(f"{self.base_url}/vocab/capability_clusters").json()

    def list_agents(self) -> list:
        return requests.get(f"{self.base_url}/agents").json()
    
    def get_agent(self, name: str) -> dict:
        agents = self.list_agents()
        for a in agents:
            if a["name"] == name:
                return a
        raise ValueError(f"Agent '{name}' not found in registry")