## 2024-05-01 - FastAPI Dependency Injection and ML Model Caching
**Learning:** By default, FastAPI's dependency injection system re-executes dependency provider functions on every single request. When these providers instantiate heavy objects like ML model engines (e.g., LSTMs or CNNs), this causes massive performance bottlenecks.
**Action:** Use Python's built-in `@functools.lru_cache()` on dependency provider functions that return stateless, heavy objects. This effectively turns them into worker-scoped singletons, avoiding repeated initializations and significantly speeding up request handling.
## 2024-05-24 - Pydantic V2 Native Serialization
**Learning:** Manual list comprehensions in Python for mapping domain objects to Pydantic DTOs are slower and less readable than relying on Pydantic's Rust-based core.
**Action:** Use `model_config = ConfigDict(from_attributes=True)` on DTOs and return domain objects directly from FastAPI controllers. This delegates iteration and extraction to Rust, improving both performance and code clarity.
