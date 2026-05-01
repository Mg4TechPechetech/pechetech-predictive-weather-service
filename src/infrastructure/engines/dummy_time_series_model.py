from src.core.ports.time_series_model_interface import ITimeSeriesModelEngine
from typing import List
import uuid
from src.core.domain.entities.market_price_prediction import MarketPricePrediction
from src.core.domain.enums.fish_species import FishSpecies
from src.core.domain.enums.market_trend import MarketTrend

class DummyTimeSeriesModelEngine(ITimeSeriesModelEngine):
    def predict_market_prices(self, site_id: str) -> List[MarketPricePrediction]:
        # Mocking ARIMA/RNN inference
        return [
            MarketPricePrediction(
                id_prev_marche=str(uuid.uuid4()),
                id_site_debarquement=site_id,
                espece=FishSpecies.SARDINELLE,
                prix_estime_48h=1500.0,
                indice_confiance=0.92,
                tendance=MarketTrend.BAISSE
            ),
            MarketPricePrediction(
                id_prev_marche=str(uuid.uuid4()),
                id_site_debarquement=site_id,
                espece=FishSpecies.THON,
                prix_estime_48h=5500.0,
                indice_confiance=0.88,
                tendance=MarketTrend.HAUSSE
            )
        ]
