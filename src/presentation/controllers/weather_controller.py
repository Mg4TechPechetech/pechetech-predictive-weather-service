import time
from fastapi import APIRouter
from pydantic import BaseModel
import httpx
from typing import Dict, Any

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

# Cache system: structure -> {(lat, lon): {"data": WeatherResponseDTO, "timestamp": float}}
WEATHER_CACHE: Dict[tuple, Dict[str, Any]] = {}
CACHE_TTL = 1800  # 30 minutes in seconds

@router.get("/current", response_model=WeatherResponseDTO)
async def get_current_weather(site_id: str = "yoff", lat: float = None, lon: float = None):
    # Mapping of common Senegalese fishing sites to coordinates
    SITES = {
        "yoff": (14.75, -17.46),
        "clpa-de-dakar-ouest": (14.68, -17.46),
        "clpa-de-hann": (14.71, -17.43),
        "clpa-de-pikine": (14.72, -17.42),
        "clpa-de-rufisque-bargny": (14.71, -17.27),
        "clpa-de-yenn-dialao": (14.62, -17.16),
        "kayar": (14.91, -17.12),
        "clpa-de-fass-boye": (15.15, -16.89),
        "saint-louis": (16.02, -16.50),
        "clpa-de-sindia": (14.58, -17.06),
        "clpa-de-mbour": (14.41, -16.96),
        "joal": (14.16, -16.84),
        "clpa-de-fimela": (14.12, -16.65),
        "clpa-de-foundiougne": (14.13, -16.47),
        "clpa-de-missirah": (13.78, -16.50),
        "clpa-de-toubacouta": (13.78, -16.47),
        "clpa-de-sokone": (13.88, -16.37),
        "clpa-de-elinkine": (12.55, -16.55),
        "clpa-de-ziguinchor": (12.58, -16.27),
        "dakar": (14.69, -17.44),
    }
    
    if lat is None or lon is None:
        normalized_site = site_id.lower().replace(" ", "-")
        lat, lon = SITES.get(normalized_site, SITES["dakar"])
    
    cache_key = (lat, lon)
    current_time = time.time()
    
    # 1. CHECK CACHE: Return cached data if it's less than 30 minutes old
    if cache_key in WEATHER_CACHE:
        cached_entry = WEATHER_CACHE[cache_key]
        if current_time - cached_entry["timestamp"] < CACHE_TTL:
            return cached_entry["data"]

    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,wind_speed_10m,wind_direction_10m,weather_code"
    marine_url = f"https://marine-api.open-meteo.com/v1/marine?latitude={lat}&longitude={lon}&current=wave_height,wave_direction,wave_period"
    
    # 2. IDENTIFY AS PECHETECH (Prevents generic Python blocking)
    headers = {
        "User-Agent": "PecheTech-SuperApp/1.0 (contact: admin@pechetech.com)"
    }

    temp, wind_spd, wind_dir_deg, weather_code = 25, 15, 0, 0
    wave_h, wave_p = 1.0, 8.0
    
    try:
        # Add timeouts to prevent hanging requests
        async with httpx.AsyncClient(headers=headers, timeout=10.0) as client:
            weather_res = await client.get(weather_url)
            marine_res = await client.get(marine_url)
            
        weather_res.raise_for_status()
        marine_res.raise_for_status()
            
        weather_data = weather_res.json().get("current", {})
        marine_data = marine_res.json().get("current", {})
        
        temp = weather_data.get("temperature_2m", 25)
        wind_spd = weather_data.get("wind_speed_10m", 15)
        wind_dir_deg = weather_data.get("wind_direction_10m", 0)
        weather_code = weather_data.get("weather_code", 0)
        
        wave_h = marine_data.get("wave_height", 1.0)
        wave_p = marine_data.get("wave_period", 8.0)
        
    except Exception as e:
        # 3. FALLBACK: If API fails, try to return old cached data even if expired, else use safe defaults
        print(f"Weather API Error: {e}. Using fallback data.")
        if cache_key in WEATHER_CACHE:
            return WEATHER_CACHE[cache_key]["data"]
            
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
        
    if weather_code == 0:
        status_text = "Ciel clair"
    elif weather_code in [1, 2, 3]:
        status_text = "Partiellement nuageux"
    elif weather_code >= 50:
        status_text = "Pluie / Averses"
    else:
        status_text = "Mer agitée" if condition != "good" else "Ciel clair"
        
    dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    wind_direction = dirs[int((wind_dir_deg / 45.0) + 0.5) % 8]

    response = WeatherResponseDTO(
        condition=condition,
        temperature=int(temp),
        wind_speed=int(wind_spd),
        wind_direction=wind_direction,
        wave_height=round(float(wave_h), 1),
        wave_period=int(wave_p),
        status_text=status_text,
        alert_text=alert_text
    )
    
    # Save to cache
    WEATHER_CACHE[cache_key] = {
        "data": response,
        "timestamp": current_time
    }
    
    return response
