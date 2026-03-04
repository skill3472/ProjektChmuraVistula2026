import os

from azure.cosmos import CosmosClient
from sqlalchemy.orm import Session

from src.models import Counter
from src.utils import is_cloud


class DatabaseRepository:
    """Repository class to handle database operations for the counter."""
    db_name = os.environ.get("COSMOS_DB", "counterdb")
    container_name = os.environ.get("COSMOS_CONTAINER", "counter")

    def _get_container(self, cosmos: CosmosClient):
        """Get or create the Cosmos DB container for the counter."""
        if is_cloud():
            database = cosmos.get_database_client(self.db_name)
            try:
                container = database.get_container_client(self.container_name)
                container.read()
            except Exception:
                container = database.create_container(id=self.container_name, partition_key="/id")
            return container
        else:
            return None

    def create_counter_db(self, db: Session, cosmos: CosmosClient) -> int:
        """Create a new counter with value 0 and persist it."""
        if is_cloud():
            container = self._get_container(cosmos)
            item = {"id": "main", "value": 0}
            container.upsert_item(item)
            count = 0
        else:
            counter = Counter(value=0)
            db.add(counter)
            db.commit()
            db.refresh(counter)
            count = counter.value
        return count

    def get_count_db(self, db: Session, cosmos: CosmosClient) -> int:
        """Retrieve the current counter value from the database."""
        if is_cloud():
            container = self._get_container(cosmos)
            try:
                item = container.read_item(item="main", partition_key="main")
                count = item["value"]
            except Exception:
                count = 0
        else:
            counter = db.query(Counter).first()
            if not counter:
                counter = self.create_counter_db(db, cosmos)
            count = counter.value
        return count

    def increment_counter_db(self, db: Session, cosmos: CosmosClient) -> int:
        """Increment the counter value and persist the change."""
        if is_cloud():
            container = self._get_container(cosmos)
            try:
                item = container.read_item(item="main", partition_key="main")
                item["value"] += 1
                container.upsert_item(item)
                count = item["value"]
            except Exception:
                item = {"id": "main", "value": 1}
                container.upsert_item(item)
                count = 1
        else:
            counter = db.query(Counter).first()
            if not counter:
                counter = self.create_counter_db(db, cosmos)
            counter.value += 1
            db.commit()
            db.refresh(counter)
            count = counter.value
        return count
