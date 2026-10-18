from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies.db import get_db, get_current_user
from app.database.models import User, FarmerProfile
from app.schemas.agriculture import FarmerProfileCreate, FarmerProfileResponse

farmer_router = APIRouter(prefix="/farmer", tags=["farmer"])


@farmer_router.get("/profile", response_model=FarmerProfileResponse)
async def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = db.query(FarmerProfile).filter(FarmerProfile.user_id == current_user.id).first()
    if not profile:
        # Create default empty profile if none exists
        profile = FarmerProfile(user_id=current_user.id, state="Maharashtra")
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile


@farmer_router.post("/profile", response_model=FarmerProfileResponse)
@farmer_router.put("/profile", response_model=FarmerProfileResponse)
async def upsert_profile(
    profile_data: FarmerProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = db.query(FarmerProfile).filter(FarmerProfile.user_id == current_user.id).first()
    if not profile:
        profile = FarmerProfile(user_id=current_user.id, **profile_data.model_dump())
        db.add(profile)
    else:
        for key, value in profile_data.model_dump(exclude_unset=True).items():
            setattr(profile, key, value)

    db.commit()
    db.refresh(profile)
    return profile
