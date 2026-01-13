# Отчёт об аудите obsidian-kb v1.0.1

**Дата:** 2026-01-10
**Версия:** 1.0.1
**Автор:** Claude Code Audit

---

## Executive Summary

1. **Bottlenecks в основном исправлены** — batch queries дали 60x speedup (commit a1555a0)
2. **Главный оставшийся bottleneck** — embedding generation (LLM call, 100-500ms)
3. **Автоиндексация работает корректно** — но нужен явный контроль пользователем
4. **SQLite код уже существует** — готов к интеграции, схема определена
5. **Качество поиска** — есть gaps: нет query expansion, re-ranking, semantic chunking

---

## Проблема 1: Медленный поиск

### Измерения

Timing измеряется в `ChunkLevelStrategy` (`search/strategies/chunk_level.py:69-127`) через DEBUG логи:

| Этап | Latency | Файл:строка |
|------|---------|-------------|
| **Embedding generation** | 100-500ms | `chunk_level.py:145-147` |
| **Pre-filtering** | 10-50ms | `base.py:56-146` |
| **Vector search (IVF-PQ)** | 20-100ms | `vector_search_service.py:368-474` |
| **FTS search (BM25)** | 10-50ms | `vector_search_service.py:475-594` |
| **RRF merge** | 5-10ms | `chunk_level.py:320-368` |
| **Aggregation** | 5-20ms | `chunk_level.py:289-318` |
| **Document enrichment** | 10-30ms | `chunk_level.py:230-287` |
| **Total** | **150-700ms** | `search/service.py:70,137` |

### Root Cause

1. **Embedding generation** — сетевой вызов к LLM провайдеру (Ollama/Yandex)
   - Timeout: 10 секунд (`config.py:22`)
   - Нет кэширования query embeddings

2. **Двухэтапные запросы для фильтрации** — нет JOIN в LanceDB
   ```python
   # base.py:77-135 — каждый фильтр = отдельный запрос
   ids1 = await self._documents.find_by_property(vault_name, "type", doc_type)
   ids2 = await self._documents.find_by_tags(vault_name, tags, match_all=True)
   all_ids = ids1 & ids2  # merge в Python
   ```

3. **Post-processing дат** — хранятся в documents таблице, не в chunks
   - Нельзя добавить в WHERE clause для chunks
   - Применяются после получения результатов

### Что уже исправлено

- **N+1 для document metadata** — batch queries (`vector_search_service.py:271-346`)
- **Параллельные запросы** — `asyncio.gather` для filters (`base.py:84-88`)
- **Кэширование** — TTLCache для document info (300 сек)

### Рекомендации

| # | Рекомендация | Приоритет | Сложность | Ожидаемый эффект |
|---|--------------|-----------|-----------|------------------|
| 1 | Кэширование query embeddings в SQLite | P0 | M | -200ms на повторных запросах |
| 2 | Переключить фильтрацию на SQLite | P1 | L | -30ms на сложных фильтрах |
| 3 | Batch embedding requests | P2 | M | Для batch операций |

---

## Проблема 2: Нерелевантные результаты

### Текущая реализация

**Intent Detection** (`search/intent_detector.py`):
```
QueryIntent:
├── METADATA_FILTER  # Только фильтры (tags:, type:)
├── KNOWN_ITEM       # *.md, ADR-001, ID документа
├── EXPLORATORY      # "что такое", "почему", "зачем"
├── PROCEDURAL       # "как", "инструкция", "template"
└── SEMANTIC         # Default fallback
```

**RRF Ranking** (`chunk_level.py:320-368`):
```python
k = 60  # RRF parameter
alpha = 0.7  # Вес vector search (config.hybrid_alpha)

# Формула:
score = alpha * (1/(k + rank_vector)) + (1 - alpha) * (1/(k + rank_fts))
```

**Chunking** (`config.py:38-39`):
```python
chunk_size: int = 2000   # ВНИМАНИЕ: это СИМВОЛЫ, не токены!
chunk_overlap: int = 250
```

### Gaps vs RAG Best Practices

