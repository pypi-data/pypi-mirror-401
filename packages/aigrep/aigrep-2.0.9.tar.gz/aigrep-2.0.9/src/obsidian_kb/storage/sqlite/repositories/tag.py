"""Tag repository for SQLite storage.

This module provides repository for managing tags and document-tag
relationships in SQLite. Supports frontmatter and inline tags.
"""

import logging
from dataclasses import dataclass
from typing import Any

from obsidian_kb.storage.sqlite.manager import SQLiteManager
from obsidian_kb.storage.sqlite.repositories.base import BaseRepository

logger = logging.getLogger(__name__)


@dataclass
class Tag:
    """Tag entity for SQLite storage.

    Represents a unique tag within a vault.

    Attributes:
        id: Database primary key (None for new entities)
        vault_id: Foreign key to vaults table
        name: Normalized tag name (without #)
        tag_type: Type of tag (frontmatter or inline)
        document_count: Number of documents with this tag
    """

    vault_id: int
    name: str
    tag_type: str = "frontmatter"
    document_count: int = 0
    id: int | None = None


@dataclass
class DocumentTag:
    """Document-tag relationship entity.

    Represents the many-to-many relationship between documents and tags.

    Attributes:
        id: Database primary key (None for new entities)
        document_id: Foreign key to documents table
        tag_id: Foreign key to tags table
        occurrence_count: How many times tag appears in document
    """

    document_id: int
    tag_id: int
    occurrence_count: int = 1
    id: int | None = None


