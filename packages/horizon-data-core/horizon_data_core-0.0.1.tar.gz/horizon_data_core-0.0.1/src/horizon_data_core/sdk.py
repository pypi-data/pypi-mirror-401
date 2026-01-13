"""SDK for Horizon Data Core operations."""
# Do not lint for exception strings being assigned to variables first
# ruff: noqa: EM101
# ruff: noqa: EM102
# Do not lint for logger f-strings
# ruff: noqa: G004
# Do not lint for long messages in exceptions
# ruff: noqa: TRY003

import logging
import random
import time
from abc import ABC, abstractmethod
from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID

import pyarrow as pa
from pydantic import BaseModel
from pyiceberg.catalog import Catalog, load_catalog
from pyiceberg.exceptions import CommitFailedException, OAuthError
from pyiceberg.table import Table as IcebergTable
from sqlalchemy import inspect, select
from sqlalchemy.dialects.postgresql import insert

from horizon_data_core.logging import log_calls

from .base_types import (
    BasePostgresModel,
    BasePyarrowModel,
    BeamgramSpecification,
    BearingTimeRecordSpecification,
    DataRow,
    DataStream,
    Entity,
    EntityBeamgramSpecification,
    EntityBearingTimeRecordSpecification,
    MetadataRow,
    Mission,
    MissionEntity,
    Ontology,
    OntologyClass,
)
from .client import Client
from .orm_types import (
    BeamgramSpecificationOrm,
    BearingTimeRecordSpecificationOrm,
    DataRowOrm,
    DataStreamOrm,
    EntityBeamgramSpecificationOrm,
    EntityBearingTimeRecordSpecificationOrm,
    EntityOrm,
    HorizonPublicOrm,
    MetadataRowOrm,
    MissionEntityOrm,
    MissionOrm,
    OntologyClassOrm,
    OntologyOrm,
)

logger = logging.getLogger(__name__)


class BaseRepository[B: BaseModel](ABC):
    """Base repository for database operations.

    Defines a basic set of operations:
        - insert        Create a new database entry
        - insert_batch  Create several new database entries
        - upsert        Create (or update) a new database entry (if matching entry exists)
        - upsert_batch  Create (or update) several new entries (if matching entry exists)
        - read          Return the entry given its id
        - update        Update an existing entry, error if it does not already exist
        - delete        Remove an existing entry
        - list          Return a list of entries (possibly empty) from a list of filter conditions
    """

    def __init__(self, client: Client) -> None:
        """Initialize the base repository.

        Args:
            client: Database client for operations
        """
        self.client = client

    @abstractmethod
    def insert(self, model: B) -> B:
        """Insert a new record."""

    @abstractmethod
    def insert_batch(self, models: list[B]) -> list[B]:
        """Create a new record batch."""

    @abstractmethod
    def upsert(self, model: B, unique_fields: list[str], merge_fields: list[str]) -> B:
        """Insert a new record or update if it already exists."""

    @abstractmethod
    def upsert_batch(self, models: list[B], unique_fields: list[str], merge_fields: list[str]) -> list[B]:
        """Insert a new record or update if it already exists."""

    @abstractmethod
    def read(self, id: UUID) -> B | None:
        """Read a record by ID."""

    @abstractmethod
    def update(self, model: B) -> B:
        """Update an existing record."""

    @abstractmethod
    def delete(self, id: UUID) -> bool:
        """Delete a record by ID."""

    @abstractmethod
    def list(self, **filters: Any) -> list[B]:  # noqa: ANN401
        """List records with optional filters."""


