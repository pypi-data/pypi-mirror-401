"""Tests for dual-write functionality (v2.0.7).

Tests the SQLite dual-write feature in IndexingService:
- Documents are written to both LanceDB and SQLite
- Properties are synchronized
- Deletes propagate to both databases
- Consistency check works correctly
"""

import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from obsidian_kb.config import settings

# v2.0.8: Use dynamic dimensions from settings
EMBED_DIM = settings.embedding_dimensions
import pytest_asyncio

from obsidian_kb.core.connection_manager import DBConnectionManager
from obsidian_kb.storage.indexing.indexing_service import IndexingService
from obsidian_kb.storage.sqlite.manager import SQLiteManager
from obsidian_kb.storage.sqlite.schema import create_schema
from obsidian_kb.types import DocumentChunk


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test databases."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def lancedb_path(temp_dir):
    """Path for LanceDB test database."""
    return temp_dir / "lancedb"


@pytest.fixture
def sqlite_path(temp_dir):
    """Path for SQLite test database."""
    return temp_dir / "metadata.db"


@pytest_asyncio.fixture
async def sqlite_manager(sqlite_path):
    """Create and initialize SQLite manager."""
    manager = SQLiteManager(db_path=sqlite_path)
    await manager.initialize()
    await create_schema(manager)
    yield manager
    await manager.close()


@pytest.fixture
def connection_manager(lancedb_path):
    """Create LanceDB connection manager."""
    DBConnectionManager.reset_instance()
    manager = DBConnectionManager.get_instance(lancedb_path)
    yield manager
    DBConnectionManager.reset_instance()


@pytest_asyncio.fixture
async def indexing_service(connection_manager, sqlite_manager):
    """Create IndexingService with dual-write enabled."""
    return IndexingService(
        connection_manager=connection_manager,
        sqlite_manager=sqlite_manager,
    )


@pytest.fixture
def indexing_service_no_sqlite(connection_manager):
    """Create IndexingService without SQLite (legacy mode)."""
    return IndexingService(
        connection_manager=connection_manager,
        sqlite_manager=None,
    )


@pytest.fixture
def sample_chunks():
    """Create sample document chunks for testing."""
    now = datetime.now()
    return [
        DocumentChunk(
            id="test_vault::doc1.md::0",
            vault_name="test_vault",
            file_path="doc1.md",
            title="Document 1",
            section="",
            content="This is the content of document 1.",
            tags=["status:active", "tag1"],
            links=["doc2"],
            inline_tags=["tag1"],
            frontmatter_tags=["status:active"],
            metadata={"status": "active", "priority": 1},
            created_at=now,
            modified_at=now,
        ),
        DocumentChunk(
            id="test_vault::doc1.md::1",
            vault_name="test_vault",
            file_path="doc1.md",
            title="Document 1",
            section="Section 1",
            content="This is section 1 of document 1.",
            tags=["status:active"],
            links=[],
            inline_tags=[],
            frontmatter_tags=["status:active"],
            metadata={"status": "active", "priority": 1},
            created_at=now,
            modified_at=now,
        ),
        DocumentChunk(
            id="test_vault::doc2.md::0",
            vault_name="test_vault",
            file_path="doc2.md",
            title="Document 2",
            section="",
            content="This is the content of document 2.",
            tags=["status:draft", "tag2"],
            links=["doc1"],
            inline_tags=["tag2"],
            frontmatter_tags=["status:draft"],
            metadata={"status": "draft", "priority": 2},
            created_at=now,
            modified_at=now,
        ),
    ]


@pytest.fixture
def sample_embeddings():
    """Create sample embeddings (default dimension EMBED_DIM)."""
    from obsidian_kb.config import settings
    dim = settings.embedding_dimensions
    return [
        [0.1] * dim,
        [0.2] * dim,
        [0.3] * dim,
    ]


async def mock_retry_with_backoff(coro, **kwargs):
    """Mock retry_with_backoff that properly awaits the coroutine."""
    return await coro()


