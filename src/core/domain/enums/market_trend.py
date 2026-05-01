from enum import Enum

class MarketTrend(str, Enum):
    HAUSSE = "HAUSSE"
    BAISSE = "BAISSE"
    STABLE = "STABLE"
