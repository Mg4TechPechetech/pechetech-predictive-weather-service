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
    predictions = use_case.execute(date.today())
    return [
        FishingZoneResponseDTO(
            id_prediction=p.id_prediction,
            date_validite=p.date_validite,
            polygone_geojson=p.polygone_geojson,
            score_probabilite=p.score_probabilite,
            espece_cible=p.espece_cible
        ) for p in predictions
    ]

@router.get("/market/{site_id}", response_model=List[MarketPriceResponseDTO])
def get_market_prices(site_id: str, use_case: GenerateMarketPricesUseCase = Depends(get_market_prices_use_case)):
    predictions = use_case.execute(site_id)
    return [
        MarketPriceResponseDTO(
            id_prev_marche=p.id_prev_marche,
            id_site_debarquement=p.id_site_debarquement,
            espece=p.espece,
            prix_estime_48h=p.prix_estime_48h,
            indice_confiance=p.indice_confiance,
            tendance=p.tendance
        ) for p in predictions
    ]
