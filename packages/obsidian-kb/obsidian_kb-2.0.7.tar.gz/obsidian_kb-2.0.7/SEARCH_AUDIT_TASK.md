# Задание: Комплексный аудит поисковой системы obsidian-kb

## Цель аудита

Провести глубокий анализ поисковой подсистемы obsidian-kb для:
1. Документирования текущей архитектуры и потоков данных
2. Выявления расхождений с лучшими практиками RAG-систем
3. Формирования рекомендаций для roadmap v2.x

## Scope аудита

### Включено
- Все виды поиска: vector search, FTS, hybrid, filter-based
- Flow от входной точки (MCP/CLI) до форматированного результата
- Взаимодействие LanceDB + SQLite (если есть)
- Intent detection и выбор стратегии
- Обогащение и ранжирование результатов
- Кэширование и оптимизации

### Исключено
- Индексация документов (отдельный аудит)
- LLM провайдеры (отдельный аудит)
- MCP транспортный слой

---

## Часть 1: Картирование потоков (Flow Mapping)

### 1.1 Входные точки поиска

Задокументировать все входные точки поисковых запросов:

| Точка входа | Файл | Функция/метод | Параметры |
|-------------|------|---------------|-----------|
| MCP tool | `mcp_server.py` | `search_vault()` | query, vault_name, limit, filters |
| MCP tool | `mcp_server.py` | `search_multi_vault()` | ... |
| MCP tool | `mcp_server.py` | `search_text()` | ... |
| CLI | `cli.py` (если есть) | ... | ... |
| Internal | `SearchService` | `search()` | ... |

**Вопросы для исследования:**
- Какие параметры принимает каждая точка входа?
- Как происходит нормализация/валидация входных данных?
- Есть ли дублирование логики между точками входа?

### 1.2 End-to-End Flow диаграмма

Построить детальную диаграмму для основного сценария `search_vault`:

```
Формат ожидаемой диаграммы:

User Request
    ↓
[MCP Layer] search_vault()
    ↓ параметры: query, vault, limit, filters
[Validation] ???
    ↓
[Intent Detection] IntentDetector
    ↓ intent: document_level | chunk_level | metadata_only
[Strategy Selection] ???
    ↓
[Query Processing] ???
    ↓
[Database Query] LanceDB / SQLite
    ↓
[Result Processing] ???
    ↓
[Formatting] MCPResultFormatter
    ↓
Response
```

**Задачи:**
1. Заполнить каждый блок реальными классами/методами
2. Указать данные, передаваемые между блоками
3. Отметить точки ветвления (if/else, strategy pattern)
4. Измерить типичное время на каждом этапе

### 1.3 Альтернативные flows

Аналогичные диаграммы для:
- `search_text` (ripgrep path)
- `search_regex`
- `dataview_query`
- Filter-only запросы (например, `type:person` без семантики)

---

## Часть 2: Типы поиска (Search Types Analysis)

### 2.1 Инвентаризация типов поиска

Для каждого типа поиска заполнить таблицу:

| Тип | Где реализован | Когда используется | Сильные стороны | Слабые стороны |
|-----|----------------|-------------------|-----------------|----------------|
| Vector Search | | | | |
| FTS (Full-Text Search) | | | | |
| Hybrid (Vector + FTS) | | | | |
| Filter-based (metadata) | | | | |
| Regex/Glob | | | | |

### 2.2 Vector Search

**Исследовать:**
- Какой алгоритм поиска (IVF, HNSW, brute-force)?
- Какая метрика расстояния (cosine, L2, dot product)?
- Какие параметры индекса используются?
- Как формируется embedding запроса?
- Есть ли query expansion или augmentation?

**Код для анализа:**
```python
# Найти и задокументировать:
# 1. Создание embedding для запроса
# 2. Вызов LanceDB search
# 3. Параметры: nprobes, refine_factor, metric
# 4. Post-processing результатов
```

**Метрики для сбора:**
- Средняя latency vector search
- Recall@k для тестовых запросов
- Распределение similarity scores

### 2.3 Full-Text Search (FTS)

**Исследовать:**
- Где реализован FTS: LanceDB native или SQLite FTS5?
- Какой tokenizer используется?
- Поддержка русского языка (stemming, morphology)?
- BM25 параметры (k1, b)?

