from abc import ABC, abstractmethod
from typing import List
from datetime import date
from src.core.domain.entities.fishing_zone_prediction import FishingZonePrediction

class ISpatialModelEngine(ABC):
    @abstractmethod
    def predict_fishing_zones(self, target_date: date) -> List[FishingZonePrediction]:
        """Runs CNN/LSTM model to predict fish zones based on oceanographic data."""
        pass
