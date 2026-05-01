import pytest
from datetime import date
from src.core.domain.enums.fish_species import FishSpecies
from src.core.domain.enums.market_trend import MarketTrend
from src.core.domain.entities.fishing_zone_prediction import FishingZonePrediction
from src.core.domain.entities.market_price_prediction import MarketPricePrediction
from src.use_cases.generate_fishing_zones_use_case import GenerateFishingZonesUseCase
from src.use_cases.generate_market_prices_use_case import GenerateMarketPricesUseCase
from src.core.ports.spatial_model_interface import ISpatialModelEngine
from src.core.ports.time_series_model_interface import ITimeSeriesModelEngine
from typing import List

class MockSpatialModel(ISpatialModelEngine):
    def predict_fishing_zones(self, target_date: date) -> List[FishingZonePrediction]:
        return [
            FishingZonePrediction("id1", target_date, {}, 0.85, FishSpecies.SARDINELLE),
            FishingZonePrediction("id2", target_date, {}, 0.45, FishSpecies.THON) # Should be filtered out (<0.70)
        ]

class MockTimeSeriesModel(ITimeSeriesModelEngine):
    def predict_market_prices(self, site_id: str) -> List[MarketPricePrediction]:
        return [
            MarketPricePrediction("p1", site_id, FishSpecies.SARDINELLE, 1500.0, 0.90, MarketTrend.HAUSSE)
        ]

def test_generate_fishing_zones():
    use_case = GenerateFishingZonesUseCase(MockSpatialModel())
    predictions = use_case.execute(date.today())
    
    assert len(predictions) == 1
    assert predictions[0].score_probabilite == 0.85
    assert predictions[0].espece_cible == FishSpecies.SARDINELLE

def test_generate_market_prices():
    use_case = GenerateMarketPricesUseCase(MockTimeSeriesModel())
    predictions = use_case.execute("Dakar-Hann")
    
    assert len(predictions) == 1
    assert predictions[0].prix_estime_48h == 1500.0
    assert predictions[0].tendance == MarketTrend.HAUSSE