| Практика | Статус | Файл | Рекомендация |
|----------|--------|------|--------------|
| Query expansion | Нет | — | Добавить переформулировку |
| Query prefix ("query:") | Нет | `embedding_service.py` | Для asymmetric embeddings |
| Re-ranking (cross-encoder) | Нет | — | BGE-reranker после top-50 |
| Semantic chunking | Есть модуль | `indexing/chunking.py` | Включить в pipeline |
| MMR (diversity) | Нет | — | Maximal Marginal Relevance |
| Position bonus | Частично | `vector_search_service.py` | Только для заголовков |

### Проблема: chunk_size в символах

**Документация** (`DATABASE_SCHEMA.md`):
> chunk_size: 2000 токенов

**Код** (`config.py:38`):
```python
chunk_size: int = 2000  # Это СИМВОЛЫ, не токены!
```

**Оценка токенов** (`indexing/chunking.py`):
```python
return len(text) // 3  # Приблизительно: 1 токен ≈ 3 символа
```

**Результат:** chunk_size=2000 символов ≈ 666 токенов, а не 2000 токенов.

### Рекомендации

| # | Рекомендация | Приоритет | Сложность | Файл |
|---|--------------|-----------|-----------|------|
| 1 | Исправить chunk_size (символы → токены) | P1 | S | `chunking.py` |
| 2 | Добавить query prefix | P1 | S | `embedding_service.py` |
| 3 | Включить semantic chunking | P2 | M | `indexing/chunking.py` |
| 4 | Добавить re-ranking | P2 | L | Новый модуль |
| 5 | Добавить MMR | P2 | M | `vector_search_service.py` |

---

## Проблема 3: Неконтролируемая индексация

### Найденные триггеры

| # | Триггер | Файл:строка | Механизм |
|---|---------|-------------|----------|
| 1 | **File watcher** | `change_monitor.py:224` | watchdog FileSystemEventHandler |
| 2 | **Polling** | `change_monitor.py:291` | Интервал 300 сек |
| 3 | **MCP: index_documents** | `mcp/tools/index_vault_tool.py` | Явный вызов |
| 4 | **MCP: reindex_vault** | `mcp_server.py` | Явный вызов |
| 5 | **add_vault_to_config** | `mcp_server.py:450,835` | auto_index=True |

### Детали автоиндексации

**ChangeMonitorService** (`indexing/change_monitor.py`):
```python
self._debounce_delay = 10.0   # секунд
self._poll_interval = 300     # секунд (5 минут)
```

**События:**
- CREATED: новый файл → индексация
- MODIFIED: изменение → переиндексация
- DELETED: удаление → удаление из индекса
- MOVED: перемещение → обновление путей

**BackgroundJobQueue** (`indexing/job_queue.py`):
- Max workers: 2
- Дедупликация: объединение paths для pending задач

### Важно: НЕТ implicit индексации при поиске

Поиск (`SearchService.search()`) **НЕ** вызывает индексацию:
- `search/service.py` — только чтение
- `vector_search_service.py` — только чтение
- Индексация — только через явные триггеры

### Рекомендации

| # | Рекомендация | Приоритет | Файл |
|---|--------------|-----------|------|
| 1 | Добавить `auto_index_enabled: bool = False` | P0 | `config.py` |
| 2 | Документировать auto_index в README | P0 | `README.md` |
| 3 | MCP tool `toggle_auto_index` | P1 | Новый tool |
| 4 | Уведомления о фоновой индексации | P2 | `job_queue.py` |

---

## Архитектурный Gap

### Текущая схема (LanceDB-only)

```
LanceDB (db_path/):
├── vault_{name}_documents          # метаданные файлов
├── vault_{name}_chunks             # чанки + embeddings (vector[768])
├── vault_{name}_document_properties # key-value свойства
├── vault_{name}_metadata           # frontmatter_tags[], metadata_json
├── metrics.lance/                  # метрики поиска
└── embedding_cache.lance/          # кэш embeddings
```

### Целевая схема (SQLite + LanceDB)

