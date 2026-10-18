from fastapi import APIRouter, Depends
from app.dependencies.db import get_current_user
from app.database.models import User
from app.schemas.agriculture import YieldPredictRequest, YieldPredictResponse
from app.services.yield_service import calculate_yield

yield_router = APIRouter(prefix="/yield", tags=["yield"])


@yield_router.post("/predict", response_model=YieldPredictResponse)
async def predict_crop_yield(
    req: YieldPredictRequest,
    current_user: User = Depends(get_current_user),
):
    result = calculate_yield(
        crop_name=req.crop_name,
        land_area_acres=req.land_area_acres,
        soil_type=req.soil_type or "Black Soil",
        season=req.season or "Kharif",
        rainfall_mm=req.rainfall_mm or 800.0,
        fertilizer_used_kg=req.fertilizer_used_kg or 100.0,
    )
    return YieldPredictResponse(**result)
