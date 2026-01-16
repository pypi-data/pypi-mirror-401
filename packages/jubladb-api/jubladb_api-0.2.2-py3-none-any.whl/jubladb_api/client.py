from jubladb_api.generated.client import *
from jubladb_api.core.base_client import JublaDbError

def create(url: str, api_key: str) -> Client:
    return Client(url, api_key)

__all__ = ["create", "Client"]