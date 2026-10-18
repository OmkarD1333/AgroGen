from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, Query
from app.dependencies.db import get_current_user
from app.database.models import User
from app.schemas.agriculture import WeatherCurrentResponse
from app.services.weather_service import get_agro_weather

weather_router = APIRouter(prefix="/weather", tags=["weather"])


@weather_router.get("/current", response_model=WeatherCurrentResponse)
async def get_current_weather(
    city: Optional[str] = Query(default="Pune"),
):
    return get_agro_weather(city=city)


@weather_router.get("/forecast")
async def get_forecast(
    city: Optional[str] = Query(default="Pune"),
):
    current = get_agro_weather(city=city)
    return {
        "location": city,
        "current": current,
        "forecast_days": [
            {"day": "Day 1", "temp": current["temperature"], "condition": current["weather_condition"], "rain_prob": 10},
            {"day": "Day 2", "temp": current["temperature"] + 1, "condition": "Partly Cloudy", "rain_prob": 20},
            {"day": "Day 3", "temp": current["temperature"] - 1, "condition": "Sunny", "rain_prob": 5},
            {"day": "Day 4", "temp": current["temperature"], "condition": "Clear", "rain_prob": 15},
            {"day": "Day 5", "temp": current["temperature"] + 2, "condition": "Sunny", "rain_prob": 10},
        ],
    }


@weather_router.get("/history")
async def get_weather_history(
    city: Optional[str] = Query(default="Pune"),
):
    return [
        {"date": "2026-10-14", "temp_max": 31, "temp_min": 20, "rainfall_mm": 0},
        {"date": "2026-10-15", "temp_max": 30, "temp_min": 19, "rainfall_mm": 2.5},
        {"date": "2026-10-16", "temp_max": 29, "temp_min": 21, "rainfall_mm": 0},
    ]
