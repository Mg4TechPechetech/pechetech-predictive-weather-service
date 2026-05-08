## 2024-05-01 - FastAPI Dependency Injection and ML Model Caching
**Learning:** By default, FastAPI's dependency injection system re-executes dependency provider functions on every single request. When these providers instantiate heavy objects like ML model engines (e.g., LSTMs or CNNs), this causes massive performance bottlenecks.
**Action:** Use Python's built-in `@functools.lru_cache()` on dependency provider functions that return stateless, heavy objects. This effectively turns them into worker-scoped singletons, avoiding repeated initializations and significantly speeding up request handling.
## 2024-05-02 - GZip Compression for GeoJSON Payloads
**Learning:** GeoJSON responses for spatial data (like fishing zones) can produce massive JSON payloads, consuming excessive network bandwidth and increasing latency.
**Action:** Always enable GZip compression (e.g., via FastAPI's GZipMiddleware) when serving endpoints that return large, repetitive text-based data like GeoJSON to drastically reduce payload sizes.
