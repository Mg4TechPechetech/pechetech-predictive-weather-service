from fastapi.testclient import TestClient
from main import app
from datetime import date

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "up"}

def test_get_fishing_zones():
    response = client.get("/api/v1/predictions/zones/today")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    # The dummy spatial model returns two zones, one is 0.85 and one is 0.60
    # The usecase filters out the 0.60, so only 1 should be returned
    assert len(data) == 1
    assert data[0]["espece_cible"] == "SARDINELLE"
    assert data[0]["score_probabilite"] == 0.85

def test_get_market_prices():
    response = client.get("/api/v1/predictions/market/Mbour")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["id_site_debarquement"] == "Mbour"
    assert data[0]["espece"] == "SARDINELLE"
    assert data[1]["tendance"] == "HAUSSE"
