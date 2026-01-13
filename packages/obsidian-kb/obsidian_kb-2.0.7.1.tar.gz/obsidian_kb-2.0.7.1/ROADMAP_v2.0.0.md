# Roadmap v2.0.0: Storage Architecture Evolution

**Дата создания:** 2026-01-10
**Текущая версия:** 1.0.0
**Цель:** Выбор и реализация оптимальной схемы хранения данных

---

## Мотивация

Текущая архитектура (всё в LanceDB) работает для v1.x, но имеет ограничения:
- Нет JOIN'ов для сложных фильтров
- N+1 запросов при комбинации фильтров
- Ограниченные возможности SQL

v2.0.0 должен определить целевую архитектуру на основе:
- Бенчмарков на реальных данных
- Прототипирования альтернативных решений
- Оценки сложности миграции

**Подробный анализ вариантов:** см. [docs/SEARCH_ARCHITECTURE.md](docs/SEARCH_ARCHITECTURE.md#storage-architecture-analysis)

---

## Варианты целевой архитектуры

| Вариант | Описание | Рекомендация |
|---------|----------|--------------|
| **A: LanceDB** | Текущий, оптимизация | Если use case не изменится |
| **B: PostgreSQL + pgvector** | Зрелый SQL + vectors | Для server/multi-user |
| **C: SQLite + sqlite-vec** | Единая embedded БД | Когда sqlite-vec достигнет v1.0 |
| **D: Гибридный** | SQLite metadata + LanceDB vectors | Баланс SQL + производительность |

---

## Фазы разработки

### Phase 1: Research & Benchmarking (P0)

**Цель:** Собрать данные для принятия решения

**Статус:** Не начато

#### 1.1 Создание benchmark suite

**Файл:** `benchmarks/storage_benchmark.py`

**Метрики для измерения:**
- Vector search latency (p50, p95, p99)
- Filter query latency
- Combined filter + vector search
- Indexing throughput
- Memory usage
- Disk space

**Тестовые сценарии:**
```python
scenarios = [
    {"vectors": 1000, "filters": "none"},
    {"vectors": 1000, "filters": "type:person"},
    {"vectors": 10000, "filters": "none"},
    {"vectors": 10000, "filters": "type:person tags:team"},
    {"vectors": 50000, "filters": "complex"},
]
```

#### 1.2 Прототип sqlite-vec

**Цель:** Оценить производительность sqlite-vec на реальных данных

**Задачи:**
- [ ] Создать SQLite схему с sqlite-vec
- [ ] Импортировать тестовый vault
- [ ] Запустить benchmark suite
- [ ] Документировать результаты

#### 1.3 Прототип гибридного решения

**Цель:** Оценить сложность и производительность

**Задачи:**
- [ ] SQLite для метаданных (documents, properties, tags)
- [ ] LanceDB для chunks + embeddings
- [ ] Реализовать синхронизацию при upsert
- [ ] Запустить benchmark suite

#### 1.4 Документирование результатов

**Deliverable:** `docs/STORAGE_BENCHMARK_RESULTS.md`

**Критерии завершения Phase 1:**
- [ ] Benchmark suite готов и воспроизводим
- [ ] sqlite-vec прототип протестирован
- [ ] Гибридный прототип протестирован
- [ ] Результаты задокументированы
- [ ] **Решение о целевой архитектуре принято**

---

### Phase 2: Design (P0)

**Цель:** Спроектировать целевую архитектуру

**Статус:** Ожидает Phase 1

**Зависит от результатов Phase 1**

#### Если выбран Гибридный вариант:

**2.1 SQLite Schema Design**
```sql
-- documents table
CREATE TABLE documents (
    document_id TEXT PRIMARY KEY,
    vault_name TEXT NOT NULL,
    file_path TEXT NOT NULL,
    title TEXT,
    content_type TEXT,
    created_at TEXT,
    modified_at TEXT,
    chunk_count INTEGER,
    content_hash TEXT
);

-- properties table (normalized)
CREATE TABLE document_properties (
    id INTEGER PRIMARY KEY,
    document_id TEXT NOT NULL,
    property_key TEXT NOT NULL,
    property_value TEXT,
    FOREIGN KEY (document_id) REFERENCES documents(document_id),
    UNIQUE(document_id, property_key)
);

-- tags table (many-to-many)
CREATE TABLE document_tags (
    document_id TEXT NOT NULL,
    tag TEXT NOT NULL,
    tag_type TEXT DEFAULT 'frontmatter', -- frontmatter | inline
    PRIMARY KEY (document_id, tag),
    FOREIGN KEY (document_id) REFERENCES documents(document_id)
);

-- indexes for fast filtering
CREATE INDEX idx_properties_key_value ON document_properties(property_key, property_value);
CREATE INDEX idx_tags_tag ON document_tags(tag);
CREATE INDEX idx_documents_vault ON documents(vault_name);
CREATE INDEX idx_documents_modified ON documents(modified_at);
```

**2.2 Migration Plan**
- Backward compatibility с v1.x vault'ами
- Автоматическая миграция при первом запуске
- Fallback на LanceDB-only если миграция не удалась

**2.3 API Compatibility**
- Сохранить существующие интерфейсы IDocumentRepository, IChunkRepository
- Новые реализации SQLiteDocumentRepository, LanceDBChunkRepository

#### Если выбран LanceDB (оптимизация):

**2.1 Оптимизации текущего решения**
- Batch запросы для фильтрации
- Агрессивное кэширование метаданных
- Денормализация для частых запросов

**Критерии завершения Phase 2:**
- [ ] Схема данных спроектирована
- [ ] План миграции готов
- [ ] API изменения задокументированы
- [ ] Риски оценены

---

### Phase 3: Implementation (P1)

**Цель:** Реализовать выбранную архитектуру

**Статус:** Ожидает Phase 2

**Задачи:**
- [ ] Реализовать новый storage layer
- [ ] Написать миграционный скрипт
- [ ] Обновить тесты (target: ≥90% coverage)
- [ ] Провести нагрузочное тестирование

**Критерии завершения Phase 3:**
- [ ] Все тесты проходят
- [ ] Миграция работает на тестовых vault'ах
- [ ] Performance соответствует целям

---

### Phase 4: Stabilization (P2)

**Цель:** Подготовка к релизу

**Статус:** Ожидает Phase 3

**Задачи:**
- [ ] Performance testing на реальных vault'ах разного размера
- [ ] Документация новой архитектуры
- [ ] Migration guide для пользователей v1.x
- [ ] Release notes
- [ ] Release v2.0.0

**Критерии завершения Phase 4:**
- [ ] Документация полная
- [ ] Нет критических багов
- [ ] Performance targets достигнуты

---

## Риски и митигация

| Риск | Вероятность | Влияние | Митигация |
|------|-------------|---------|-----------|
| sqlite-vec слишком медленный | Средняя | Высокое | Fallback на гибридный или текущий |
| Сложность синхронизации БД | Высокая | Среднее | Использовать транзакции, тесты |
| Регрессии производительности | Средняя | Высокое | Benchmark suite, A/B тестирование |
| Несовместимость со старыми vault | Низкая | Высокое | Автоматическая миграция |
| sqlite-vec не достигнет v1.0 | Средняя | Среднее | Мониторить развитие, иметь fallback |

---

## Метрики успеха

| Метрика | v1.0.0 (baseline) | v2.0.0 Target |
|---------|-------------------|---------------|
| Filter query latency | ~50ms | <20ms |
| Complex filter + vector | ~100ms | <50ms |
| Code complexity | N+1 queries | Single query (where possible) |
| Test coverage | ≥85% | ≥90% |
| Memory usage | baseline | ≤1.2x baseline |

---

## Зависимости

- **sqlite-vec v1.0:** Если выбран вариант C, нужно дождаться стабильного релиза
- **LanceDB updates:** Мониторить улучшения SQL support в LanceDB
- **pgvector/pgvectorscale:** Если появятся server requirements

---

## Начало работы

### Для Phase 1: Research

```bash
git checkout main
git pull origin main
git checkout -b feature/v2.0.0-storage-research
```

**Первые шаги:**
1. Создать `benchmarks/` директорию
2. Реализовать `storage_benchmark.py`
3. Протестировать на текущей архитектуре (baseline)
4. Создать прототипы альтернатив

---

## История изменений

| Дата | Изменение |
|------|-----------|
| 2026-01-10 | Создание roadmap |
