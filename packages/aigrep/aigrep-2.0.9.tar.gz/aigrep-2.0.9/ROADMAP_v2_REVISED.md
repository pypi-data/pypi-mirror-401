# obsidian-kb Roadmap v2.0 (Revised)

**Дата:** 2026-01-14
**Текущая версия:** 2.0.8
**Основа:** Результаты аудита AUDIT_REPORT.md

---

## Изменения относительно предыдущей версии

### Добавлено

| # | Изменение | Причина |
|---|-----------|---------|
| 1 | P0: Флаг `auto_index_enabled` | Контроль автоиндексации пользователем |
| 2 | P1: Query prefix для embeddings | Улучшение качества asymmetric search |
| 3 | P1: Исправление chunk_size | Баг: символы вместо токенов |

### Убрано

| # | Изменение | Причина |
|---|-----------|---------|
| 1 | Benchmarking Phase | Решение принято: SQLite + LanceDB |
| 2 | sqlite-vec прототип | Используем LanceDB для vectors |
| 3 | Оценка PostgreSQL | Overkill для embedded use case |

### Переприоритизировано

| Задача | Было | Стало | Причина |
|--------|------|-------|---------|
| SQLite миграция | "Исследование" | "Реализация" | Код готов, схема определена |
| NER и entities | P1 | P2 | Фокус на стабильности |
| Graph queries | P1 | P2 | Зависит от SQLite links |

---

## Immediate Fixes (до Release 2.0.7)

Эти исправления можно сделать немедленно без breaking changes.

### P0 — Критические

| # | Задача | Файл | Описание |
|---|--------|------|----------|
| 1 | Добавить `auto_index_enabled: bool = False` | `config.py` | Default OFF для контроля |
| 2 | Документировать auto_index в README | `README.md` | Раздел "Auto-indexing" |

### P1 — Важные

| # | Задача | Файл | Описание |
|---|--------|------|----------|
| 3 | Исправить chunk_size | `config.py`, `chunking.py` | Символы → токены |
| 4 | Добавить query prefix | `embedding_service.py` | "query:" для asymmetric |

---

## Release 2.0.7 — SQLite Migration (Phase 1: Dual-Write)

**Цель:** Переключить metadata на SQLite, оставить vectors в LanceDB

### Architecture Overview

```
BEFORE (v2.0.6):
┌─────────────────────────────────────────────────────────────┐
│                        LanceDB                               │
│  ┌──────────────┐ ┌──────────────┐ ┌────────────────────────┐│
│  │  documents   │ │   chunks     │ │ document_properties    ││
│  │  metadata    │ │  (vectors)   │ │ metadata               ││
│  └──────────────┘ └──────────────┘ └────────────────────────┘│
└─────────────────────────────────────────────────────────────┘

AFTER (v2.0.10+):
┌────────────────────────────────┐    ┌───────────────────────────┐
│           SQLite                │    │        LanceDB            │
│  ┌──────────────────────────┐  │    │  ┌─────────────────────┐  │
│  │ documents                │  │    │  │      chunks         │  │
│  │ document_properties      │  │    │  │   (vectors only)    │  │
│  │ tags, document_tags      │  │    │  └─────────────────────┘  │
│  │ links                    │  │    │                           │
│  │ embedding_cache          │  │    │                           │
│  └──────────────────────────┘  │    │                           │
└────────────────────────────────┘    └───────────────────────────┘
```

### v2.0.7 — Dual-Write ✅ DONE

**Цель:** Начать записывать в SQLite параллельно с LanceDB

**Задачи:**
- [x] Активировать SQLiteManager в service_container
- [x] Добавить dual-write в IndexingService
- [x] Добавить consistency check (SQLite vs LanceDB)
- [x] Тесты для dual-write

**Файлы:**
| Файл | Изменения |
|------|-----------|
| `service_container.py` | Инициализация SQLiteManager |
| `storage/indexing/indexing_service.py` | Dual-write |
| `storage/sqlite/manager.py` | Активация |

**Deliverables:**
- [x] SQLite БД создаётся при индексации
- [x] Данные записываются в обе БД
- [x] Consistency report без расхождений

### v2.0.7.1 — HOTFIX: Document Lookup Fix ✅ DONE

**Цель:** Исправить критический баг, блокирующий поиск (95% результатов теряется)

**Root Cause:** При индексации `created_at` записывался как пустая строка `""`. При чтении `datetime.fromisoformat("")` падал, документ пропускался с warning "Document not found".

**Симптомы (исправлены):**
- 71+ warnings "Document not found" при поиске "Кардашин"
- Только 3 результата вместо 70+
- Релевантность = 0.00