class PostgresRepository[P: BasePostgresModel, O: HorizonPublicOrm](BaseRepository[P]):
    """Repository for PostgreSQL operations."""

    def __init__(
        self, model_class: type[P], orm_class: type[O], client: Client, organization_id: UUID | None = None
    ) -> None:
        """Initialize the PostgreSQL repository.

        Args:
            client: PostgreSQL client for database operations
            model_class: The model class this repository handles
            organization_id: Organization ID for multi-tenancy (optional)

        Raises:
            ValueError: If no ORM class is found for the model class
        """
        super().__init__(client)
        self.model_class = model_class
        self.organization_id = organization_id
        self.orm_class = orm_class

    def _base_model_to_orm(self, model: P) -> O:
        """Convert BaseModel to SQLAlchemy ORM model."""
        model_dict = model.model_dump(exclude_none=True)
        # Ensure organization_id is set if its part of the model
        if "organization_id" in self.model_class.model_fields:
            model_dict["organization_id"] = self.organization_id
        # Modified datetime is set by trigger on the database side, but has a NOT NULL constraint
        # (abuck) I couldn't figure out how to get around the NOT NULL constraint so we just set it to "now"
        # in the SDK and allow a user to send "None".
        model.modified_datetime = datetime.now(UTC)
        orm = self.orm_class(**model_dict)
        orm.modified_datetime = datetime.now(UTC)
        return orm

    def _orm_to_base_model(self, orm_instance: O) -> P:
        """Convert SQLAlchemy ORM model to BaseModel."""
        mapper = inspect(orm_instance.__class__)
        assert mapper is not None  # inspect will raise an exception rather than returning None
        orm_dict = {column.name: getattr(orm_instance, column.name) for column in mapper.columns}
        return self.model_class(**orm_dict)

    @log_calls(logger, level=logging.DEBUG)
    def insert(self, model: P) -> P:
        """Insert a new record in PostgreSQL.

        Args:
            model: The model instance to create

        Returns:
            The inserted model instance with updated fields (e.g., generated ID)

        Raises:
            SQLAlchemyError: If database operation fails
        """
        with self.client.session() as session:
            # Convert all models to ORM instances
            orm_instance = self._base_model_to_orm(model)
            session.add(orm_instance)
            session.commit()
            # Convert back to models
            return self._orm_to_base_model(orm_instance)

    def insert_batch(self, models: list[P]) -> list[P]:
        """Create a new record batch in PostgreSQL.

        Args:
            models: List of model instances to create

        Returns:
            List of created model instances with updated fields or empty list if input is empty

        Raises:
            SQLAlchemyError: If database operation fails
        """
        # Early return for empty input
        if not models:
            logger.warning("Empty input provided to upsert_batch. No action taken.")
            return []

        with self.client.session() as session:
            # Convert all models to ORM instances
            orm_instances = [self._base_model_to_orm(m) for m in models]
            session.add_all(orm_instances)
            session.commit()
            # Convert back to models
            return [self._orm_to_base_model(orm) for orm in orm_instances]

    def upsert(
        self,
        model: P,
        unique_fields: list[str] | None = None,  # Natural key columns
        merge_fields: list[str] | None = None,  # Columns to update on conflict
    ) -> P:
        """
        Upsert using PostgreSQL's ON CONFLICT.

        Args:
            model: The model to upsert
            unique_fields: Columns that define uniqueness (e.g., ['name', 'mission_id'])
            merge_fields: Columns to update on conflict (None = all except conflict_columns)

        Returns:
            The created or updated model instance

        Raises:
            SQLAlchemyError: If database operation fails
        """
        with self.client.session() as session:
            orm_instance = self._base_model_to_orm(model)
            orm_class = self.orm_class

            # Get all columns
            inspector = inspect(orm_class)
            assert inspector is not None  # inspect will raise an exception rather than returning None
            table_columns = inspector.columns
            all_columns = table_columns.keys()

            # Default: use primary key as conflict column
            if unique_fields is None:
                unique_fields = [c.key for c in table_columns if c.primary_key]

            # Default: update all columns except conflict columns
            if merge_fields is None:
                merge_fields = [c for c in all_columns if c not in unique_fields]

            # Build values dict
            values = {c: getattr(orm_instance, c, None) for c in all_columns}

            # Build statement
            insert_stmt = insert(orm_class).values(**values)
            stmt = insert_stmt.on_conflict_do_update(
                index_elements=unique_fields, set_={col: getattr(insert_stmt.excluded, col) for col in merge_fields}
            ).returning(orm_class)

            result = session.execute(stmt)
            merged_instance = result.scalar_one()

            session.commit()
            session.refresh(merged_instance)
            return self._orm_to_base_model(merged_instance)

    def upsert_batch(
        self,
        models: list[P],
        unique_fields: list[str] | None = None,
        merge_fields: list[str] | None = None,
    ) -> list[P]:
        """
        Batch upsert using PostgreSQL's ON CONFLICT.

        Args:
            models: List of models to upsert
            unique_fields: Columns that define uniqueness
            merge_fields: Columns to update on conflict
        """
        # Early return for empty input
        if not models:
            logger.warning("Empty input provided to upsert_batch. No action taken.")
            return []

        with self.client.session() as session:
            # Convert all models to ORM instances
            orm_instances = [self._base_model_to_orm(m) for m in models]
            orm_class = self.orm_class

            # Get all columns
            inspector = inspect(orm_class)
            assert inspector is not None  # inspect will raise an exception rather than returning None
            table_columns = inspector.columns
            all_columns = table_columns.keys()

            # Default: use primary key as conflict column
            if unique_fields is None:
                unique_fields = [c.key for c in table_columns if c.primary_key]

            if merge_fields is None:
                merge_fields = [c for c in all_columns if c not in unique_fields]

            # Build list of value dicts
            values_list = [{col: getattr(orm, col, None) for col in all_columns} for orm in orm_instances]

            # Build INSERT statement with multiple rows
            insert_stmt = insert(orm_class).values(values_list)
            stmt = insert_stmt.on_conflict_do_update(
                index_elements=unique_fields, set_={col: getattr(insert_stmt.excluded, col) for col in merge_fields}
            ).returning(orm_class)

            # Execute and get all results
            result = session.execute(stmt)
            merged_instances = result.scalars().all()

            session.commit()

            # Convert back to models
            return [self._orm_to_base_model(orm) for orm in merged_instances]

    def read(self, id: UUID) -> P | None:
        """Read a record by ID from PostgreSQL.

        Args:
            id: The UUID of the record to read

        Returns:
            The model instance if found, None otherwise

        Raises:
            SQLAlchemyError: If database operation fails
        """
        with self.client.session() as session:
            orm_instance = session.get(self.orm_class, id)
            if orm_instance:
                return self._orm_to_base_model(orm_instance)
            return None

    def update(self, model: P) -> P:
        """Update an existing record in PostgreSQL.

        Args:
            model: The model instance with updated fields

        Returns:
            The updated model instance

        Raises:
            ValueError: If record with the given ID is not found
            SQLAlchemyError: If database operation fails
        """
        with self.client.session() as session:
            orm_instance = session.get(self.orm_class, model.id)
            if not orm_instance:
                raise ValueError(f"Record with ID {model.id} not found")

            # Update fields
            model_dict = model.model_dump(exclude_none=True)
            for key, value in model_dict.items():
                if hasattr(orm_instance, key):
                    setattr(orm_instance, key, value)

            session.commit()
            session.refresh(orm_instance)
            return self._orm_to_base_model(orm_instance)

    def delete(self, id: UUID) -> bool:
        """Delete a record by ID from PostgreSQL.

        Args:
            id: The UUID of the record to delete

        Returns:
            True if the record was deleted, False if it didn't exist

        Raises:
            SQLAlchemyError: If database operation fails
        """
        with self.client.session() as session:
            orm_instance = session.get(self.orm_class, id)
            if orm_instance:
                session.delete(orm_instance)
                session.commit()
                return True
            return False

    def list(self, **filters: dict[str, Any]) -> list[P]:
        """List records with optional filters from PostgreSQL.

        Args:
            **filters: Keyword arguments where keys are field names and values are filter values

        Returns:
            List of model instances matching the filters

        Raises:
            SQLAlchemyError: If database operation fails
        """
        with self.client.session() as session:
            query = select(self.orm_class)

            # Apply filters
            for key, value in filters.items():
                if hasattr(self.orm_class, key):
                    query = query.where(getattr(self.orm_class, key) == value)

            orm_instances = session.execute(query).scalars().all()
            return [self._orm_to_base_model(instance) for instance in orm_instances]


