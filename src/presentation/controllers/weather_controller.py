from fastapi import APIRouter
from pydantic import BaseModel
import httpx
router = APIRouter(prefix="/api/v1/weather", tags=["Weather"])

class WeatherResponseDTO(BaseModel):
    condition: str
    temperature: int
    wind_speed: int
    wind_direction: str
    wave_height: float
    wave_period: int
    status_text: str
    alert_text: str



@router.get("/current", response_model=WeatherResponseDTO)
async def get_current_weather(site_id: str = "yoff", lat: float = None, lon: float = None):
    # Mapping of common Senegalese fishing sites to coordinates
    SITES = {
        # Dakar & Banlieue
        "yoff": (14.75, -17.46),
        "clpa-de-dakar-ouest": (14.68, -17.46),
        "clpa-de-hann": (14.71, -17.43),
        "clpa-de-pikine": (14.72, -17.42),
        "clpa-de-rufisque-bargny": (14.71, -17.27),
        "clpa-de-yenn-dialao": (14.62, -17.16),
        
        # Grande Côte & Thiès
        "kayar": (14.91, -17.12),
        "clpa-de-fass-boye": (15.15, -16.89),
        "saint-louis": (16.02, -16.50),
        
        # Petite Côte
        "clpa-de-sindia": (14.58, -17.06),
        "clpa-de-mbour": (14.41, -16.96),
        "joal": (14.16, -16.84),
        
        # Sine Saloum
        "clpa-de-fimela": (14.12, -16.65),
        "clpa-de-foundiougne": (14.13, -16.47),
        "clpa-de-missirah": (13.78, -16.50),
        "clpa-de-toubacouta": (13.78, -16.47),
        "clpa-de-sokone": (13.88, -16.37),
        
        # Casamance
        "clpa-de-elinkine": (12.55, -16.55),
        "clpa-de-ziguinchor": (12.58, -16.27),
        "dakar": (14.69, -17.44),
    }
    
    # Use provided lat/lon or fallback to site_id mapping
    if lat is None or lon is None:
        # Normalize site_id to lowercase for matching
        normalized_site = site_id.lower().replace(" ", "-")
        lat, lon = SITES.get(normalized_site, SITES["dakar"])
    
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,wind_speed_10m,wind_direction_10m,weather_code"
    marine_url = f"https://marine-api.open-meteo.com/v1/marine?latitude={lat}&longitude={lon}&current=wave_height,wave_direction,wave_period"
    
    async with httpx.AsyncClient() as client:
        weather_res = await client.get(weather_url)
        marine_res = await client.get(marine_url)
        
    weather_data = weather_res.json().get("current", {})
    marine_data = marine_res.json().get("current", {})
    
    temp = weather_data.get("temperature_2m", 25)
    wind_spd = weather_data.get("wind_speed_10m", 15)
    wind_dir_deg = weather_data.get("wind_direction_10m", 0)
    weather_code = weather_data.get("weather_code", 0)
    
    wave_h = marine_data.get("wave_height", 1.0)
    wave_p = marine_data.get("wave_period", 8.0)
    
    # Calculate condition
    if wind_spd > 35 or wave_h > 2.5:
        condition = "critical"
        alert_text = "ALERTE CRITIQUE"
    elif wind_spd > 20 or wave_h > 1.5:
        condition = "moderate"
        alert_text = "ALERTE MODÉRÉE"
    else:
        condition = "good"
        alert_text = "CONDITIONS FAVORABLES"
        
    # Translate some common WMO weather codes to text
    if weather_code == 0:
        status_text = "Ciel clair"
    elif weather_code in [1, 2, 3]:
        status_text = "Partiellement nuageux"
    elif weather_code >= 50:
        status_text = "Pluie / Averses"
    else:
        status_text = "Mer agitée" if condition != "good" else "Ciel clair"
        
    # Translate wind direction degrees to cardinal points
    dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    wind_direction = dirs[int((wind_dir_deg / 45.0) + 0.5) % 8]

    return WeatherResponseDTO(
        condition=condition,
        temperature=int(temp),
        wind_speed=int(wind_spd),
        wind_direction=wind_direction,
        wave_height=round(float(wave_h), 1),
        wave_period=int(wave_p),
        status_text=status_text,
        alert_text=alert_text
    )
