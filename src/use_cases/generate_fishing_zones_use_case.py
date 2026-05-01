from src.core.ports.spatial_model_interface import ISpatialModelEngine
from datetime import date
from typing import List
from src.core.domain.entities.fishing_zone_prediction import FishingZonePrediction

class GenerateFishingZonesUseCase:
    def __init__(self, spatial_engine: ISpatialModelEngine):
        self.spatial_engine = spatial_engine
        
    def execute(self, target_date: date) -> List[FishingZonePrediction]:
        # Orchestrate data fetching and model inference
        predictions = self.spatial_engine.predict_fishing_zones(target_date)
        
        # Filter low probability zones to optimize bandwidth (< 500Ko GeoJSON as per spec)
        high_prob_zones = [p for p in predictions if p.score_probabilite > 0.70]
        
        return high_prob_zones