class TagRepository(BaseRepository[Tag]):
    """Repository for tag operations in SQLite.

    Provides CRUD operations and specialized queries for tags,
    including document filtering by tags.

    Usage:
        repo = TagRepository(manager)

        # Get or create tag
        tag_id = await repo.get_or_create(vault_id, "ai", "frontmatter")

        # Find documents by tag
        doc_ids = await repo.find_documents_by_tag(vault_id, "ai")

        # Get all tags in vault
        tags = await repo.get_vault_tags(vault_id)
    """

    table_name = "tags"

    def __init__(self, manager: SQLiteManager) -> None:
        """Initialize tag repository.

        Args:
            manager: SQLiteManager instance
        """
        super().__init__(manager)

    def _row_to_entity(self, row: dict[str, Any]) -> Tag:
        """Convert database row to Tag entity."""
        return Tag(
            id=row["id"],
            vault_id=row["vault_id"],
            name=row["name"],
            tag_type=row.get("tag_type", "frontmatter"),
            document_count=row.get("document_count", 0),
        )

    def _entity_to_row(self, entity: Tag) -> dict[str, Any]:
        """Convert Tag entity to database row."""
        return {
            "vault_id": entity.vault_id,
            "name": entity.name,
            "tag_type": entity.tag_type,
            "document_count": entity.document_count,
        }

    # =========================================================================
    # Tag operations
    # =========================================================================

    async def get_or_create(
        self,
        vault_id: int,
        name: str,
        tag_type: str = "frontmatter",
    ) -> int:
        """Get existing tag or create new one.

        Args:
            vault_id: Vault database ID
            name: Tag name (without #)
            tag_type: Tag type (frontmatter or inline)

        Returns:
            Tag database ID
        """
        # Normalize tag name
        normalized_name = name.lower().strip().lstrip("#")

        # Try to find existing
        existing = await self.find_one(
            "vault_id = ? AND name = ? AND tag_type = ?",
            (vault_id, normalized_name, tag_type),
        )
        if existing and existing.id:
            return existing.id

        # Create new
        tag = Tag(
            vault_id=vault_id,
            name=normalized_name,
            tag_type=tag_type,
            document_count=0,
        )
        return await self.create(tag)

    async def get_by_name(
        self,
        vault_id: int,
        name: str,
        tag_type: str | None = None,
    ) -> Tag | None:
        """Get tag by name.

        Args:
            vault_id: Vault database ID
            name: Tag name (without #)
            tag_type: Optional tag type filter

        Returns:
            Tag if found, None otherwise
        """
        normalized_name = name.lower().strip().lstrip("#")

        if tag_type:
            return await self.find_one(
                "vault_id = ? AND name = ? AND tag_type = ?",
                (vault_id, normalized_name, tag_type),
            )
        else:
            return await self.find_one(
                "vault_id = ? AND name = ?",
                (vault_id, normalized_name),
            )

    async def get_vault_tags(
        self,
        vault_id: int,
        tag_type: str | None = None,
    ) -> list[Tag]:
        """Get all tags in a vault.

        Args:
            vault_id: Vault database ID
            tag_type: Optional filter by tag type

        Returns:
            List of tags
        """
        if tag_type:
            return await self.find_many(
                "vault_id = ? AND tag_type = ?",
                (vault_id, tag_type),
                order_by="name",
            )
        else:
            return await self.find_many(
                "vault_id = ?",
                (vault_id,),
                order_by="name",
            )

    async def update_document_count(self, tag_id: int) -> None:
        """Update document count for a tag.

        Args:
            tag_id: Tag database ID
        """
        await self._manager.execute(
            """
            UPDATE tags
            SET document_count = (
                SELECT COUNT(DISTINCT document_id)
                FROM document_tags
                WHERE tag_id = ?
            )
            WHERE id = ?
            """,
            (tag_id, tag_id),
        )

    async def delete_by_vault(self, vault_id: int) -> int:
        """Delete all tags for a vault.

        Args:
            vault_id: Vault database ID

        Returns:
            Number of deleted tags
        """
        return await self.delete_where("vault_id = ?", (vault_id,))

    # =========================================================================
    # Document-tag relationship operations
    # =========================================================================

    async def add_document_tag(
        self,
        document_id: int,
        tag_id: int,
        occurrence_count: int = 1,
    ) -> int:
        """Add tag to document.

        If relationship exists, updates occurrence count.

        Args:
            document_id: Document database ID
            tag_id: Tag database ID
            occurrence_count: How many times tag appears

        Returns:
            DocumentTag database ID
        """
        # Use INSERT OR REPLACE for upsert
        cursor = await self._manager.execute(
            """
            INSERT INTO document_tags (document_id, tag_id, occurrence_count)
            VALUES (?, ?, ?)
            ON CONFLICT(document_id, tag_id) DO UPDATE SET
                occurrence_count = excluded.occurrence_count
            """,
            (document_id, tag_id, occurrence_count),
        )
        return cursor.lastrowid or 0

    async def remove_document_tag(
        self,
        document_id: int,
        tag_id: int,
    ) -> bool:
        """Remove tag from document.

        Args:
            document_id: Document database ID
            tag_id: Tag database ID

        Returns:
            True if relationship was deleted
        """
        cursor = await self._manager.execute(
            "DELETE FROM document_tags WHERE document_id = ? AND tag_id = ?",
            (document_id, tag_id),
        )
        return cursor.rowcount > 0

    async def remove_document_tags(self, document_id: int) -> int:
        """Remove all tags from a document.

        Args:
            document_id: Document database ID

        Returns:
            Number of removed relationships
        """
        cursor = await self._manager.execute(
            "DELETE FROM document_tags WHERE document_id = ?",
            (document_id,),
        )
        return cursor.rowcount

    async def get_document_tags(self, document_id: int) -> list[Tag]:
        """Get all tags for a document.

        Args:
            document_id: Document database ID

        Returns:
            List of tags
        """
        rows = await self._manager.fetch_all(
            """
            SELECT t.*
            FROM tags t
            JOIN document_tags dt ON t.id = dt.tag_id
            WHERE dt.document_id = ?
            ORDER BY t.name
            """,
            (document_id,),
        )
        return [self._row_to_entity(row) for row in rows]

    # =========================================================================
    # Search operations
    # =========================================================================

    async def find_documents_by_tag(
        self,
        vault_id: int,
        tag_name: str,
        tag_type: str | None = None,
    ) -> list[int]:
        """Find document IDs with a specific tag.

        Args:
            vault_id: Vault database ID
            tag_name: Tag name (without #)
            tag_type: Optional filter by tag type

        Returns:
            List of document IDs
        """
        normalized_name = tag_name.lower().strip().lstrip("#")

        if tag_type:
            rows = await self._manager.fetch_all(
                """
                SELECT DISTINCT dt.document_id
                FROM document_tags dt
                JOIN tags t ON dt.tag_id = t.id
                WHERE t.vault_id = ?
                  AND t.name = ?
                  AND t.tag_type = ?
                """,
                (vault_id, normalized_name, tag_type),
            )
        else:
            rows = await self._manager.fetch_all(
                """
                SELECT DISTINCT dt.document_id
                FROM document_tags dt
                JOIN tags t ON dt.tag_id = t.id
                WHERE t.vault_id = ?
                  AND t.name = ?
                """,
                (vault_id, normalized_name),
            )

        return [row["document_id"] for row in rows]

    async def find_documents_by_tags(
        self,
        vault_id: int,
        tag_names: list[str],
        match_all: bool = False,
    ) -> list[int]:
        """Find document IDs with multiple tags.

        Args:
            vault_id: Vault database ID
            tag_names: List of tag names (without #)
            match_all: If True, document must have all tags (AND logic)
                      If False, document can have any tag (OR logic)

        Returns:
            List of document IDs
        """
        if not tag_names:
            return []

        normalized_names = [
            name.lower().strip().lstrip("#") for name in tag_names
        ]
        placeholders = ", ".join("?" * len(normalized_names))

        if match_all:
            # Document must have ALL tags
            rows = await self._manager.fetch_all(
                f"""
                SELECT dt.document_id
                FROM document_tags dt
                JOIN tags t ON dt.tag_id = t.id
                WHERE t.vault_id = ?
                  AND t.name IN ({placeholders})
                GROUP BY dt.document_id
                HAVING COUNT(DISTINCT t.name) = ?
                """,
                (vault_id, *normalized_names, len(normalized_names)),
            )
        else:
            # Document can have ANY tag
            rows = await self._manager.fetch_all(
                f"""
                SELECT DISTINCT dt.document_id
                FROM document_tags dt
                JOIN tags t ON dt.tag_id = t.id
                WHERE t.vault_id = ?
                  AND t.name IN ({placeholders})
                """,
                (vault_id, *normalized_names),
            )

        return [row["document_id"] for row in rows]

    async def find_documents_by_tag_pattern(
        self,
        vault_id: int,
        pattern: str,
    ) -> list[int]:
        """Find documents with tags matching a pattern.

        Args:
            vault_id: Vault database ID
            pattern: SQL LIKE pattern (e.g., "project/%")

        Returns:
            List of document IDs
        """
        rows = await self._manager.fetch_all(
            """
            SELECT DISTINCT dt.document_id
            FROM document_tags dt
            JOIN tags t ON dt.tag_id = t.id
            WHERE t.vault_id = ?
              AND t.name LIKE ?
            """,
            (vault_id, pattern),
        )
        return [row["document_id"] for row in rows]

    # =========================================================================
    # Aggregation operations
    # =========================================================================

    async def get_tag_counts(
        self,
        vault_id: int,
        limit: int = 100,
    ) -> list[tuple[str, int]]:
        """Get tags with document counts.

        Args:
            vault_id: Vault database ID
            limit: Maximum number of tags to return

        Returns:
            List of (tag_name, document_count) tuples
        """
        rows = await self._manager.fetch_all(
            """
            SELECT t.name, COUNT(DISTINCT dt.document_id) as count
            FROM tags t
            LEFT JOIN document_tags dt ON t.id = dt.tag_id
            WHERE t.vault_id = ?
            GROUP BY t.id, t.name
            ORDER BY count DESC, t.name
            LIMIT ?
            """,
            (vault_id, limit),
        )
        return [(row["name"], row["count"]) for row in rows]

    async def get_unique_tag_names(self, vault_id: int) -> list[str]:
        """Get all unique tag names in a vault.

        Args:
            vault_id: Vault database ID

        Returns:
            List of unique tag names
        """
        rows = await self._manager.fetch_all(
            """
            SELECT DISTINCT name
            FROM tags
            WHERE vault_id = ?
            ORDER BY name
            """,
            (vault_id,),
        )
        return [row["name"] for row in rows]