class IcebergRepository[A: BasePyarrowModel](BaseRepository[A]):  # pragma: no cover
    """Repository for Iceberg table operations."""

    def __init__(
        self,
        catalog: Catalog,
        refresh_catalog: Callable[[], Catalog],
        table_name: str,
        model_class: type[A],
        organization_id: UUID | None = None,
        batch_size: int = 10,
        max_retries: int = 3,
    ) -> None:
        """Initialize the Iceberg repository.

        Args:
            catalog: Iceberg catalog for table operations
            table_name: Name of the Iceberg table
            model_class: The model class this repository handles
            organization_id: Organization ID for multi-tenancy (optional)
            batch_size: Batch size for buffered writes (default: 10)
            max_retries: Maximum retry attempts for failed operations (default: 3)
        """
        self.catalog = catalog
        self.table_name = table_name
        self.model_class = model_class
        self.organization_id = organization_id
        self.table_name = table_name
        self.table = self.catalog.load_table(self.table_name)
        self.buffer: dict[str, list[A]] = {}
        self.batch_size = batch_size
        self.max_retries = max_retries
        self.refresh_catalog = refresh_catalog
        self.catalog_ttl = timedelta(minutes=1)
        self.catalog_created_at = datetime.now(tz=UTC)

    def _append(self, pyarrow_table: pa.Table, max_retries: int | None = None) -> None:
        """Append a PyArrow table to the Iceberg table with retry logic.

        Uses exponential backoff with jitter for retry attempts.

        Args:
            pyarrow_table: The PyArrow table to append
            max_retries: Maximum number of retry attempts (uses instance default if None)

        Raises:
            CommitFailedException: If all retry attempts fail
        """
        if max_retries is None:
            max_retries = self.max_retries
        """Append a PyArrow table to the Iceberg table."""
        retry_count = 0
        sleep_time = 5.0  # 5 seconds
        exponential_backoff_factor = 2.0  # 2x the previous sleep time
        jitter_factor = (
            0.5  # jitter factor on backoff_factor [0 => no jitter, jitter over full range of backoff_factor]
        )
        assert jitter_factor > 0, "Jitter factor should be greater than 0 for algorithm stability."
        assert jitter_factor < exponential_backoff_factor, (
            "Jitter factor should be less than the exponential backoff factor for algorithm stability."
        )
        max_sleep_time = 1200.0  # max sleep time in seconds
        while retry_count < max_retries:
            try:
                logger.info("Appending PyArrow table to Iceberg table, attempt %s of %s", retry_count + 1, max_retries)
                start_time = time.time()
                self.refresh_table().append(pyarrow_table)
            except CommitFailedException as e:
                # We are not yet re-raising the exception so we are not logging it as an exception yet...
                logger.error("Error appending PyArrow table to Iceberg table: %s", e)  # noqa: TRY400
                retry_count += 1
                logger.info("Sleeping for %s seconds before retrying", sleep_time)
                time.sleep(sleep_time)
                # Update backoff with jitter
                sleep_time = sleep_time * (
                    # random.random() is not being used for cryptographic purposes
                    # so it is suitable for this use case: S311
                    exponential_backoff_factor * (1.0 + random.random() * jitter_factor * 2.0 - jitter_factor)  # noqa: S311
                )
                sleep_time = min(sleep_time, max_sleep_time)
                if retry_count >= max_retries:
                    logger.exception("Failed to append pyarrow table to iceberg table after %s retries", max_retries)
                    raise
            else:
                # If we get here, we successfully appended the PyArrow table to the Iceberg table
                logger.info(
                    "Appended PyArrow table to Iceberg table, attempt %s of %s, time taken: %s seconds",
                    retry_count + 1,
                    max_retries,
                    time.time() - start_time,
                )
                return

    def refresh_table(self) -> IcebergTable:
        """Refresh the Iceberg table.

        Reloads the table from the catalog to get the latest metadata.

        Returns:
            The refreshed Iceberg table instance
        """
        try:
            self.table = self.catalog.load_table(self.table_name)
        except OAuthError as e:
            logger.warning("OAuthError when loading Iceberg table: %s", e)
            logger.warning("Attempting to refresh OAuth token by reloading the catalog")
            # Refresh the catalog
            self.catalog = self.refresh_catalog()
            # Reload the table
            self.table = self.catalog.load_table(self.table_name)
            logger.warning("Successfully refreshed Iceberg table")

        return self.table

    def _should_flush(self, buffer_name: str) -> bool:
        """Check if the buffer should be flushed.

        Args:
            buffer_name: Name of the buffer to check

        Returns:
            True if buffer size exceeds batch_size, False otherwise
        """
        buffer = self._get_buffer(buffer_name)
        return len(buffer) >= self.batch_size

    def _write(self, models: list[A]) -> None:
        """Write a list of models to the Iceberg table.

        Converts models to PyArrow format and appends to the table.

        Args:
            models: List of models to write

        Raises:
            CommitFailedException: If write operation fails after retries
        """
        if not models:
            logger.debug("IcebergRepository._write called with empty models; skipping.")
            return

        table = pa.concat_tables([model.to_pyarrow() for model in models])
        self._append(table)

    def _clear_buffer(self, buffer_name: str) -> None:
        """Clear the buffer for a given buffer name.

        Args:
            buffer_name: Name of the buffer to clear
        """
        self.buffer[buffer_name] = []

    def _get_buffer(self, buffer_name: str) -> list[A]:
        """Get the buffer for a given buffer name.

        Creates a new empty buffer if it doesn't exist.

        Args:
            buffer_name: Name of the buffer to get

        Returns:
            List of model instances in the buffer
        """
        if buffer_name not in self.buffer:
            self.buffer[buffer_name] = []
        return self.buffer[buffer_name]

    def _pop_buffer(self, buffer_name: str) -> list[A]:
        """Pop the buffer for a given buffer name.

        Args:
            buffer_name: Name of the buffer to pop
        """
        if buffer_name not in self.buffer:
            return []
        return self.buffer.pop(buffer_name)

    def flush(self, buffer_name: str | None = None) -> None:
        """Flush the buffer to the Iceberg table.

        If no buffer_name is provided, all buffers will be flushed.

        Args:
            buffer_name: Name of specific buffer to flush, or None to flush all buffers

        Raises:
            CommitFailedException: If write operation fails after retries
        """
        if buffer_name:
            logger.info(f"Flushing buffer: {buffer_name}")
            buffer = self._pop_buffer(buffer_name)
            self._write(buffer)
        else:
            self.group_flush(list(self.buffer.keys()))

    def group_flush(self, buffer_names: list[str]) -> None:
        """Flush a group of buffers to the Iceberg table.

        Args:
            buffer_names: List of buffer names to flush
        """
        if len(buffer_names) == 0:
            logger.debug("No buffers to flush")
            return
        group_buffer = [model for buffer_name in buffer_names for model in self._pop_buffer(buffer_name)]
        logger.info("Flushing buffers %s to Iceberg table", buffer_names)
        self._write(group_buffer)

    def tick(self) -> None:
        """Tick the Iceberg repository.

        This is used to flush the buffers if they are not flushed by the time the tick is called.
        """
        # Refresh the catalog if it has expired
        if datetime.now(tz=UTC) - self.catalog_created_at >= self.catalog_ttl:
            logger.info("Refreshing Iceberg catalog")
            self.catalog = self.refresh_catalog()
            self.catalog_created_at = datetime.now(tz=UTC)

        # Flush any buffers that are ready to be flushed as a group
        buffers_to_flush = []
        for buf_name in self.buffer:
            if self._should_flush(buf_name):
                logger.debug("(%s) Adding buffer to flush list", buf_name)
                buffers_to_flush.append(buf_name)
        self.group_flush(buffers_to_flush)

    def insert(self, model: A, buffer_name: str | None = None) -> A:
        """Create a new record in Iceberg table.

        Args:
            model: The model instance to create
            buffer_name: Optional buffer name for batching writes

        Returns:
            The model instance (unchanged)

        Raises:
            CommitFailedException: If write operation fails after retries
        """
        if buffer_name:
            buffer = self._get_buffer(buffer_name)
            buffer.append(model)
            logger.debug(f"({buffer_name}) Buffer size now %s rows", len(buffer))
        else:
            self._write([model])
        return model

    def insert_batch(self, models: list[A], buffer_name: str | None = None) -> list[A]:
        """Create a new record batch in Iceberg table.

        If a buffer_name is provided, the models will be added to the buffer and flushed as needed.

        If no buffer_name is provided, the models will be written directly to the Iceberg table.
        NOTE: THIS WILL BYPASS THE BUFFER, so it may result in out-of-order writes if you mix
        buffered and non-buffered writes.

        Args:
            models: List of model instances to create
            buffer_name: Optional buffer name for batching writes

        Returns:
            The list of model instances (unchanged)

        Raises:
            CommitFailedException: If write operation fails after retries
        """
        # Write to Iceberg table
        if buffer_name:
            buffer = self._get_buffer(buffer_name)
            buffer.extend(models)
            logger.debug(f"Buffer size now: {len(buffer)}")
        else:
            self._write(models)
        return models

    def upsert(self, model: A, unique_fields: list[str], merge_fields: list[str]) -> A:
        """Upsert a new record in Iceberg table.

        Args:
            model: The model instance to create or update
            unique_fields: The list of fields to detect conflict
            merge_fields: The fields to update on conflict

        Raises:
            NotImplementedError: Always raised as Iceberg doesn't support upserts
        """
        # Iceberg doesn't have native upsert support, so we just create
        raise NotImplementedError("Upsert operations for Iceberg tables not implemented")

    def read(self, id: UUID) -> A | None:
        """Read a record by ID from Iceberg table.

        Args:
            id: The UUID of the record to read

        Raises:
            NotImplementedError: Always raised as Iceberg doesn't support direct ID lookups
        """
        # Note: Iceberg doesn't have direct ID-based lookups like SQL
        raise NotImplementedError("Read operations for Iceberg tables not implemented")

    def update(self, model: A) -> A:
        """Update an existing record in Iceberg table.

        Args:
            model: The model instance with updated fields

        Raises:
            NotImplementedError: Always raised as Iceberg updates are table-specific
        """
        raise NotImplementedError("Update operations for Iceberg tables not implemented")

    def delete(self, id: UUID) -> bool:
        """Delete a record by ID from Iceberg table.

        Args:
            id: The UUID of the record to delete

        Raises:
            NotImplementedError: Always raised as Iceberg deletes are table-specific
        """
        raise NotImplementedError("Delete operations for Iceberg tables not implemented")

    def list(self, **filters: Any) -> list[A]:  # noqa: ANN401
        """List records with optional filters from Iceberg table.

        Args:
            **filters: Iceberg scan parameters including:
                - row_filter: str | boolean_expr = True
                - selected_fields: tuple[str] = ("*",)
                - case_sensitive: bool = True
                - snapshot_id: str | None = None
                - options: Properties = {}
                - limit: int | None = None

        Returns:
            List of model instances matching the filters

        Raises:
            Exception: If Iceberg scan operation fails
        """
        # Convert filters to Iceberg query format
        table = self.refresh_table().scan(**filters).to_polars()
        # A given instance of an Iceberg Repository is tied to a single table, which means
        # it is tied to a single schema and model_class, so we should be able to
        # read from the table and directly instantiate the model_class with the row
        return [self.model_class(**row) for row in table.iter_rows(named=True)]