**Задачи:**

| # | Задача | Файл | Статус |
|---|--------|------|--------|
| 1 | Исправить `_row_to_document()` — обработка пустых дат | `storage/document_repository.py:125-151` | ✅ |
| 2 | Исправить запись `created_at` — не писать `""` | `storage/indexing/indexing_service.py:297` | ✅ |
| 3 | Миграция данных — заменить `""` на valid dates | `scripts/migrate_created_at.py` | ✅ |
| 4 | Исправить пустой SQLite (dual-write) | `storage/indexing/indexing_service.py` | ✅ |

**Выполненные исправления:**

**Fix 1** — `_row_to_document()`:
- Добавлена проверка `and created_at` перед `fromisoformat()`
- Fallback: если `created_at` пустой, используется `modified_at`

**Fix 2** — `_prepare_document_record()`:
- Изменено на `(chunk.created_at or chunk.modified_at).isoformat()`

**Fix 3** — Скрипт миграции `scripts/migrate_created_at.py`:
- Поддержка `--dry-run`
- Поддержка `--vault-name all`
- Поддержка `--list-vaults`

**Fix 4** — SQLite dual-write:
- Добавлен явный `await sqlite_manager.initialize()` перед созданием схемы

**Deliverables:**
- [x] Поиск возвращает все релевантные документы
- [x] Нет warnings "Document not found"
- [x] `created_at` не пустой ни в одном документе
- [x] SQLite заполняется при индексации

**Acceptance Criteria:**
- [x] `search_vault("Кардашин")` возвращает `nkardashin.md` в топ-3 (после переиндексации)
- [x] Количество warnings = 0
- [x] Все тесты проходят

---

### v2.0.8 — SQLite-first Reads + Search Quality Fixes ✅ DONE

**Цель:** Исправить критические баги поиска из SEARCH_QUALITY_REPORT.md

**Выполненные задачи:**
- [x] MetadataService читает из SQLite (SQLite-first с LanceDB fallback)
- [x] TagRepository для SQLite dual-write
- [x] BUG-1: Фильтр `type:` не работал → исправлено
- [x] BUG-2: Hybrid search хуже отдельных методов → убран position_bonus
- [x] BUG-3: PROCEDURAL 122s → добавлен timeout 5s
- [x] BUG-4: SQLite таблицы пусты → добавлен _write_tags_to_sqlite()
- [x] Смена модели на mxbai-embed-large (1024 dims)
- [x] Query prefix для asymmetric embeddings

**Файлы:**
| Файл | Изменения |
|------|-----------|
| `storage/metadata_service.py` | SQLite-first reads |
| `storage/sqlite/repositories/tag.py` | Новый TagRepository |
| `storage/indexing/indexing_service.py` | _write_tags_to_sqlite() |
| `search/vector_search_service.py` | Убран position_bonus |
| `search/strategies/document_level.py` | PROCEDURAL timeout 5s |
| `embedding_service.py` | Query prefix support |
| `config.py` | mxbai-embed-large, 1024 dims |

**Результат:**
- Все 4 критических бага из SEARCH_QUALITY_REPORT.md исправлены
- Новая модель эмбеддингов mxbai-embed-large (1024 dims)
- 1544 тестов проходят

**Deliverables:**
- [x] Фильтры type:, author: работают через SQLite
- [x] Hybrid search использует чистую min-max нормализацию
- [x] PROCEDURAL запросы ограничены 5 секундами
- [x] Теги записываются в SQLite при индексации

### v2.0.9 — Cleanup

**Цель:** Удалить metadata из LanceDB

**Задачи:**
- [ ] Удалить таблицы documents, properties, metadata из LanceDB
- [ ] Оставить только chunks с embeddings
- [ ] Мигрировать embedding_cache в SQLite
- [ ] Обновить миграционные скрипты

**Файлы:**
| Файл | Изменения |
|------|-----------|
| `lance_db.py` | Удалить metadata таблицы |
| `storage/sqlite/embedding_cache.py` | Новый кэш |
| `scripts/migrate_v2.py` | Миграция данных |

### v2.0.10 — Stabilization

**Цель:** Подготовка к стабильному релизу

**Задачи:**
- [ ] Performance testing на реальных vault'ах
- [ ] Migration guide для пользователей v2.0.6
- [ ] Обновление документации
- [ ] Release notes

**Deliverables:**
- [ ] Все тесты проходят (1026+)
- [ ] Coverage ≥85% для новых модулей
- [ ] README, CHANGELOG обновлены

---

## Release 2.1 — Search Quality

**Цель:** Улучшение качества поиска

