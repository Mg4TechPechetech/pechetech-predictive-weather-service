from fastapi import FastAPI
from src.presentation.controllers.prediction_controller import router as prediction_router
from src.presentation.controllers.weather_controller import router as weather_router

app = FastAPI(
    title="PecheTech Predictive Weather & Market Service",
    description="Micro-service IA for spatial fishing zone prediction and market price forecasting.",
    version="1.0.0"
)

app.include_router(prediction_router)
app.include_router(weather_router)

@app.get("/health")
def health_check():
    return {"status": "up"}
