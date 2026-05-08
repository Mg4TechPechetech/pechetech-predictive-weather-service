from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from src.presentation.controllers.prediction_controller import router as prediction_router

app = FastAPI(
    title="PecheTech Predictive Weather & Market Service",
    description="Micro-service IA for spatial fishing zone prediction and market price forecasting.",
    version="1.0.0"
)

# ⚡ Bolt: Add GZip compression middleware to compress large GeoJSON responses,
# significantly reducing bandwidth usage and transfer times.
app.add_middleware(GZipMiddleware, minimum_size=1000)

app.include_router(prediction_router)

@app.get("/health")
def health_check():
    return {"status": "up"}
