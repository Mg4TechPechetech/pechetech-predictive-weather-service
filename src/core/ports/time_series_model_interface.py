from abc import ABC, abstractmethod
from typing import List
from src.core.domain.entities.market_price_prediction import MarketPricePrediction

class ITimeSeriesModelEngine(ABC):
    @abstractmethod
    def predict_market_prices(self, site_id: str) -> List[MarketPricePrediction]:
        """Runs ARIMA/RNN model to predict fish prices at H+48."""
        pass