```
SQLite (metadata.db):
├── vaults
├── documents
├── document_properties (типизированные)
├── tags
├── document_tags (many-to-many)
├── links
├── entities
├── document_entities
├── embedding_cache
└── search_history

LanceDB (vectors/):
└── vault_{name}_chunks  # ТОЛЬКО chunks + embeddings
```

### Gap Analysis

| Компонент | Текущее (LanceDB) | Целевое (SQLite) | Gap |
|-----------|-------------------|------------------|-----|
| **Documents** | LanceDB table | SQLite table | Миграция данных |
| **Properties** | key-value | Типизированные (value_type) | Схема расширяется |
| **Tags** | Массивы в chunks | Many-to-many (tags, document_tags) | Нормализация |
| **Links** | Массивы в chunks | Таблица links | Новая структура |
| **Entities** | Нет | SQLite (NER) | Новая фича |
| **Embedding cache** | LanceDB | SQLite BLOB | Миграция |
| **Search history** | Нет | SQLite | Новая фича |

### Существующий SQLite код

Уже реализовано (готово к интеграции):

| Модуль | Файл | Описание |
|--------|------|----------|
| SQLiteManager | `storage/sqlite/manager.py` | Connection pooling, WAL mode |
| Schema | `storage/sqlite/schema.py` | Полная схема v2.0.0 |
| Repositories | `storage/sqlite/repositories/` | Базовые CRUD |
| Unified Layer | `storage/unified/` | Unified Metadata Access |

---

## Technical Debt

| # | Проблема | Приоритет | Сложность | Файл |
|---|----------|-----------|-----------|------|
| 1 | chunk_size в символах, не токенах | P1 | S | `config.py`, `chunking.py` |
| 2 | Semantic chunking не используется | P2 | M | `indexing/chunking.py` |
| 3 | Нет query prefix для embeddings | P1 | S | `embedding_service.py` |
| 4 | Нет re-ranking | P2 | L | Новый модуль |
| 5 | Нет MMR для diversity | P2 | M | `vector_search_service.py` |
| 6 | auto_index нет явного контроля | P0 | S | `config.py` |

---

## Критические файлы для v2.0

| Файл | Изменения |
|------|-----------|
| `config.py` | Добавить `auto_index_enabled`, исправить `chunk_size` |
| `storage/indexing/indexing_service.py` | Dual-write в SQLite |
| `storage/metadata_service.py` | Переключить на SQLite reads |
| `search/strategies/base.py` | SQLite filters |
| `indexing/chunking.py` | Исправить chunk_size |
| `embedding_service.py` | Query prefix |
| `storage/sqlite/manager.py` | Активировать |

---

## Приложение: Профилирование поиска

### Логи ChunkLevelStrategy

```python
# chunk_level.py:119-127
logger.debug(
    f"[PERF] ChunkLevelStrategy.search('{query[:50]}...'): "
    f"total={total_time:.1f}ms, "
    f"search={search_time:.1f}ms, "
    f"build={build_time:.1f}ms, "
    f"grouping={grouping_time:.1f}ms, "
    f"sort={sort_time:.1f}ms"
)
```

### Включение DEBUG логов

```bash
# В .env или окружении
OBSIDIAN_KB_LOG_LEVEL=DEBUG

# Или в коде
import logging
logging.getLogger("obsidian_kb").setLevel(logging.DEBUG)
```

### Метрики в MetricsCollector

```python
# metrics.py:136-205
await metrics.record_search(
    vault_name=vault_name,
    query=query,
    search_type="hybrid",
    result_count=len(results),
    execution_time_ms=elapsed_ms,
    avg_relevance_score=avg_score,
)
```

---

## Заключение

obsidian-kb v1.0.1 — зрелый проект с хорошей архитектурой. Основные bottlenecks производительности уже исправлены. Для v2.0 рекомендуется:

1. **P0**: Добавить контроль автоиндексации
2. **P1**: Переключить фильтрацию на SQLite (код готов)
3. **P1**: Исправить chunk_size и добавить query prefix
4. **P2**: Улучшить качество поиска (re-ranking, MMR, semantic chunking)
