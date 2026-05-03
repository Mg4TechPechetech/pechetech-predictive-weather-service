## 2024-05-01 - FastAPI Dependency Injection and ML Model Caching
**Learning:** By default, FastAPI's dependency injection system re-executes dependency provider functions on every single request. When these providers instantiate heavy objects like ML model engines (e.g., LSTMs or CNNs), this causes massive performance bottlenecks.
**Action:** Use Python's built-in `@functools.lru_cache()` on dependency provider functions that return stateless, heavy objects. This effectively turns them into worker-scoped singletons, avoiding repeated initializations and significantly speeding up request handling.
## 2024-05-24 - FastAPI Pydantic serialization performance
**Learning:** Returning dataclass entity objects directly from a FastAPI controller while specifying a Pydantic `response_model` (with `model_config = ConfigDict(from_attributes=True)`) relies entirely on Pydantic's rust-core serialization and avoids manually constructing lists of DTOs in Python. In lists with many elements, this drops overhead by avoiding pure-Python loops.
**Action:** Always prefer direct entity returns and rely on Pydantic models with `from_attributes=True` for serializing large arrays.
