import os

from azure.cosmos import CosmosClient


def get_cosmos_client():
    """Create and return a Cosmos DB client."""
    url = os.environ.get("COSMOS_URL")
    key = os.environ.get("COSMOS_KEY")
    if url and key:
        return CosmosClient(url, credential=key)
    return None
