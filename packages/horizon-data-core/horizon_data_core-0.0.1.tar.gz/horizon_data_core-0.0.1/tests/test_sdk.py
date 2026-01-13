import os
from uuid import uuid4, UUID
import pytest
from horizon_data_core.client import PostgresClient
from horizon_data_core.sdk import HorizonSDK, IcebergRepository
from horizon_data_core.base_types import Entity, DataStream
from sqlalchemy import text
from unittest.mock import Mock


@pytest.fixture
def initialized_sdk() -> HorizonSDK:
    """Fixture to initialize SDK with database connection."""
    postgres_client = PostgresClient(
        user=os.environ.get("OWNER_PGUSER", "postgres"),
        password=os.environ.get("OWNER_PGPASSWORD", "password"),
        host=os.environ.get("PGHOST", "localhost"),
        port=int(os.environ.get("PGPORT", 5432)),
        database=os.environ.get("PGDATABASE", "horizon"),
        sslmode="disable",
        channel_binding="prefer",
    )
    iceberg_catalog_properties: dict[str, str | None] = {
        "uri": "http://localhost:8181",
        "warehouse": "file://./iceberg/warehouse",
    }
    return HorizonSDK(postgres_client, iceberg_catalog_properties, None)


@pytest.fixture
def entity_kind_id(initialized_sdk: HorizonSDK) -> UUID:
    """Fixture to create an entity kind for use in repository tests."""
    kind_id = uuid4()
    with initialized_sdk.postgres_client.session() as session:
        session.execute(
            text("INSERT INTO horizon_public.entity_kind (id, name) VALUES (:id, :name)"),
            {"id": kind_id, "name": "Test Entity Kind"}
        )
        session.commit()
    return kind_id


def test_create_sdk() -> None:
    """Test that the SDK can be created."""
    postgres_client = PostgresClient(
        user="postgres",
        password="password",
        host="localhost",
        port=5432,
        database="horizon",
        sslmode="disable",
        channel_binding="prefer",
    )
    iceberg_catalog_properties: dict[str, str | None] = {
        "uri": "http://localhost:8181",
        "warehouse": "file://./iceberg/warehouse",
    }
    sdk = HorizonSDK(postgres_client, iceberg_catalog_properties, None)
    assert sdk is not None


# Repository Operation Tests

def test_repository_insert(initialized_sdk: HorizonSDK, entity_kind_id: UUID) -> None:
    """Test that repository insert() creates a new record."""
    entity = Entity(
        id=uuid4(),
        kind_id=entity_kind_id,
        name="Test Entity",
    )
    result = initialized_sdk.entities.insert(entity)
    assert result.id == entity.id
    assert result.name == "Test Entity"
    assert result.kind_id == entity_kind_id


def test_repository_insert_batch(initialized_sdk: HorizonSDK, entity_kind_id: UUID) -> None:
    """Test that repository insert_batch() creates multiple records."""
    entities = [
        Entity(id=uuid4(), kind_id=entity_kind_id, name="Entity 1"),
        Entity(id=uuid4(), kind_id=entity_kind_id, name="Entity 2"),
    ]
    result = initialized_sdk.entities.insert_batch(entities)
    assert len(result) == 2
    assert all(r.name in ["Entity 1", "Entity 2"] for r in result)


def test_repository_insert_batch_empty(initialized_sdk: HorizonSDK) -> None:
    """Test that repository insert_batch() returns empty list for empty input."""
    result = initialized_sdk.entities.insert_batch([])
    assert result == []


def test_repository_read(initialized_sdk: HorizonSDK, entity_kind_id: UUID) -> None:
    """Test that repository read() retrieves a record by ID."""
    entity = Entity(id=uuid4(), kind_id=entity_kind_id, name="Test Entity")
    created = initialized_sdk.entities.insert(entity)
    assert created.id is not None
    
    result = initialized_sdk.entities.read(created.id)
    assert result is not None
    assert result.id == created.id
    assert result.name == "Test Entity"


def test_repository_read_not_found(initialized_sdk: HorizonSDK) -> None:
    """Test that repository read() returns None for non-existent ID."""
    result = initialized_sdk.entities.read(uuid4())
    assert result is None


