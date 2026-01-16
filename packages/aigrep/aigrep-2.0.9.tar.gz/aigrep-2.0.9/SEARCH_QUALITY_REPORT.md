# Отчёт о качестве поиска obsidian-kb

**Дата:** 2026-01-12
**Vault:** Naumen_CTO (230 документов, 4559 чанков)
**Версия:** 2.0.7.1

---

## 1. Резюме

### Общая оценка: 4/10

Поиск работает частично. Критические проблемы с фильтрацией по `type:` делают MCP-сервер неудобным для пользователей.

### Что работает хорошо
- Known-item поиск по ID (`amuratov`, `ai-office`)
- Фильтрация по тегам (`tags:ai`)
- Процедурные запросы (`шаблон 1-1`)

### Критические проблемы
- **Фильтры `type:` не работают** — возвращают 0 результатов
- **Semantic поиск низкого качества** — релевантность 0.01
- **Hybrid search хуже FTS** — парадоксально низкая релевантность

---

## 2. Метрики автоматических тестов

| Метрика | Результат | Цель | Статус |
|---------|-----------|------|--------|
| P@1 | 0.100 | >= 0.70 | FAIL |
| P@5 | 0.080 | >= 0.60 | FAIL |
| MRR | 0.155 | >= 0.70 | FAIL |
| NDCG@5 | 0.094 | >= 0.65 | FAIL |
| R@10 | 0.080 | >= 0.70 | FAIL |

---

## 3. Детальные результаты по категориям

### 3.1 METADATA_FILTER (фильтры)

| Запрос | Результат | Проблема |
|--------|-----------|----------|
| `type:person` | 0 найдено | Фильтр не работает |
| `type:1-1` | 0 найдено | Фильтр не работает |
| `type:project` | 0 найдено | Фильтр не работает |
| `tags:ai` | 5+ найдено | РАБОТАЕТ |

**Причина:** Свойства frontmatter (type, status) хранятся в JSON поле `metadata` в LanceDB, но функция `get_documents_by_property()` ищет в таблице `document_properties` по колонке `property_key`. Эта таблица содержит только 4 типа записей: `created_at`, `metadata`, `modified_at`, `title`.

### 3.2 KNOWN_ITEM (поиск по ID)

| Запрос | Результат | Время |
|--------|-----------|-------|
| `amuratov` | 1 найден (relevance 1.0) | 1208ms |
| `ai-office` | 1 найден (relevance 1.0) | 1117ms |
| `guide_adr` | 1 найден (relevance 1.0) | 1188ms |
| `README.md` | 0 найдено | - |

**Проблема с README.md:** KNOWN_ITEM intent слишком строгий — если нет точного совпадения имени файла, возвращает 0 результатов.

### 3.3 SEMANTIC (семантический поиск)

| Запрос | Релевантность | Качество результатов |
|--------|---------------|---------------------|
| `критичные проблемы платформы` | 0.01 | Нерелевантные |
| `архитектура SMP` (vector) | 0.58 | Средне |
| `архитектура SMP` (fts) | 0.79 | Хорошо |
| `архитектура SMP` (hybrid) | 0.02 | Плохо |

**Проблема с hybrid:** Комбинирование скоров работает некорректно — hybrid даёт худшие результаты, чем FTS или vector отдельно.

### 3.4 PROCEDURAL (процедурные запросы)

| Запрос | Результат | Комментарий |
|--------|-----------|-------------|
| `как создать ADR` | Найдены документы | guide_adr.md НЕ в топе |
| `шаблон 1-1` | template_1-1.md в топ-3 | РАБОТАЕТ |
| `how to install` | Очень медленно (122с) | Проблема производительности |

---

## 4. A/B Тестирование типов поиска

Тестовый запрос: "архитектура SMP"

| Тип | Релевантность топ-1 | Комментарий |
|-----|---------------------|-------------|
| **FTS** | 0.79 | Лучший результат |
| **Vector** | 0.58 | Средне |
| **Hybrid** | 0.02 | Парадоксально плохо |

**Вывод:** Hybrid search в текущей реализации работает хуже отдельных методов.

---

## 5. Выявленные баги

### BUG-1: Фильтр `type:` не работает (CRITICAL)

**Воспроизведение:**
```bash
.venv/bin/obsidian-kb search --vault "Naumen_CTO" --query "type:person"
# Результат: 0 найдено
```

**Причина:**
- `get_documents_by_property()` ищет в таблице `document_properties`
- Frontmatter свойства хранятся в JSON поле `metadata` в таблице `metadata`
- Таблица `document_properties` не содержит записей с `property_key = 'type'`

