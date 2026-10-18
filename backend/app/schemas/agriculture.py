from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# --- Farmer Profile ---
class FarmerProfileBase(BaseModel):
    state: Optional[str] = "Maharashtra"
    district: Optional[str] = None
    taluka: Optional[str] = None
    village: Optional[str] = None
    land_size_acres: Optional[float] = 0.0
    soil_type: Optional[str] = None
    irrigation_source: Optional[str] = None


class FarmerProfileCreate(FarmerProfileBase):
    pass


class FarmerProfileResponse(FarmerProfileBase):
    id: int
    user_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# --- Crops ---
class CropBase(BaseModel):
    name: str
    variety: Optional[str] = None
    area_acres: Optional[float] = 1.0
    sowing_date: Optional[datetime] = None
    expected_harvest_date: Optional[datetime] = None
    season: Optional[str] = None
    status: Optional[str] = "active"


class CropCreate(CropBase):
    pass


class CropUpdate(BaseModel):
    name: Optional[str] = None
    variety: Optional[str] = None
    area_acres: Optional[float] = None
    sowing_date: Optional[datetime] = None
    expected_harvest_date: Optional[datetime] = None
    season: Optional[str] = None
    status: Optional[str] = None


class CropResponse(CropBase):
    id: int
    user_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# --- Disease Diagnosis ---
class DiseaseDiagnosisResponse(BaseModel):
    id: int
    crop_id: int
    image_path: str
    disease_name: str
    confidence: float
    status: str
    treatment_mr: Optional[str] = None
    treatment_en: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# --- Weather ---
class WeatherCurrentResponse(BaseModel):
    city: str
    temperature: float
    feels_like: float
    humidity: int
    wind_speed: float
    weather_condition: str
    description: str
    advisory_mr: str
    advisory_en: str
    spraying_suitability: str
    frost_warning: bool
    rain_probability: int


# --- Mandi Market Prices ---
class MandiMarketPriceResponse(BaseModel):
    id: int
    district: str
    market: str
    commodity: str
    variety: Optional[str] = None
    min_price: float
    max_price: float
    modal_price: float
    arrival_date: datetime

    class Config:
        from_attributes = True


# --- Government Schemes ---
class GovernmentSchemeResponse(BaseModel):
    id: int
    title_en: str
    title_mr: str
    category: str
    description_en: str
    description_mr: str
    benefits: Optional[str] = None
    eligibility: Optional[str] = None
    application_link: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# --- Chatbot ---
class ChatMessageRequest(BaseModel):
    message: str
    language: Optional[str] = "mr"


class ChatMessageResponse(BaseModel):
    response: str
    language: str
    timestamp: datetime


# --- Yield Prediction ---
class YieldPredictRequest(BaseModel):
    crop_name: str
    variety: Optional[str] = None
    land_area_acres: float = Field(gt=0)
    soil_type: Optional[str] = "Black Soil"
    season: Optional[str] = "Kharif"
    rainfall_mm: Optional[float] = 850.0
    fertilizer_used_kg: Optional[float] = 120.0


class YieldPredictResponse(BaseModel):
    crop_name: str
    estimated_yield_quintals: float
    estimated_yield_per_acre: float
    estimated_revenue_inr: float
    confidence_score: float
    tips_mr: List[str]
    tips_en: List[str]


# --- Voice Assistant ---
class VoiceTTSRequest(BaseModel):
    text: str
    language: Optional[str] = "mr"


class VoiceTTSResponse(BaseModel):
    audio_url: str
    language: str
    duration_seconds: Optional[float] = None


# --- Notifications ---
class NotificationResponse(BaseModel):
    id: int
    title: str
    message: str
    type: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True