def test_repository_update(initialized_sdk: HorizonSDK, entity_kind_id: UUID) -> None:
    """Test that repository update() modifies an existing record."""
    entity = Entity(id=uuid4(), kind_id=entity_kind_id, name="Original Name")
    created = initialized_sdk.entities.insert(entity)
    assert created.id is not None
    
    updated_entity = Entity(id=created.id, kind_id=entity_kind_id, name="Updated Name")
    result = initialized_sdk.entities.update(updated_entity)
    assert result.name == "Updated Name"
    
    # Verify update persisted
    read_result = initialized_sdk.entities.read(created.id)
    assert read_result is not None
    assert read_result.name == "Updated Name"


def test_repository_delete(initialized_sdk: HorizonSDK, entity_kind_id: UUID) -> None:
    """Test that repository delete() removes a record."""
    entity = Entity(id=uuid4(), kind_id=entity_kind_id, name="Entity to delete")
    created = initialized_sdk.entities.insert(entity)
    assert created.id is not None
    
    deleted = initialized_sdk.entities.delete(created.id)
    assert deleted is True
    
    # Verify it's gone
    result = initialized_sdk.entities.read(created.id)
    assert result is None


def test_repository_delete_not_found(initialized_sdk: HorizonSDK) -> None:
    """Test that repository delete() returns False for non-existent ID."""
    result = initialized_sdk.entities.delete(uuid4())
    assert result is False


def test_repository_list(initialized_sdk: HorizonSDK, entity_kind_id: UUID) -> None:
    """Test that repository list() returns all records."""
    entity1 = initialized_sdk.entities.insert(Entity(id=uuid4(), kind_id=entity_kind_id, name="Entity 1"))
    entity2 = initialized_sdk.entities.insert(Entity(id=uuid4(), kind_id=entity_kind_id, name="entity 2"))
    
    result = initialized_sdk.entities.list()
    assert len(result) >= 2
    entity_ids = {e.id for e in result}
    assert entity1.id in entity_ids
    assert entity2.id in entity_ids


def test_repository_list_with_filters(initialized_sdk: HorizonSDK, entity_kind_id: UUID) -> None:
    """Test that repository list() filters records correctly."""
    entity1 = initialized_sdk.entities.insert(Entity(id=uuid4(), kind_id=entity_kind_id, name="Filtered Entity"))
    initialized_sdk.entities.insert(Entity(id=uuid4(), kind_id=entity_kind_id, name="Other Entity"))
    
    # Filter by name
    result = initialized_sdk.entities.list(name="Filtered Entity")  # type: ignore[arg-type]
    assert len(result) >= 1
    assert all(e.name == "Filtered Entity" for e in result)
    assert entity1.id in {e.id for e in result}
    
    # Filter by kind_id
    kind_result = initialized_sdk.entities.list(kind_id=entity_kind_id)  # type: ignore[arg-type]
    assert len(kind_result) >= 2
    assert all(e.kind_id == entity_kind_id for e in kind_result)


def test_repository_upsert_create(initialized_sdk: HorizonSDK, entity_kind_id: UUID) -> None:
    """Test that repository upsert() creates a new record when it doesn't exist."""
    entity = Entity(id=uuid4(), kind_id=entity_kind_id, name="New Entity")
    result = initialized_sdk.entities.upsert(entity, unique_fields=["id"], merge_fields=["name", "kind_id"])
    assert result.id == entity.id
    assert result.id is not None
    
    # Verify it was created
    read_result = initialized_sdk.entities.read(result.id)
    assert read_result is not None
    assert read_result.name == "New Entity"


def test_repository_upsert_update(initialized_sdk: HorizonSDK, entity_kind_id: UUID) -> None:
    """Test that repository upsert() updates an existing record."""
    entity = Entity(id=uuid4(), kind_id=entity_kind_id, name="Original Name")
    created = initialized_sdk.entities.insert(entity)
    assert created.id is not None
    
    # Upsert with updated name
    updated = Entity(id=created.id, kind_id=entity_kind_id, name="Upserted Name")
    result = initialized_sdk.entities.upsert(updated, unique_fields=["id"], merge_fields=["name"])
    assert result.name == "Upserted Name"
    
    # Verify update persisted
    read_result = initialized_sdk.entities.read(created.id)
    assert read_result is not None
    assert read_result.name == "Upserted Name"