class TestDualWriteUpsert:
    """Tests for upsert_chunks with dual-write."""

    @pytest.mark.asyncio
    async def test_upsert_writes_to_both_databases(
        self,
        indexing_service,
        sample_chunks,
        sample_embeddings,
        sqlite_manager,
    ):
        """Verify that upsert_chunks writes to both LanceDB and SQLite."""
        vault_name = "test_vault"

        with patch(
            "obsidian_kb.service_container.get_service_container"
        ) as mock_container:
            mock_recovery = MagicMock()
            mock_recovery.retry_with_backoff = mock_retry_with_backoff
            mock_container.return_value.recovery_service = mock_recovery

            await indexing_service.upsert_chunks(
                vault_name, sample_chunks, sample_embeddings
            )

        # Verify SQLite has the documents
        from obsidian_kb.storage.sqlite.repositories.document import (
            SQLiteDocumentRepository,
        )
        from obsidian_kb.storage.sqlite.repositories.vault import VaultRepository

        vault_repo = VaultRepository(sqlite_manager)
        vault = await vault_repo.get_by_name(vault_name)
        assert vault is not None
        assert vault.id is not None

        doc_repo = SQLiteDocumentRepository(sqlite_manager)
        docs = await doc_repo.find_by_vault(vault.id)

        # Should have 2 unique documents (doc1.md and doc2.md)
        assert len(docs) == 2
        doc_paths = {d.file_path for d in docs}
        assert doc_paths == {"doc1.md", "doc2.md"}

    @pytest.mark.asyncio
    async def test_upsert_without_sqlite_manager(
        self,
        indexing_service_no_sqlite,
        sample_chunks,
        sample_embeddings,
    ):
        """Verify upsert works when SQLite manager is not configured."""
        vault_name = "test_vault"

        with patch(
            "obsidian_kb.service_container.get_service_container"
        ) as mock_container:
            mock_recovery = MagicMock()
            mock_recovery.retry_with_backoff = mock_retry_with_backoff
            mock_container.return_value.recovery_service = mock_recovery

            # Should not raise an error
            await indexing_service_no_sqlite.upsert_chunks(
                vault_name, sample_chunks, sample_embeddings
            )

    @pytest.mark.asyncio
    async def test_sqlite_error_does_not_block_lancedb(
        self,
        connection_manager,
        sample_chunks,
        sample_embeddings,
    ):
        """Verify that SQLite errors don't block LanceDB operations."""
        vault_name = "test_vault"

        # Create a mock SQLite manager that always fails
        mock_sqlite = MagicMock()
        mock_sqlite.initialize = MagicMock()

        service = IndexingService(
            connection_manager=connection_manager,
            sqlite_manager=mock_sqlite,
        )
        service._sqlite_initialized = True

        # Make SQLite operations fail
        with patch.object(
            service, "_write_documents_to_sqlite", side_effect=Exception("SQLite error")
        ):
            with patch(
                "obsidian_kb.service_container.get_service_container"
            ) as mock_container:
                mock_recovery = MagicMock()
                mock_recovery.retry_with_backoff = mock_retry_with_backoff
                mock_container.return_value.recovery_service = mock_recovery

                # Should not raise - SQLite errors are non-blocking
                await service.upsert_chunks(
                    vault_name, sample_chunks, sample_embeddings
                )


class TestDualWriteDelete:
    """Tests for delete operations with dual-write."""

    @pytest.mark.asyncio
    async def test_delete_file_removes_from_both(
        self,
        indexing_service,
        sample_chunks,
        sample_embeddings,
        sqlite_manager,
    ):
        """Verify delete_file removes from both LanceDB and SQLite."""
        vault_name = "test_vault"

        # First, insert the documents
        with patch(
            "obsidian_kb.service_container.get_service_container"
        ) as mock_container:
            mock_recovery = MagicMock()
            mock_recovery.retry_with_backoff = mock_retry_with_backoff
            mock_container.return_value.recovery_service = mock_recovery

            await indexing_service.upsert_chunks(
                vault_name, sample_chunks, sample_embeddings
            )

        # Delete one document
        await indexing_service.delete_file(vault_name, "doc1.md")

        # Verify SQLite no longer has doc1.md
        from obsidian_kb.storage.sqlite.repositories.document import (
            SQLiteDocumentRepository,
        )

        doc_repo = SQLiteDocumentRepository(sqlite_manager)
        doc = await doc_repo.get_by_document_id(f"{vault_name}::doc1.md")
        assert doc is None

        # But doc2.md should still exist
        doc2 = await doc_repo.get_by_document_id(f"{vault_name}::doc2.md")
        assert doc2 is not None

    @pytest.mark.asyncio
    async def test_delete_vault_removes_from_both(
        self,
        indexing_service,
        sample_chunks,
        sample_embeddings,
        sqlite_manager,
    ):
        """Verify delete_vault removes from both LanceDB and SQLite."""
        vault_name = "test_vault"

        # First, insert the documents
        with patch(
            "obsidian_kb.service_container.get_service_container"
        ) as mock_container:
            mock_recovery = MagicMock()
            mock_recovery.retry_with_backoff = mock_retry_with_backoff
            mock_container.return_value.recovery_service = mock_recovery

            await indexing_service.upsert_chunks(
                vault_name, sample_chunks, sample_embeddings
            )

        # Verify vault exists
        from obsidian_kb.storage.sqlite.repositories.vault import VaultRepository

        vault_repo = VaultRepository(sqlite_manager)
        vault = await vault_repo.get_by_name(vault_name)
        assert vault is not None

        # Delete the vault
        await indexing_service.delete_vault(vault_name)

        # Verify vault no longer exists
        vault = await vault_repo.get_by_name(vault_name)
        assert vault is None


