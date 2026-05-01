from pydantic import BaseModel
from typing import Dict, Any, List
from datetime import date
from src.core.domain.enums.fish_species import FishSpecies
from src.core.domain.enums.market_trend import MarketTrend

class FishingZoneResponseDTO(BaseModel):
    id_prediction: str
    date_validite: date
    polygone_geojson: Dict[str, Any]
    score_probabilite: float
    espece_cible: FishSpecies

class MarketPriceResponseDTO(BaseModel):
    id_prev_marche: str
    id_site_debarquement: str
    espece: FishSpecies
    prix_estime_48h: float
    indice_confiance: float
    tendance: MarketTrend
