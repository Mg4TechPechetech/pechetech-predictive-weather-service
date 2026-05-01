from src.core.ports.time_series_model_interface import ITimeSeriesModelEngine
from typing import List
from src.core.domain.entities.market_price_prediction import MarketPricePrediction

class GenerateMarketPricesUseCase:
    def __init__(self, time_series_engine: ITimeSeriesModelEngine):
        self.time_series_engine = time_series_engine
        
    def execute(self, site_id: str) -> List[MarketPricePrediction]:
        predictions = self.time_series_engine.predict_market_prices(site_id)
        return predictions
