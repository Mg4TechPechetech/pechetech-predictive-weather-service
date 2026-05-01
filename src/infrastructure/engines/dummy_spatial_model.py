from src.core.ports.spatial_model_interface import ISpatialModelEngine
from datetime import date
from typing import List
import uuid
from src.core.domain.entities.fishing_zone_prediction import FishingZonePrediction
from src.core.domain.enums.fish_species import FishSpecies

class DummySpatialModelEngine(ISpatialModelEngine):
    def predict_fishing_zones(self, target_date: date) -> List[FishingZonePrediction]:
        # Mocking CNN/LSTM inference
        return [
            FishingZonePrediction(
                id_prediction=str(uuid.uuid4()),
                date_validite=target_date,
                polygone_geojson={
                    "type": "Polygon",
                    "coordinates": [[[-17.44, 14.69], [-17.50, 14.75], [-17.40, 14.80], [-17.44, 14.69]]]
                },
                score_probabilite=0.85, # 85% probability
                espece_cible=FishSpecies.SARDINELLE
            ),
            FishingZonePrediction(
                id_prediction=str(uuid.uuid4()),
                date_validite=target_date,
                polygone_geojson={
                    "type": "Polygon",
                    "coordinates": [[[-17.60, 14.50], [-17.65, 14.55], [-17.55, 14.60], [-17.60, 14.50]]]
                },
                score_probabilite=0.60, # 60% probability - should be filtered out by use case
                espece_cible=FishSpecies.THON
            )
        ]
