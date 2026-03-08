import os

from azure.cosmos import CosmosClient


class DatabaseRepository:
    """Repository class to handle Cosmos DB operations for the counter."""

    db_name = os.environ.get("COSMOS_DB", "counterdb")
    container_name = os.environ.get("COSMOS_CONTAINER", "counter")

    def _get_container(self, cosmos: CosmosClient):
        """Get or create the Cosmos DB container for the counter."""
        database = cosmos.get_database_client(self.db_name)
        try:
            container = database.get_container_client(self.container_name)
            container.read()
        except Exception:
            container = database.create_container(id=self.container_name, partition_key="/id")
        return container

    def create_counter_db(self, cosmos: CosmosClient) -> int:
        """Create a new counter with value 0 and persist it."""
        container = self._get_container(cosmos)
        item = {"id": "main", "value": 0}
        container.upsert_item(item)
        return 0

    def get_count_db(self, cosmos: CosmosClient) -> int:
        """Retrieve the current counter value from Cosmos DB."""
        container = self._get_container(cosmos)
        try:
            item = container.read_item(item="main", partition_key="main")
            return item["value"]
        except Exception:
            return 0

    def increment_counter_db(self, cosmos: CosmosClient) -> int:
        """Increment the counter value and persist the change in Cosmos DB."""
        container = self._get_container(cosmos)
        try:
            item = container.read_item(item="main", partition_key="main")
            item["value"] += 1
            container.upsert_item(item)
            return item["value"]
        except Exception:
            item = {"id": "main", "value": 1}
            container.upsert_item(item)
            return 1