class HorizonSDK:
    """Main SDK class for Horizon Data Core operations."""

    def __init__(
        self,
        postgres_client: Client,
        # Iceberg repositories were deprecated after version 0.3.6. This will be removed in version 0.5.0
        catalog_properties: dict[str, str | None],  # noqa: ARG002
        organization_id: UUID | None = None,
        # Iceberg repositories were deprecated after version 0.3.6. This will be removed in version 0.5.0
        iceberg_batch_size: int = 16,  # noqa: ARG002
        # Iceberg repositories were deprecated after version 0.3.6. This will be removed in version 0.5.0
        max_retries: int = 10,  # noqa: ARG002
    ) -> None:
        """Initialize the Horizon SDK.

        Args:
            postgres_client: PostgreSQL client for database operations
            catalog_properties: Properties for the Iceberg catalog
            organization_id: Organization ID for multi-tenancy (optional)
            iceberg_batch_size: (DEPRECATED) Batch size for Iceberg operations (default: 16)
            max_retries: (DEPRECATED) Maximum retry attempts for failed operations (default: 10)
        """
        self.catalog_properties: dict[str, str | None] = {}
        self.postgres_client = postgres_client
        self.organization_id = organization_id

        # Initialize repositories for PostgreSQL models
        self.entities = PostgresRepository(Entity, EntityOrm, postgres_client, organization_id)
        self.data_streams = PostgresRepository(DataStream, DataStreamOrm, postgres_client, organization_id)
        self.missions = PostgresRepository(Mission, MissionOrm, postgres_client, organization_id)
        self.mission_entities = PostgresRepository(MissionEntity, MissionEntityOrm, postgres_client, organization_id)
        self.ontologies = PostgresRepository(Ontology, OntologyOrm, postgres_client, organization_id)
        self.ontology_classes = PostgresRepository(OntologyClass, OntologyClassOrm, postgres_client, organization_id)
        self.beamgram_specifications = PostgresRepository(
            BeamgramSpecification, BeamgramSpecificationOrm, postgres_client, organization_id
        )
        self.entity_beamgram_specifications = PostgresRepository(
            EntityBeamgramSpecification, EntityBeamgramSpecificationOrm, postgres_client, organization_id
        )
        self.bearing_time_record_specifications: PostgresRepository[
            BearingTimeRecordSpecification, BearingTimeRecordSpecificationOrm
        ] = PostgresRepository(
            BearingTimeRecordSpecification, BearingTimeRecordSpecificationOrm, postgres_client, organization_id
        )
        self.entity_bearing_time_record_specifications = PostgresRepository(
            EntityBearingTimeRecordSpecification,
            EntityBearingTimeRecordSpecificationOrm,
            postgres_client,
            organization_id,
        )
        self.data_rows = PostgresRepository(DataRow, DataRowOrm, postgres_client, organization_id)
        self.metadata_rows = PostgresRepository(MetadataRow, MetadataRowOrm, postgres_client, organization_id)

    def refresh_iceberg_catalog(self) -> Catalog:
        """Refresh the Iceberg catalog.

        DEPRECATED after v0.3.6
        """
        self.iceberg_catalog = load_catalog("rest", **self.catalog_properties)
        return self.iceberg_catalog

    def tick(self) -> None:
        """Tick the Iceberg repository.

        DEPRECATED after version 0.3.6.
        """
        return

    # Entity-BeamgramSpecification operations
    def create_entity_beamgram_specification(
        self, entity_beamgram_specification: EntityBeamgramSpecification
    ) -> EntityBeamgramSpecification:
        """Create a new entity-beamgram specification relationship."""
        return self.entity_beamgram_specifications.insert(entity_beamgram_specification)

    def list_entity_beamgram_specifications(self, **filters: Any) -> list[EntityBeamgramSpecification]:  # noqa: ANN401
        """List entity-beamgram specification relationships with optional filters."""
        return self.entity_beamgram_specifications.list(**filters)

    # Entity-BearingTimeRecordSpecification operations
    def create_entity_bearing_time_record_specification(
        self, entity_bearing_time_record_specification: EntityBearingTimeRecordSpecification
    ) -> EntityBearingTimeRecordSpecification:
        """Create a new entity-btr specification relationship."""
        return self.entity_bearing_time_record_specifications.insert(entity_bearing_time_record_specification)

    def list_entity_bearing_time_record_specifications(
        self,
        **filters: Any,  # noqa: ANN401
    ) -> list[EntityBearingTimeRecordSpecification]:
        """List entity-btr specification relationships with optional filters."""
        return self.entity_bearing_time_record_specifications.list(**filters)

    # PostgreSQL operations
    def create_entity(self, entity: Entity) -> Entity:
        """Create a new entity.

        Args:
            entity: The entity instance to create

        Returns:
            The created entity with updated fields (e.g., generated ID)

        Raises:
            SQLAlchemyError: If database operation fails
        """
        logger.debug(
            "SDK: Creating entity",
            extra={"entity": entity},
        )
        return self.entities.upsert(entity)

    def create_or_update_entity(self, entity: Entity) -> Entity:
        """Create a new entity or update if it already exists.

        Uses custom datetime logic for start_datetime and end_datetime fields:
        - Updates start_datetime if new value is earlier than existing
        - Updates end_datetime if new value is later than existing

        Args:
            entity: The entity instance to create or update

        Returns:
            The created or updated entity

        Raises:
            SQLAlchemyError: If database operation fails
        """
        logger.debug(
            "SDK: Creating or updating entity",
            extra={"entity": entity},
        )

        # Custom logic for start_datetime and end_datetime fields:
        # - Updates start_datetime if new value is earlier than existing
        # - Keep start_datetime if new value is None and existing value is not None
        # - Updates end_datetime if new value is later than existing
        # - Keep end_datetime if new value is None and existing value is not None
        if entity.id is not None:
            existing_entity = self.entities.read(entity.id)
            if existing_entity is not None:
                updated_entity = entity

                # Keep start_datetime if both values are set and new value is later than existing
                # Keep start_datetime if new value is None and existing value is not None
                if (
                    updated_entity.start_datetime is not None
                    and existing_entity.start_datetime is not None
                    and updated_entity.start_datetime > existing_entity.start_datetime
                ) or (updated_entity.start_datetime is None and existing_entity.start_datetime is not None):
                    updated_entity.start_datetime = existing_entity.start_datetime

                # Keep end_datetime if both values are set and new value is later than existing
                # Keep end_datetime if new value is None and existing value is not None
                if (
                    updated_entity.end_datetime is not None
                    and existing_entity.end_datetime is not None
                    and updated_entity.end_datetime < existing_entity.end_datetime
                ) or (updated_entity.end_datetime is None and existing_entity.end_datetime is not None):
                    updated_entity.end_datetime = existing_entity.end_datetime

                return self.entities.upsert(updated_entity)
        # If no existing entity or no ID, do regular upsert
        return self.entities.upsert(entity)

    def read_entity(self, id: UUID) -> Entity | None:
        """Read an entity by ID.

        Args:
            id: The UUID of the entity to read

        Returns:
            The entity if found, None otherwise

        Raises:
            SQLAlchemyError: If database operation fails
        """
        return self.entities.read(id)

    def update_entity(self, entity: Entity) -> Entity:
        """Update an existing entity.

        Args:
            entity: The entity instance with updated fields

        Returns:
            The updated entity

        Raises:
            ValueError: If entity with the given ID is not found
            SQLAlchemyError: If database operation fails
        """
        return self.entities.update(entity)

    def delete_entity(self, id: UUID) -> bool:
        """Delete an entity by ID.

        Args:
            id: The UUID of the entity to delete

        Returns:
            True if the entity was deleted, False if it didn't exist

        Raises:
            SQLAlchemyError: If database operation fails
        """
        return self.entities.delete(id)

    def list_entities(self, **filters: Any) -> list[Entity]:  # noqa: ANN401
        """List entities with optional filters.

        Args:
            **filters: Keyword arguments where keys are field names and values are filter values

        Returns:
            List of entities matching the filters

        Raises:
            SQLAlchemyError: If database operation fails
        """
        return self.entities.list(**filters)

    def create_data_stream(self, data_stream: DataStream) -> DataStream:
        """Create a new data stream.

        Args:
            data_stream: The data stream instance to create

        Returns:
            The created data stream with updated fields (e.g., generated ID)

        Raises:
            SQLAlchemyError: If database operation fails
        """
        return self.data_streams.upsert(data_stream)

    def read_data_stream(self, id: UUID) -> DataStream | None:
        """Read a data stream by ID.

        Args:
            id: The UUID of the data stream to read

        Returns:
            The data stream if found, None otherwise

        Raises:
            SQLAlchemyError: If database operation fails
        """
        return self.data_streams.read(id)

    def update_data_stream(self, data_stream: DataStream) -> DataStream:
        """Update an existing data stream.

        Args:
            data_stream: The data stream instance with updated fields

        Returns:
            The updated data stream

        Raises:
            ValueError: If data stream with the given ID is not found
            SQLAlchemyError: If database operation fails
        """
        return self.data_streams.upsert(data_stream)

    def delete_data_stream(self, id: UUID) -> bool:
        """Delete a data stream by ID.

        Args:
            id: The UUID of the data stream to delete

        Returns:
            True if the data stream was deleted, False if it didn't exist

        Raises:
            SQLAlchemyError: If database operation fails
        """
        return self.data_streams.delete(id)

    def list_data_streams(self, **filters: Any) -> list[DataStream]:  # noqa: ANN401
        """List data streams with optional filters.

        Args:
            **filters: Keyword arguments where keys are field names and values are filter values

        Returns:
            List of data streams matching the filters

        Raises:
            SQLAlchemyError: If database operation fails
        """
        return self.data_streams.list(**filters)

    def create_mission(self, mission: Mission) -> Mission:
        """Create a new mission.

        Args:
            mission: The mission instance to create

        Returns:
            The created mission with updated fields (e.g., generated ID)

        Raises:
            SQLAlchemyError: If database operation fails
        """
        return self.missions.insert(mission)

    def read_mission(self, id: UUID) -> Mission | None:
        """Read a mission by ID.

        Args:
            id: The UUID of the mission to read

        Returns:
            The mission if found, None otherwise

        Raises:
            SQLAlchemyError: If database operation fails
        """
        return self.missions.read(id)

    def update_mission(self, mission: Mission) -> Mission:
        """Update an existing mission.

        Args:
            mission: The mission instance with updated fields

        Returns:
            The updated mission

        Raises:
            ValueError: If mission with the given ID is not found
            SQLAlchemyError: If database operation fails
        """
        return self.missions.update(mission)

    def delete_mission(self, id: UUID) -> bool:
        """Delete a mission by ID.

        Args:
            id: The UUID of the mission to delete

        Returns:
            True if the mission was deleted, False if it didn't exist

        Raises:
            SQLAlchemyError: If database operation fails
        """
        return self.missions.delete(id)

    def list_missions(self, **filters: Any) -> list[Mission]:  # noqa: ANN401
        """List missions with optional filters.

        Args:
            **filters: Keyword arguments where keys are field names and values are filter values

        Returns:
            List of missions matching the filters

        Raises:
            SQLAlchemyError: If database operation fails
        """
        return self.missions.list(**filters)

    def create_mission_entity(self, mission_entity: MissionEntity) -> MissionEntity:
        """Create a new mission-entity relationship.

        Args:
            mission_entity: The mission-entity relationship instance to create

        Returns:
            The created mission-entity relationship with updated fields (e.g., generated ID)

        Raises:
            SQLAlchemyError: If database operation fails
        """
        return self.mission_entities.insert(mission_entity)

    def read_mission_entity(self, id: UUID) -> MissionEntity | None:
        """Read a mission-entity relationship by ID.

        Args:
            id: The UUID of the mission-entity relationship to read

        Returns:
            The mission-entity relationship if found, None otherwise

        Raises:
            SQLAlchemyError: If database operation fails
        """
        return self.mission_entities.read(id)

    def update_mission_entity(self, mission_entity: MissionEntity) -> MissionEntity:
        """Update an existing mission-entity relationship.

        Args:
            mission_entity: The mission-entity relationship instance with updated fields

        Returns:
            The updated mission-entity relationship

        Raises:
            ValueError: If mission-entity relationship with the given ID is not found
            SQLAlchemyError: If database operation fails
        """
        return self.mission_entities.update(mission_entity)

    def delete_mission_entity(self, id: UUID) -> bool:
        """Delete a mission-entity relationship by ID.

        Args:
            id: The UUID of the mission-entity relationship to delete

        Returns:
            True if the mission-entity relationship was deleted, False if it didn't exist

        Raises:
            SQLAlchemyError: If database operation fails
        """
        return self.mission_entities.delete(id)

    def list_mission_entities(self, **filters: Any) -> list[MissionEntity]:  # noqa: ANN401
        """List mission-entity relationships with optional filters.

        Args:
            **filters: Keyword arguments where keys are field names and values are filter values

        Returns:
            List of mission-entity relationships matching the filters

        Raises:
            SQLAlchemyError: If database operation fails
        """
        return self.mission_entities.list(**filters)

    def create_ontology(self, ontology: Ontology) -> Ontology:
        """Create a new ontology.

        Args:
            ontology: The ontology instance to create

        Returns:
            The created ontology with updated fields (e.g., generated ID)

        Raises:
            SQLAlchemyError: If database operation fails
        """
        return self.ontologies.upsert(ontology)

    def read_ontology(self, id: UUID) -> Ontology | None:
        """Read an ontology by ID.

        Args:
            id: The UUID of the ontology to read

        Returns:
            The ontology if found, None otherwise

        Raises:
            SQLAlchemyError: If database operation fails
        """
        return self.ontologies.read(id)

    def update_ontology(self, ontology: Ontology) -> Ontology:
        """Update an existing ontology.

        Args:
            ontology: The ontology instance with updated fields

        Returns:
            The updated ontology

        Raises:
            ValueError: If ontology with the given ID is not found
            SQLAlchemyError: If database operation fails
        """
        return self.ontologies.update(ontology)

    def delete_ontology(self, id: UUID) -> bool:
        """Delete an ontology by ID.

        Args:
            id: The UUID of the ontology to delete

        Returns:
            True if the ontology was deleted, False if it didn't exist

        Raises:
            SQLAlchemyError: If database operation fails
        """
        return self.ontologies.delete(id)

    def list_ontologies(self, **filters: Any) -> list[Ontology]:  # noqa: ANN401
        """List ontologies with optional filters.

        Args:
            **filters: Keyword arguments where keys are field names and values are filter values

        Returns:
            List of ontologies matching the filters

        Raises:
            SQLAlchemyError: If database operation fails
        """
        return self.ontologies.list(**filters)

    def create_ontology_class(self, ontology_class: OntologyClass) -> OntologyClass:
        """Create a new ontology class.

        Args:
            ontology_class: The ontology class instance to create

        Returns:
            The created ontology class with updated fields (e.g., generated ID)

        Raises:
            SQLAlchemyError: If database operation fails
        """
        return self.ontology_classes.upsert(ontology_class)

    def read_ontology_class(self, id: UUID) -> OntologyClass | None:
        """Read an ontology class by ID.

        Args:
            id: The UUID of the ontology class to read

        Returns:
            The ontology class if found, None otherwise

        Raises:
            SQLAlchemyError: If database operation fails
        """
        return self.ontology_classes.read(id)

    def update_ontology_class(self, ontology_class: OntologyClass) -> OntologyClass:
        """Update an existing ontology class.

        Args:
            ontology_class: The ontology class instance with updated fields

        Returns:
            The updated ontology class

        Raises:
            ValueError: If ontology class with the given ID is not found
            SQLAlchemyError: If database operation fails
        """
        return self.ontology_classes.update(ontology_class)

    def delete_ontology_class(self, id: UUID) -> bool:
        """Delete an ontology class by ID.

        Args:
            id: The UUID of the ontology class to delete

        Returns:
            True if the ontology class was deleted, False if it didn't exist

        Raises:
            SQLAlchemyError: If database operation fails
        """
        return self.ontology_classes.delete(id)

    def list_ontology_classes(self, **filters: Any) -> list[OntologyClass]:  # noqa: ANN401
        """List ontology classes with optional filters.

        Args:
            **filters: Keyword arguments where keys are field names and values are filter values

        Returns:
            List of ontology classes matching the filters

        Raises:
            SQLAlchemyError: If database operation fails
        """
        return self.ontology_classes.list(**filters)

    # BeamgramSpecification operations
    def create_beamgram_specification(self, beamgram_specification: BeamgramSpecification) -> BeamgramSpecification:
        """Create a new beamgram specification.

        Args:
            beamgram_specification: The beamgram specification instance to create

        Returns:
            The created beamgram specification with updated fields (e.g., generated ID)

        Raises:
            SQLAlchemyError: If database operation fails
        """
        return self.beamgram_specifications.upsert(beamgram_specification)

    def create_or_update_beamgram_specification(
        self, beamgram_specification: BeamgramSpecification
    ) -> BeamgramSpecification:
        """Create a new beamgram specification or update if it already exists.

        Args:
            beamgram_specification: The beamgram specification instance to create or update

        Returns:
            The created or updated beamgram specification

        Raises:
            SQLAlchemyError: If database operation fails
        """
        return self.beamgram_specifications.upsert(beamgram_specification)

    def read_beamgram_specification(self, id: UUID) -> BeamgramSpecification | None:
        """Read a beamgram specification by ID.

        Args:
            id: The UUID of the beamgram specification to read

        Returns:
            The beamgram specification if found, None otherwise

        Raises:
            SQLAlchemyError: If database operation fails
        """
        return self.beamgram_specifications.read(id)

    def update_beamgram_specification(self, beamgram_specification: BeamgramSpecification) -> BeamgramSpecification:
        """Update an existing beamgram specification.

        Args:
            beamgram_specification: The beamgram specification instance with updated fields

        Returns:
            The updated beamgram specification

        Raises:
            ValueError: If beamgram specification with the given ID is not found
            SQLAlchemyError: If database operation fails
        """
        return self.beamgram_specifications.update(beamgram_specification)

    def delete_beamgram_specification(self, id: UUID) -> bool:
        """Delete a beamgram specification by ID.

        Args:
            id: The UUID of the beamgram specification to delete

        Returns:
            True if the beamgram specification was deleted, False if it didn't exist

        Raises:
            SQLAlchemyError: If database operation fails
        """
        return self.beamgram_specifications.delete(id)

    def list_beamgram_specifications(self, **filters: Any) -> list[BeamgramSpecification]:  # noqa: ANN401
        """List beamgram specifications with optional filters.

        Args:
            **filters: Keyword arguments where keys are field names and values are filter values

        Returns:
            List of beamgram specifications matching the filters

        Raises:
            SQLAlchemyError: If database operation fails
        """
        return self.beamgram_specifications.list(**filters)

    # BearingTimeRecordSpecification operations
    def create_bearing_time_record_specification(
        self, bearing_time_record_specification: BearingTimeRecordSpecification
    ) -> BearingTimeRecordSpecification:
        """Create a new bearing-time record specification.

        Args:
            bearing_time_record_specification: The bearing-time record specification instance to create

        Returns:
            The created bearing-time record specification with updated fields (e.g., generated ID)

        Raises:
            SQLAlchemyError: If database operation fails
        """
        return self.bearing_time_record_specifications.upsert(bearing_time_record_specification)

    def create_or_update_bearing_time_record_specification(
        self, bearing_time_record_specification: BearingTimeRecordSpecification
    ) -> BearingTimeRecordSpecification:
        """Create a new bearing-time record specification or update if it already exists.

        Args:
            bearing_time_record_specification: The bearing-time record specification instance to create or update

        Returns:
            The created or updated bearing-time record specification

        Raises:
            SQLAlchemyError: If database operation fails
        """
        return self.bearing_time_record_specifications.upsert(bearing_time_record_specification)

    def read_bearing_time_record_specification(self, id: UUID) -> BearingTimeRecordSpecification | None:
        """Read a bearing-time record specification by ID.

        Args:
            id: The UUID of the bearing-time record specification to read

        Returns:
            The bearing-time record specification if found, None otherwise

        Raises:
            SQLAlchemyError: If database operation fails
        """
        return self.bearing_time_record_specifications.read(id)

    def update_bearing_time_record_specification(
        self, bearing_time_record_specification: BearingTimeRecordSpecification
    ) -> BearingTimeRecordSpecification:
        """Update an existing bearing-time record specification.

        Args:
            bearing_time_record_specification: The bearing-time record specification instance with updated fields

        Returns:
            The updated bearing-time record specification

        Raises:
            ValueError: If bearing-time record specification with the given ID is not found
            SQLAlchemyError: If database operation fails
        """
        return self.bearing_time_record_specifications.update(bearing_time_record_specification)

    def delete_bearing_time_record_specification(self, id: UUID) -> bool:
        """Delete a bearing-time record specification by ID.

        Args:
            id: The UUID of the bearing-time record specification to delete

        Returns:
            True if the bearing-time record specification was deleted, False if it didn't exist

        Raises:
            SQLAlchemyError: If database operation fails
        """
        return self.bearing_time_record_specifications.delete(id)

    def list_bearing_time_record_specifications(self, **filters: Any) -> list[BearingTimeRecordSpecification]:  # noqa: ANN401
        """List bearing-time record specifications with optional filters.

        Args:
            **filters: Keyword arguments where keys are field names and values are filter values

        Returns:
            List of bearing-time record specifications matching the filters

        Raises:
            SQLAlchemyError: If database operation fails
        """
        return self.bearing_time_record_specifications.list(**filters)

    # Iceberg operations removed after v0.3.6. buffer_name parameter is deprecated and will be removed in v0.5.0
    def create_data_row(self, data_row: DataRow, buffer_name: str | None = None) -> DataRow:  # noqa: ARG002
        """Create a new data row in data_row table.

        Args:
            data_row: The data row instance to create
            buffer_name: (DEPRECATED) Optional buffer name for batching writes

        Returns:
            The data row instance (unchanged)

        Raises:
            CommitFailedException: If write operation fails after retries
        """
        return self.data_rows.insert(data_row)

    def create_data_row_batch(self, data_rows: list[DataRow], buffer_name: str | None = None) -> list[DataRow]:  # noqa: ARG002
        """Create a new data row batch in data_row table.

        Args:
            data_rows: The list of data row instances to create
            buffer_name: (DEPRECATED) Optional buffer name for batching writes

        Returns:
            The data row instance (unchanged)

        Raises:
            CommitFailedException: If write operation fails after retries
        """
        return self.data_rows.insert_batch(data_rows)

    def list_data_rows(self, **filters: Any) -> list[DataRow]:  # noqa: ANN401
        """List data rows with optional filters from Iceberg table.

        Args:
            **filters: Iceberg scan parameters including:

        Returns:
            List of data rows matching the filters

        Raises:
            Exception: If Iceberg scan operation fails
        """
        return self.data_rows.list(**filters)

    # Iceberg operations removed after v0.3.6. buffer_name parameter is deprecated and will be removed in v0.5.0
    def create_metadata_row(self, metadata_row: MetadataRow, buffer_name: str | None = None) -> MetadataRow:  # noqa: ARG002
        """Create a new metadata row in Iceberg table.

        Args:
            metadata_row: The metadata row instance to create
            buffer_name: (DEPRECATED) Optional buffer name for batching writes

        Returns:
            The metadata row instance (unchanged)

        Raises:
            CommitFailedException: If write operation fails after retries
        """
        return self.metadata_rows.insert(metadata_row)

    def list_metadata_rows(self, **filters: Any) -> list[MetadataRow]:  # noqa: ANN401
        """List metadata rows with optional filters from Iceberg table.

        Args:
            **filters: Postgres query values parameters including:

        Returns:
            List of metadata rows matching the filters

        Raises:
            Exception: If Iceberg scan operation fails
        """
        return self.metadata_rows.list(**filters)