**Длительность:** После стабилизации 2.0.10

### v2.1.0 — Re-ranking (P1)

| Задача | Описание |
|--------|----------|
| Cross-encoder | Re-rank top-50 → top-10 |
| BGE-reranker | Или similar lightweight model |
| Tunable threshold | Настраиваемый порог relevance |

### v2.1.1 — Semantic Chunking (P2)

| Задача | Описание |
|--------|----------|
| Активировать chunking.py | Модуль уже существует |
| Complexity threshold | Настройка через config |
| Markdown-aware | Разбиение по заголовкам |

### v2.1.2 — Query Expansion (P2)

| Задача | Описание |
|--------|----------|
| Synonym expansion | Расширение синонимами |
| Query rewriting | LLM-based переформулировка |
| Multi-query | Несколько вариантов запроса |

### v2.1.3 — MMR Diversity (P2)

| Задача | Описание |
|--------|----------|
| Maximal Marginal Relevance | Diversity в результатах |
| Lambda parameter | Баланс relevance/diversity |
| Per-document MMR | Избежание дубликатов |

### v2.1.4 — NER & Entities (P2)

| Задача | Описание |
|--------|----------|
| Entity extraction | spaCy или custom NER |
| Entity linking | Связь с canonical docs |
| Alias search | "Сева" → vshadrin |

---

## Критические файлы

### Immediate Fixes

| Файл | Изменения |
|------|-----------|
| `config.py` | `auto_index_enabled`, `chunk_size` fix |
| `README.md` | Документация auto-indexing |
| `embedding_service.py` | Query prefix |
| `indexing/chunking.py` | Токены вместо символов |

### v2.0.7-2.0.10

| Файл | Изменения |
|------|-----------|
| `service_container.py` | SQLiteManager init |
| `storage/indexing/indexing_service.py` | Dual-write |
| `storage/metadata_service.py` | SQLite reads |
| `search/strategies/base.py` | SQLite filters |
| `lance_db.py` | Cleanup metadata |
| `storage/sqlite/embedding_cache.py` | Новый кэш |

### v2.1.x

| Файл | Изменения |
|------|-----------|
| `search/reranker.py` | Новый модуль |
| `search/vector_search_service.py` | MMR |
| `indexing/chunking.py` | Semantic chunking activation |
| `search/query_expander.py` | Новый модуль |

---

## Метрики успеха

### v2.0.10

| Метрика | v2.0.6 | v2.0.10 Target |
|---------|--------|----------------|
| Filter query latency | ~50ms | <20ms |
| Complex filter + vector | ~100ms | <50ms |
| Code complexity | N+1 queries | Single SQL query |
| Test coverage | ~85% | ≥85% |

### v2.1.x

| Метрика | v2.0.10 | v2.1 Target |
|---------|---------|-------------|
| Relevance (subjective) | Baseline | +20% |
| Result diversity | Low | High (MMR) |
| Entity recognition | None | People, projects |

---

## Риски и митигации

| Риск | Вероятность | Impact | Митигация |
|------|-------------|--------|-----------|
| Потеря данных при миграции | Medium | Critical | Backup + dual-write период |
| Breaking changes в API | Low | High | Фасад сохраняет интерфейс |
| SQLite lock contention | Low | Medium | WAL mode + connection pool |
| Performance regression | Low | High | A/B testing, feature flags |
| Несинхронизация SQLite/LanceDB | Medium | Medium | Consistency checks |

---

## Зависимости

| Зависимость | Статус | Необходимо для |
|-------------|--------|----------------|
| SQLite | Встроен | v2.0.7+ |
| aiosqlite | Установлен | Async SQLite |
| LanceDB | Установлен | Vector search |
| spaCy | Опционально | NER (v2.1) |

---

## Начало работы

### v2.0.7 — Dual-Write

```bash
git checkout main
git pull origin main
git checkout -b feature/v2.0.7-dual-write

# Изменить service_container.py, indexing_service.py, sqlite/manager.py
```

---

## История изменений

| Дата | Версия | Изменение |
|------|--------|-----------|
| 2026-01-10 | 2.0.6 | Создание revised roadmap на основе аудита |
| 2026-01-10 | 2.0.7 | Обновление нумерации фаз (2.0.7-2.0.10) |
| 2026-01-11 | 2.0.7 | ✅ Dual-Write выполнен, опубликован на PyPI |
| 2026-01-11 | 2.0.7.1 | ✅ HOTFIX: Document Lookup Fix выполнен, опубликован на PyPI |
| 2026-01-14 | 2.0.8 | ✅ Search Quality Fixes + mxbai-embed-large (1024 dims) |
