from fastapi import APIRouter, Depends
from datetime import date
from typing import List
from src.use_cases.generate_fishing_zones_use_case import GenerateFishingZonesUseCase
from src.use_cases.generate_market_prices_use_case import GenerateMarketPricesUseCase
from src.infrastructure.engines.dummy_spatial_model import DummySpatialModelEngine
from src.infrastructure.engines.dummy_time_series_model import DummyTimeSeriesModelEngine
from src.presentation.dtos.prediction_responses import FishingZoneResponseDTO, MarketPriceResponseDTO
from functools import lru_cache

router = APIRouter(prefix="/api/v1/predictions", tags=["Predictions"])

@lru_cache()
def get_fishing_zones_use_case():
    # Cache the use case and ML engine instantiation to avoid re-creating them on every request
    return GenerateFishingZonesUseCase(DummySpatialModelEngine())

@lru_cache()
def get_market_prices_use_case():
    # Cache the use case and ML engine instantiation to avoid re-creating them on every request
    return GenerateMarketPricesUseCase(DummyTimeSeriesModelEngine())

@router.get("/zones/today", response_model=List[FishingZoneResponseDTO])
def get_fishing_zones(use_case: GenerateFishingZonesUseCase = Depends(get_fishing_zones_use_case)):
    # ⚡ Bolt Optimization: Return domain entities directly instead of using manual list comprehension.
    # FastAPI and Pydantic will use the `model_config = ConfigDict(from_attributes=True)` we set
    # on the DTO to automatically serialize the list optimally in Rust.
    # Impact: Reduces memory overhead and serialization time by avoiding an intermediate Python list.
    predictions = use_case.execute(date.today())
    return predictions

@router.get("/market/{site_id}", response_model=List[MarketPriceResponseDTO])
def get_market_prices(site_id: str, use_case: GenerateMarketPricesUseCase = Depends(get_market_prices_use_case)):
    # ⚡ Bolt Optimization: Directly returning the models to utilize Pydantic V2's optimized from_attributes serialization.
    predictions = use_case.execute(site_id)
    return predictions
