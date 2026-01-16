#!/usr/bin/env python3
"""DEPRECATED: Скрипт миграции created_at для HOTFIX v2.0.7.1.

⚠️ ВНИМАНИЕ: Этот скрипт предназначен ТОЛЬКО для миграции с v2.0.7.1.
После обновления до v2.0.8+ этот скрипт больше не нужен.

Заменяет все пустые created_at на modified_at в таблице documents.

Использование:
    .venv/bin/python scripts/migrate_created_at.py --vault-name "My Vault" --db-path ~/.obsidian-kb

Опционально можно указать --dry-run для просмотра изменений без их применения.
"""

import argparse
import asyncio
import logging
from pathlib import Path

import lancedb
import pyarrow as pa

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def normalize_vault_name(vault_name: str) -> str:
    """Нормализация имени vault'а для использования в именах таблиц."""
    import re
    safe_name = re.sub(r"[^a-zA-Z0-9_\-.]", "_", vault_name)
    safe_name = re.sub(r"_+", "_", safe_name)
    safe_name = safe_name.strip("_")
    return safe_name


def get_table_name(vault_name: str) -> str:
    """Получение имени таблицы documents."""
    safe_name = normalize_vault_name(vault_name)
    return f"vault_{safe_name}_documents"


def migrate_created_at(db_path: Path, vault_name: str, dry_run: bool = False) -> dict:
    """Миграция пустых created_at в таблице documents.

    Args:
        db_path: Путь к директории LanceDB
        vault_name: Имя vault'а
        dry_run: Если True, только показать что будет изменено

    Returns:
        Статистика миграции
    """
    lancedb_path = db_path / "lancedb"
    if not lancedb_path.exists():
        logger.error(f"LanceDB directory not found: {lancedb_path}")
        return {"error": "LanceDB not found", "migrated": 0}

    db = lancedb.connect(str(lancedb_path))
    table_name = get_table_name(vault_name)

    try:
        table = db.open_table(table_name)
    except Exception as e:
        logger.error(f"Table {table_name} not found: {e}")
        return {"error": f"Table not found: {e}", "migrated": 0}

    # Читаем все записи
    arrow_table = table.to_arrow()
    rows = arrow_table.to_pylist()

    if not rows:
        logger.info(f"Table {table_name} is empty")
        return {"total": 0, "empty_created_at": 0, "migrated": 0}

    # Находим записи с пустым created_at
    empty_created_at = []
    for row in rows:
        created_at = row.get("created_at", "")
        if not created_at or created_at == "":
            empty_created_at.append(row)

    logger.info(f"Found {len(empty_created_at)} documents with empty created_at (total: {len(rows)})")

    if not empty_created_at:
        return {"total": len(rows), "empty_created_at": 0, "migrated": 0}

    if dry_run:
        logger.info("DRY RUN - showing first 10 documents to be migrated:")
        for row in empty_created_at[:10]:
            doc_id = row.get("document_id", "unknown")
            modified_at = row.get("modified_at", "")
            logger.info(f"  {doc_id}: created_at='' -> '{modified_at}'")
        if len(empty_created_at) > 10:
            logger.info(f"  ... and {len(empty_created_at) - 10} more")
        return {"total": len(rows), "empty_created_at": len(empty_created_at), "migrated": 0}

    # Обновляем записи
    updated_rows = []
    for row in rows:
        created_at = row.get("created_at", "")
        if not created_at or created_at == "":
            modified_at = row.get("modified_at", "")
            if modified_at:
                row["created_at"] = modified_at
                updated_rows.append(row["document_id"])

    # Записываем обновленные данные
    # LanceDB не поддерживает UPDATE, поэтому пересоздаем таблицу
    schema = arrow_table.schema
    new_arrow_table = pa.Table.from_pylist(rows, schema=schema)

    # Удаляем и пересоздаем таблицу
    db.drop_table(table_name)
    db.create_table(table_name, new_arrow_table)

    logger.info(f"Migrated {len(updated_rows)} documents")

    return {
        "total": len(rows),
        "empty_created_at": len(empty_created_at),
        "migrated": len(updated_rows),
    }


def list_vaults(db_path: Path) -> list[str]:
    """Получение списка всех vault'ов в LanceDB."""
    lancedb_path = db_path / "lancedb"
    if not lancedb_path.exists():
        return []

    db = lancedb.connect(str(lancedb_path))
    tables = db.table_names()

    vaults = set()
    for table in tables:
        if table.startswith("vault_") and "_documents" in table:
            # vault_My_Vault_documents -> My_Vault
            parts = table.replace("vault_", "", 1).rsplit("_documents", 1)
            if parts:
                vaults.add(parts[0])

    return sorted(vaults)


def main():
    parser = argparse.ArgumentParser(
        description="Migrate empty created_at fields to modified_at in LanceDB"
    )
    parser.add_argument(
        "--vault-name",
        type=str,
        help="Name of the vault to migrate (or 'all' for all vaults)",
    )
    parser.add_argument(
        "--db-path",
        type=str,
        default="~/.obsidian-kb",
        help="Path to obsidian-kb data directory (default: ~/.obsidian-kb)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be migrated without making changes",
    )
    parser.add_argument(
        "--list-vaults",
        action="store_true",
        help="List all available vaults and exit",
    )

    args = parser.parse_args()
    db_path = Path(args.db_path).expanduser()

    if args.list_vaults:
        vaults = list_vaults(db_path)
        if vaults:
            logger.info(f"Found {len(vaults)} vault(s):")
            for vault in vaults:
                logger.info(f"  - {vault}")
        else:
            logger.info("No vaults found")
        return

    if not args.vault_name:
        parser.error("--vault-name is required (or use --list-vaults)")

    if args.vault_name.lower() == "all":
        vaults = list_vaults(db_path)
        if not vaults:
            logger.error("No vaults found to migrate")
            return

        total_stats = {"total": 0, "empty_created_at": 0, "migrated": 0}
        for vault in vaults:
            logger.info(f"\n=== Migrating vault: {vault} ===")
            stats = migrate_created_at(db_path, vault, args.dry_run)
            if "error" not in stats:
                total_stats["total"] += stats["total"]
                total_stats["empty_created_at"] += stats["empty_created_at"]
                total_stats["migrated"] += stats["migrated"]

        logger.info(f"\n=== Total ===")
        logger.info(f"Documents: {total_stats['total']}")
        logger.info(f"Empty created_at: {total_stats['empty_created_at']}")
        logger.info(f"Migrated: {total_stats['migrated']}")
    else:
        stats = migrate_created_at(db_path, args.vault_name, args.dry_run)
        if "error" not in stats:
            logger.info(f"\n=== Summary ===")
            logger.info(f"Documents: {stats['total']}")
            logger.info(f"Empty created_at: {stats['empty_created_at']}")
            logger.info(f"Migrated: {stats['migrated']}")


if __name__ == "__main__":
    main()