**Код для анализа:**
```python
# Найти:
# 1. FTS индекс creation
# 2. FTS query formation
# 3. Ranking function
```

### 2.4 Hybrid Search

**Исследовать:**
- Как комбинируются vector + FTS?
- Reciprocal Rank Fusion (RRF) или другой метод?
- Веса для каждого источника
- Когда выбирается hybrid vs pure vector/FTS?

**Формула ожидаемого RRF:**
```
score(d) = Σ 1/(k + rank_i(d))
```

### 2.5 Filter-based Search

**Исследовать:**
- Как парсятся фильтры из query string (`type:person`, `tags:meeting`)?
- Pre-filtering vs post-filtering?
- Какие поля индексированы для фильтрации?
- Производительность filtered vs unfiltered запросов

---

## Часть 3: Архитектура хранения и поиска

### 3.1 Схема данных LanceDB

Задокументировать структуру таблиц в LanceDB:

```
vault_{name}_chunks:
  - id: ???
  - document_id: ???
  - content: ???
  - embedding: vector[???]
  - metadata: ???
  
vault_{name}_documents:
  - ???
```

**Вопросы:**
- Какая размерность embeddings?
- Какие метаданные хранятся в чанках?
- Есть ли денормализация для ускорения запросов?
- Как связаны chunks ↔ documents?

### 3.2 Взаимодействие LanceDB ↔ SQLite (если есть)

**Исследовать:**
- Что хранится в SQLite vs LanceDB?
- Как происходит join данных из разных источников?
- Есть ли embedding_cache в SQLite?
- Синхронизация данных между БД

**Паттерн двухэтапного запроса:**
```
1. LanceDB: vector search → candidate_ids
2. SQLite: enrich(candidate_ids) → full metadata
3. Merge + Rank
```

### 3.3 Индексы и производительность

**Задокументировать:**
- Какие индексы созданы в LanceDB?
- Какие индексы в SQLite (если есть)?
- Статистика по таблицам (row count, index size)
- Query plans для типовых запросов

---

## Часть 4: Intent Detection и стратегии

### 4.1 Intent Detection

**Исследовать IntentDetector:**
- Какие intents определяются?
- Какие признаки используются для классификации?
- Accuracy на тестовых запросах
- False positives/negatives

**Ожидаемые intents:**
```python
class QueryIntent(Enum):
    DOCUMENT_LEVEL = "document_level"  # Найти документ по ID/type
    CHUNK_LEVEL = "chunk_level"        # Семантический поиск
    METADATA_ONLY = "metadata_only"    # Только фильтры
    AGGREGATION = "aggregation"        # Статистика
    NAVIGATION = "navigation"          # Backlinks, related
```

### 4.2 Search Strategies

**Для каждой стратегии:**

| Strategy | Intent | Источник данных | Ranking | Результат |
|----------|--------|-----------------|---------|-----------|
| DocumentLevelStrategy | | | | |
| ChunkLevelStrategy | | | | |
| MetadataOnlyStrategy | | | | |

**Код для анализа:**
```python
# Найти:
# 1. Интерфейс ISearchStrategy
# 2. Все реализации
# 3. Логика выбора стратегии
# 4. Различия в обработке
```

---

## Часть 5: Сравнение с лучшими практиками

### 5.1 RAG Best Practices Checklist

| Практика | Реализовано | Как | Комментарий |
|----------|-------------|-----|-------------|
| **Query Understanding** | | | |
| Query expansion | ☐ | | Синонимы, переформулировка |
| Query classification | ☐ | | Intent detection |
| **Retrieval** | | | |
| Hybrid search | ☐ | | Vector + keyword |
| Re-ranking | ☐ | | Cross-encoder, MMR |
| Contextual compression | ☐ | | |
| **Chunking** | | | |
| Semantic chunking | ☐ | | vs fixed-size |
| Overlap | ☐ | | Контекст между чанками |
| Hierarchy | ☐ | | Parent-child chunks |
| **Result Processing** | | | |
| Deduplication | ☐ | | Удаление похожих |
| Diversity (MMR) | ☐ | | Maximal Marginal Relevance |
| Source citation | ☐ | | Ссылки на источники |
| **Evaluation** | | | |
| Offline metrics | ☐ | | Recall@k, MRR |
| Online feedback | ☐ | | Thumbs up/down |
| A/B testing | ☐ | | |

