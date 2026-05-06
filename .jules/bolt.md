## 2024-05-01 - FastAPI Dependency Injection and ML Model Caching
**Learning:** By default, FastAPI's dependency injection system re-executes dependency provider functions on every single request. When these providers instantiate heavy objects like ML model engines (e.g., LSTMs or CNNs), this causes massive performance bottlenecks.
**Action:** Use Python's built-in `@functools.lru_cache()` on dependency provider functions that return stateless, heavy objects. This effectively turns them into worker-scoped singletons, avoiding repeated initializations and significantly speeding up request handling.

## 2024-05-17 - Pydantic V2 Fast Serialization
**Learning:** Pydantic V2's core is written in Rust. Doing manual list comprehensions to convert domain entities to DTOs in FastAPI controllers bypasses this fast path, making serialization slower for large lists.
**Action:** Always return domain entities/dataclasses directly from FastAPI controllers and rely on `response_model` + `model_config = ConfigDict(from_attributes=True)` in DTOs to let Pydantic handle the serialization efficiently.
