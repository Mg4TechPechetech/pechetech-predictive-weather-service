from dataclasses import dataclass
from src.core.domain.enums.fish_species import FishSpecies
from src.core.domain.enums.market_trend import MarketTrend

@dataclass
class MarketPricePrediction:
    id_prev_marche: str
    id_site_debarquement: str
    espece: FishSpecies
    prix_estime_48h: float
    indice_confiance: float
    tendance: MarketTrend
