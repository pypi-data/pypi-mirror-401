# Claude Code Rules для obsidian-kb

Этот файл содержит ключевые правила и best practices для работы Claude Code с проектом obsidian-kb.

## 📋 Основная информация

**Проект:** obsidian-kb — MCP-сервер для семантического поиска по Obsidian vault'ам
**Текущая версия:** 2.0.9
**Python:** 3.12+
**Тесты:** 1544+ (должны проходить все)
**Архитектура:** Hybrid SQLite + LanceDB

## 🎯 Основные правила

### 1. Виртуальная среда — ОБЯЗАТЕЛЬНА

**ВСЕГДА используй `.venv/bin/` для запуска Python и pytest:**

```bash
# ✅ Правильно
.venv/bin/pytest tests/ -x -q
.venv/bin/python -c "from obsidian_kb import __version__"
.venv/bin/python script.py

# ❌ Неправильно
pytest tests/
python -c "..."
python script.py
```

### 2. Тестирование

- **Все 1544+ тестов должны проходить** после каждого изменения
- Быстрая проверка: `.venv/bin/pytest tests/ -x -q 2>&1 | tail -15`
- Остановка на первой ошибке: `.venv/bin/pytest tests/ -x -q`
- Coverage ≥85% для критических модулей

### 3. Roadmap и релизы

- **Единственный актуальный roadmap:** [ROADMAP_v2_REVISED.md](ROADMAP_v2_REVISED.md)
- **Процедура релиза:** [.claude/rules/release.md](.claude/rules/release.md)
- **Автоматический релиз** при завершении фазы roadmap

### 4. Коммиты

**Формат коммита:**
```bash
git commit -m "feat(component): краткое описание (vX.X.X)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

**Semantic Versioning:**
- MAJOR: breaking changes
- MINOR: новые фичи (backward compatible)
- PATCH: bug fixes

### 5. Структура проекта

```
src/obsidian_kb/
├── core/                  # Базовые абстракции (TTLCache, DataNormalizer)
├── storage/
│   ├── builders/          # Record builders (Chunk, Document)
│   ├── indexing/          # IndexingService
│   └── sqlite/            # SQLite implementation (NEW в v2.0.7)
├── search/                # VectorSearchService, SearchService
├── providers/             # LLM провайдеры (Ollama, Yandex)
├── enrichment/            # Стратегии обогащения
├── mcp/tools/             # MCP инструменты
└── lance_db.py            # Фасад (рефакторинг в Phase 3)
```

## 🔧 Ключевые технологии

- **Векторная БД:** LanceDB (embeddings, chunks)
- **Metadata БД:** SQLite (documents, properties, tags, links)
- **Dual-Write:** v2.0.7+ записывает в обе БД
- **Embeddings:** Ollama (nomic-embed-text) или Yandex Cloud
- **LLM:** Ollama или Yandex Cloud (YandexGPT, Qwen3)

## 📚 Документация

### Для пользователей
- [README.md](README.md) — главная документация
- [QUICK_START.md](QUICK_START.md) — быстрый старт
- [INSTALLATION.md](INSTALLATION.md) — установка
- [USAGE.md](USAGE.md) — использование CLI и MCP
- [EXAMPLES.md](EXAMPLES.md) — примеры
- [MCP_INTEGRATION.md](MCP_INTEGRATION.md) — интеграция с агентами
- [PROVIDERS.md](PROVIDERS.md) — настройка провайдеров

### Для разработчиков
- [ARCHITECTURE.md](ARCHITECTURE.md) — архитектура проекта
- [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) — руководство разработчика
- [DATABASE_SCHEMA.md](DATABASE_SCHEMA.md) — схема БД
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) — API reference
- [CONTRIBUTING.md](CONTRIBUTING.md) — contributing guide

### Для Claude Code
- [.claude/rules/environment.md](.claude/rules/environment.md) — правила окружения
- [.claude/rules/release.md](.claude/rules/release.md) — процедура релиза
- [ROADMAP_v2_REVISED.md](ROADMAP_v2_REVISED.md) — текущий roadmap

## 🚀 Быстрые команды

### Тестирование
```bash
# Все тесты
.venv/bin/pytest tests/ -v

# Быстрая проверка
.venv/bin/pytest tests/ -x -q 2>&1 | tail -15

# Конкретный тест
.venv/bin/pytest tests/test_file.py::test_name -v
```

### Релиз (автоматический)
```bash
# 1. Тесты
.venv/bin/pytest tests/ -x -q

# 2-3. Обновить версию и документацию
# (см. .claude/rules/release.md)

# 4. Коммит
git add -A
git commit -m "feat(storage): описание (vX.X.X)..."

# 5. Тег
git tag -a vX.X.X -m "Release vX.X.X"

# 6. Push
git push origin main && git push origin vX.X.X

# 7-8. Build и publish
rm -rf dist/
.venv/bin/python -m build
.venv/bin/python -m twine upload dist/*
```

## 🎨 Стиль кода

- **Ruff** для linting и formatting
- **Type hints** обязательны для публичных API
- **Structured logging** с контекстом
- **Repository pattern** для data access
- **Strategy pattern** для разных реализаций
- **Dependency Injection** для всех компонентов

## ⚠️ Важные ограничения

1. **Обратная совместимость данных НЕ требуется** — пользователи могут переиндексировать
2. **MCP tools API должен быть стабильным** — пользователи зависят от него
3. **Breaking changes** только в major versions
4. **SQLite миграция** (v2.0.7-2.0.10) — dual-write → SQLite-first → cleanup LanceDB

## 📊 Метрики качества

| Метрика | Target |
|---------|--------|
| Тесты | 1026+ passing |
| Coverage | ≥85% критические модули |
| Filter query latency | <20ms (после v2.0.8) |
| Complex filter + vector | <50ms (после v2.0.8) |

## 🔍 Текущий фокус (v2.0.8)

**Следующая фаза:** SQLite-first Reads

**Задачи:**
- [ ] MetadataService читает из SQLite
- [ ] BaseSearchStrategy использует SQLite filters
- [ ] Измерить улучшение производительности
- [ ] A/B тестирование (feature flag)

**Целевые метрики:**
- Filter query: ~50ms → <20ms
- Complex filter + vector: ~100ms → <50ms

## 📖 Дополнительные ресурсы

- **PyPI:** https://pypi.org/project/obsidian-kb/
- **Changelog:** [CHANGELOG.md](CHANGELOG.md)
- **Roadmap:** [ROADMAP_v2_REVISED.md](ROADMAP_v2_REVISED.md)
- **Troubleshooting:** [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

**Дата создания:** 2026-01-12
**Последнее обновление:** 2026-01-12
**Версия проекта:** 2.0.7.1
