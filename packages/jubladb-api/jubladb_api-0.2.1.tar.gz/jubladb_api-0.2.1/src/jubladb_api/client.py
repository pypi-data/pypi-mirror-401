from jubladb_api.generated.client import *

def create(url: str, api_key: str) -> Client:
    return Client(url, api_key)

__all__ = ["create", "Client"]