**Локализация:**
- [metadata_service.py:600-660](src/obsidian_kb/storage/metadata_service.py#L600-L660) — `get_documents_by_property()`
- [base.py:76-78](src/obsidian_kb/search/strategies/base.py#L76-L78) — `_apply_filters()`

### BUG-2: Hybrid search даёт худшие результаты (HIGH)

**Воспроизведение:**
```bash
# FTS: 0.79
.venv/bin/obsidian-kb search --vault "Naumen_CTO" --query "архитектура SMP" --type fts

# Hybrid: 0.02
.venv/bin/obsidian-kb search --vault "Naumen_CTO" --query "архитектура SMP" --type hybrid
```

**Вероятная причина:** Неправильная нормализация или комбинирование скоров в гибридном поиске.

### BUG-3: PROCEDURAL запросы очень медленные (MEDIUM)

**Воспроизведение:**
```bash
.venv/bin/obsidian-kb search --vault "Naumen_CTO" --query "how to install"
# Время: 122723ms (2+ минуты!)
```

**Причина:** Скорее всего избыточные запросы или отсутствие early exit в логике PROCEDURAL.

### BUG-4: SQLite таблицы не заполняются (MEDIUM)

**Данные:**
- `document_properties` в SQLite: записей с `type` = 0
- `tags` в SQLite: 0 записей
- `document_tags` в SQLite: 0 записей

Dual-write в SQLite не работает для всех данных.

---

## 6. Рекомендации по исправлению

### Приоритет 1: Исправить фильтр `type:`

**Вариант A:** Парсить JSON из поля `metadata` для поиска по свойствам:
```python
async def get_documents_by_property(self, vault_name, property_key, property_value):
    # Искать в metadata_json вместо document_properties
    metadata_table = await self._ensure_table(vault_name, "metadata")
    where_clause = f"metadata_json LIKE '%\"{property_key}\": \"{property_value}\"%'"
    # ...
```

**Вариант B:** При индексации извлекать frontmatter свойства в отдельные записи `document_properties`.

### Приоритет 2: Исправить Hybrid search

Проверить логику комбинирования скоров в [vector_search_service.py](src/obsidian_kb/search/vector_search_service.py):
```python
combined_score = alpha * vector_score + (1 - alpha) * fts_score
```

Возможно, скоры не нормализованы к одинаковому диапазону.

### Приоритет 3: Оптимизировать PROCEDURAL

Добавить early exit и кэширование в [document_level.py](src/obsidian_kb/search/strategies/document_level.py) для процедурных запросов.

### Приоритет 4: Заполнить SQLite (v2.0.8 roadmap)

Переиндексировать vault с корректным dual-write в SQLite для всех свойств и тегов.

---

## 7. Матрица MCP сценариев

| Сценарий | Работает | Качество |
|----------|----------|----------|
| Поиск профиля человека по ID | Да | Хорошо |
| Поиск проекта по ID | Да | Хорошо |
| Фильтр по типу документа | НЕТ | - |
| Фильтр по тегам | Да | Хорошо |
| Семантический поиск | Частично | Низкое |
| Процедурные инструкции | Частично | Средне |
| Комбинированные фильтры | НЕТ | - |

---

## 8. Следующие шаги

1. **Срочно:** Исправить BUG-1 (фильтр `type:`)
2. **Важно:** Исправить BUG-2 (hybrid search)
3. **Желательно:** Оптимизировать BUG-3 (PROCEDURAL)
4. **Планово:** Реализовать SQLite-first reads (v2.0.8)

---

## Приложение: Тестовые запросы

```bash
# Known-item (работает)
.venv/bin/obsidian-kb search --vault "Naumen_CTO" --query "amuratov"
.venv/bin/obsidian-kb search --vault "Naumen_CTO" --query "ai-office"

# Фильтры (не работает type:)
.venv/bin/obsidian-kb search --vault "Naumen_CTO" --query "type:person"
.venv/bin/obsidian-kb search --vault "Naumen_CTO" --query "tags:ai"

# Semantic (низкое качество)
.venv/bin/obsidian-kb search --vault "Naumen_CTO" --query "критичные проблемы платформы"

# A/B тестирование
.venv/bin/obsidian-kb search --vault "Naumen_CTO" --query "архитектура SMP" --type vector
.venv/bin/obsidian-kb search --vault "Naumen_CTO" --query "архитектура SMP" --type fts
.venv/bin/obsidian-kb search --vault "Naumen_CTO" --query "архитектура SMP" --type hybrid
```
