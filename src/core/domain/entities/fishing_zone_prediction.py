from dataclasses import dataclass
from datetime import date
from typing import Dict, Any
from src.core.domain.enums.fish_species import FishSpecies

@dataclass
class FishingZonePrediction:
    id_prediction: str
    date_validite: date
    polygone_geojson: Dict[str, Any]
    score_probabilite: float
    espece_cible: FishSpecies