### 5.2 LanceDB-specific Best Practices

| Практика | Рекомендация | Текущее состояние | Gap |
|----------|--------------|-------------------|-----|
| Index type | IVF_PQ для >100K vectors, HNSW для <100K | | |
| Metric | Cosine для normalized embeddings | | |
| Prefilter | Используй prefilter для категориальных фильтров | | |
| Refine | refine_factor=10-50 для IVF | | |
| Batch queries | Batch similar queries | | |

### 5.3 Embedding Best Practices

| Практика | Рекомендация | Текущее состояние | Gap |
|----------|--------------|-------------------|-----|
| Query prefix | Добавлять "query:" для asymmetric retrieval | | |
| Normalization | L2 normalize перед поиском | | |
| Multilingual | BGE-M3 или multilingual-e5 для RU | | |
| Dimension | 1024+ для сложных задач | | |
| Caching | Кэшировать embedding запросов | | |

---

## Часть 6: Метрики и телеметрия

### 6.1 Текущие метрики

**Найти и задокументировать:**
- Какие метрики собираются?
- Где хранятся (таблица metrics)?
- Как визуализируются?

**Ожидаемые метрики:**
```python
@dataclass
class SearchMetrics:
    query: str
    vault: str
    intent: str
    strategy: str
    results_count: int
    latency_ms: float
    vector_search_ms: float
    enrichment_ms: float
    timestamp: datetime
```

### 6.2 Gaps в метриках

Какие метрики отсутствуют, но нужны:
- Relevance feedback (user satisfaction)
- Cache hit rate
- Fallback rate (vector → FTS → empty)
- Per-strategy performance

---

## Часть 7: Deliverables

### 7.1 Документация

1. **Architecture.md (обновление)** — раздел Search Architecture
2. **Search Flow Diagrams** — Mermaid диаграммы для каждого flow
3. **Best Practices Gap Analysis** — таблица с gaps и priorities

### 7.2 Код

1. **Тесты на regression** — если найдены расхождения
2. **Performance benchmarks** — скрипт для измерения latency
3. **Debug logging** — если недостаточно для анализа

### 7.3 Рекомендации

Приоритизированный список улучшений:

| # | Улучшение | Сложность | Влияние | Приоритет |
|---|-----------|-----------|---------|-----------|
| 1 | | S/M/L | High/Med/Low | P0/P1/P2 |

---

## Методология аудита

### Шаг 1: Code Reading
- Начать с `mcp_server.py` → `search_vault`
- Следовать по call chain
- Документировать каждый переход

### Шаг 2: Logging/Tracing
- Добавить debug logs если нужно
- Выполнить тестовые запросы
- Собрать traces

### Шаг 3: Testing
- Выполнить разные типы запросов
- Измерить latency
- Проверить корректность результатов

### Шаг 4: Comparison
- Сравнить с best practices
- Оценить gaps
- Приоритизировать улучшения

---

## Тестовые запросы для аудита

```python
test_queries = [
    # Pure semantic
    {"query": "подготовка к performance review", "expected": "chunk_level"},
    
    # Filter only
    {"query": "type:person", "expected": "metadata_only"},
    
    # ID lookup
    {"query": "vshadrin", "expected": "document_level"},
    
    # Hybrid
    {"query": "type:1-1 links:amuratov карьерный рост", "expected": "hybrid"},
    
    # Regex
    {"query": "search_regex pattern='TODO.*2025'", "expected": "regex"},
    
    # Empty results (edge case)
    {"query": "несуществующий_id_xyz123", "expected": "empty"},
]
```

---

## Timeline

| Фаза | Задачи | Оценка |
|------|--------|--------|
| Flow Mapping | Части 1, 4 | 2-3 часа |
| Type Analysis | Части 2, 3 | 3-4 часа |
| Best Practices | Части 5, 6 | 2-3 часа |
| Deliverables | Часть 7 | 2-3 часа |
| **Total** | | **10-13 часов** |
