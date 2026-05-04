## 2024-05-01 - FastAPI Dependency Injection and ML Model Caching
**Learning:** By default, FastAPI's dependency injection system re-executes dependency provider functions on every single request. When these providers instantiate heavy objects like ML model engines (e.g., LSTMs or CNNs), this causes massive performance bottlenecks.
**Action:** Use Python's built-in `@functools.lru_cache()` on dependency provider functions that return stateless, heavy objects. This effectively turns them into worker-scoped singletons, avoiding repeated initializations and significantly speeding up request handling.
## 2024-05-02 - Pydantic V2 Optimized Serialization
**Learning:** Manually mapping domain entities (e.g. dataclasses) to Pydantic DTOs via list comprehensions in FastAPI controllers causes performance overhead because Python handles the iteration and object creation. Pydantic V2 (backed by Rust) is significantly faster at serializing lists of objects natively.
**Action:** Always prefer returning entity objects/dataclasses directly from controllers and configure the Pydantic DTOs with `model_config = ConfigDict(from_attributes=True)` to enable optimized, native serialization.
