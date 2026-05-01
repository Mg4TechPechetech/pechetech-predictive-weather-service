from enum import Enum

class FishSpecies(str, Enum):
    SARDINELLE = "SARDINELLE"
    THON = "THON"
    MAQUEREAU = "MAQUEREAU"
    MEROU = "MEROU"
    AUTRE = "AUTRE"