class TestConsistencyCheck:
    """Tests for consistency check functionality."""

    @pytest.mark.asyncio
    async def test_consistency_check_empty_vault(self, indexing_service):
        """Consistency check on empty vault returns consistent."""
        report = await indexing_service.check_consistency("empty_vault")

        assert report["is_consistent"] is True
        assert report["lancedb_count"] == 0
        assert report["sqlite_count"] == 0
        assert report["only_in_lancedb"] == []
        assert report["only_in_sqlite"] == []
        assert report["hash_mismatches"] == []

    @pytest.mark.asyncio
    async def test_consistency_check_after_upsert(
        self,
        indexing_service,
        sample_chunks,
        sample_embeddings,
    ):
        """Consistency check passes after successful upsert."""
        vault_name = "test_vault"

        with patch(
            "obsidian_kb.service_container.get_service_container"
        ) as mock_container:
            mock_recovery = MagicMock()
            mock_recovery.retry_with_backoff = mock_retry_with_backoff
            mock_container.return_value.recovery_service = mock_recovery

            await indexing_service.upsert_chunks(
                vault_name, sample_chunks, sample_embeddings
            )

        report = await indexing_service.check_consistency(vault_name)

        assert report["is_consistent"] is True
        assert report["lancedb_count"] == 2
        assert report["sqlite_count"] == 2
        assert report["only_in_lancedb"] == []
        assert report["only_in_sqlite"] == []
        assert report["hash_mismatches"] == []

    @pytest.mark.asyncio
    async def test_consistency_check_without_sqlite(
        self,
        indexing_service_no_sqlite,
        sample_chunks,
        sample_embeddings,
    ):
        """Consistency check handles missing SQLite manager."""
        vault_name = "test_vault"

        with patch(
            "obsidian_kb.service_container.get_service_container"
        ) as mock_container:
            mock_recovery = MagicMock()
            mock_recovery.retry_with_backoff = mock_retry_with_backoff
            mock_container.return_value.recovery_service = mock_recovery

            await indexing_service_no_sqlite.upsert_chunks(
                vault_name, sample_chunks, sample_embeddings
            )

        report = await indexing_service_no_sqlite.check_consistency(vault_name)

        # Without SQLite, LanceDB docs are "only_in_lancedb"
        assert report["is_consistent"] is False
        assert report["lancedb_count"] == 2
        assert report["sqlite_count"] == 0
        assert len(report["only_in_lancedb"]) == 2


class TestVaultStatsUpdate:
    """Tests for vault stats synchronization."""

    @pytest.mark.asyncio
    async def test_vault_stats_updated_on_upsert(
        self,
        indexing_service,
        sample_chunks,
        sample_embeddings,
        sqlite_manager,
    ):
        """Verify vault stats are updated in SQLite after upsert."""
        vault_name = "test_vault"

        with patch(
            "obsidian_kb.service_container.get_service_container"
        ) as mock_container:
            mock_recovery = MagicMock()
            mock_recovery.retry_with_backoff = mock_retry_with_backoff
            mock_container.return_value.recovery_service = mock_recovery

            await indexing_service.upsert_chunks(
                vault_name, sample_chunks, sample_embeddings
            )

        from obsidian_kb.storage.sqlite.repositories.vault import VaultRepository

        vault_repo = VaultRepository(sqlite_manager)
        vault = await vault_repo.get_by_name(vault_name)

        assert vault is not None
        assert vault.document_count == 2  # 2 unique documents
        assert vault.chunk_count == 3  # 3 chunks total