def test_repository_upsert_batch(initialized_sdk: HorizonSDK, entity_kind_id: UUID) -> None:
    """Test that repository upsert_batch() creates or updates multiple records."""
    # Create one entity first
    existing = initialized_sdk.entities.insert(Entity(id=uuid4(), kind_id=entity_kind_id, name="Existing"))
    assert existing.id is not None
    
    # Upsert batch with one existing and one new
    entities = [
        Entity(id=existing.id, kind_id=entity_kind_id, name="Updated Existing"),
        Entity(id=uuid4(), kind_id=entity_kind_id, name="New Entity"),
    ]
    result = initialized_sdk.entities.upsert_batch(entities, unique_fields=["id"], merge_fields=["name", "kind_id"])
    assert len(result) == 2
    
    # Verify existing was updated
    read_existing = initialized_sdk.entities.read(existing.id)
    assert read_existing is not None
    assert read_existing.name == "Updated Existing"
    
    # Verify new was created
    new_ids = {e.id for e in result}
    assert entities[1].id in new_ids

def test_sdk_create_data_stream_idempotent_id(initialized_sdk: HorizonSDK, entity_kind_id: UUID) -> None:
    """Test that creating data streams with the same platform and name produces the same ID."""
    # Create an entity to use as the platform for the data stream
    entity = Entity(
        id=uuid4(),
        kind_id=entity_kind_id,
        name="Test Platform Entity",
    )

    created_entity = initialized_sdk.entities.insert(entity)
    assert created_entity.id is not None
    data_stream_name = "Acoustic"

    # Create first data stream using from_platform_and_name
    data_stream_one = DataStream.from_platform_and_name(created_entity, data_stream_name)
    result_one = initialized_sdk.create_data_stream(data_stream_one)
    assert result_one.id is not None

    # Create second data stream with the same platform and name
    data_stream_two = DataStream.from_platform_and_name(created_entity, data_stream_name)
    result_two = initialized_sdk.create_data_stream(data_stream_two)
    assert result_two.id is not None

    # Verify both data streams have the same ID (idempotent)
    assert result_one.id == result_two.id

def test_sdk_read_data_stream(initialized_sdk: HorizonSDK) -> None:
    """Test that SDK read_data_stream calls the repository read method."""
    initialized_sdk.data_streams.read = Mock()  # type: ignore[method-assign]
    initialized_sdk.read_data_stream(uuid4())
    initialized_sdk.data_streams.read.assert_called_once()

def test_sdk_update_data_stream(initialized_sdk: HorizonSDK) -> None:
    """Test that SDK update_data_stream calls the repository upsert method."""
    initialized_sdk.data_streams.upsert = Mock()  # type: ignore[method-assign]
    initialized_sdk.update_data_stream(Mock())
    initialized_sdk.data_streams.upsert.assert_called_once()

def test_sdk_delete_data_stream(initialized_sdk: HorizonSDK) -> None:
    """Test that SDK delete_data_stream calls the repository delete method."""
    initialized_sdk.data_streams.delete = Mock()  # type: ignore[method-assign]
    initialized_sdk.delete_data_stream(uuid4())
    initialized_sdk.data_streams.delete.assert_called_once()

def test_sdk_list_data_streams(initialized_sdk: HorizonSDK) -> None:
    """Test that SDK list_data_streams calls the repository list method."""
    initialized_sdk.data_streams.list = Mock()  # type: ignore[method-assign]
    initialized_sdk.list_data_streams()
    initialized_sdk.data_streams.list.assert_called_once()

def test_sdk_create_mission(initialized_sdk: HorizonSDK) -> None:
    """Test that SDK create_mission calls the repository insert method."""
    initialized_sdk.missions.insert = Mock()  # type: ignore[method-assign]
    initialized_sdk.create_mission(Mock())
    initialized_sdk.missions.insert.assert_called_once()

def test_sdk_read_mission(initialized_sdk: HorizonSDK) -> None:
    """Test that SDK read_mission calls the repository read method."""
    initialized_sdk.missions.read = Mock()  # type: ignore[method-assign]
    initialized_sdk.read_mission(Mock())
    initialized_sdk.missions.read.assert_called_once()

def test_sdk_update_mission(initialized_sdk: HorizonSDK) -> None:
    """Test that SDK update_mission calls the repository update method."""
    initialized_sdk.missions.update = Mock()  # type: ignore[method-assign]
    initialized_sdk.update_mission(Mock())
    initialized_sdk.missions.update.assert_called_once()

def test_sdk_delete_mission(initialized_sdk: HorizonSDK) -> None:
    """Test that SDK read_mission calls the repository delete method."""
    initialized_sdk.missions.delete = Mock()  # type: ignore[method-assign]
    initialized_sdk.delete_mission(Mock())
    initialized_sdk.missions.delete.assert_called_once()
