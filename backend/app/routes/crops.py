from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies.db import get_db, get_current_user
from app.database.models import User, Crop
from app.schemas.agriculture import CropCreate, CropUpdate, CropResponse

crops_router = APIRouter(prefix="/crops", tags=["crops"])


@crops_router.get("", response_model=List[CropResponse])
@crops_router.get("/", response_model=List[CropResponse])
async def list_crops(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return db.query(Crop).filter(Crop.user_id == current_user.id).all()


@crops_router.post("", response_model=CropResponse, status_code=status.HTTP_201_CREATED)
@crops_router.post("/", response_model=CropResponse, status_code=status.HTTP_201_CREATED)
async def create_crop(
    crop_data: CropCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    new_crop = Crop(user_id=current_user.id, **crop_data.model_dump())
    db.add(new_crop)
    db.commit()
    db.refresh(new_crop)
    return new_crop


@crops_router.get("/{crop_id}", response_model=CropResponse)
async def get_crop(
    crop_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    crop = db.query(Crop).filter(Crop.id == crop_id, Crop.user_id == current_user.id).first()
    if not crop:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Crop not found")
    return crop


@crops_router.put("/{crop_id}", response_model=CropResponse)
async def update_crop(
    crop_id: int,
    crop_data: CropUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    crop = db.query(Crop).filter(Crop.id == crop_id, Crop.user_id == current_user.id).first()
    if not crop:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Crop not found")

    for key, value in crop_data.model_dump(exclude_unset=True).items():
        setattr(crop, key, value)

    db.commit()
    db.refresh(crop)
    return crop


@crops_router.delete("/{crop_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_crop(
    crop_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    crop = db.query(Crop).filter(Crop.id == crop_id, Crop.user_id == current_user.id).first()
    if not crop:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Crop not found")

    db.delete(crop)
    db.commit()
    return None
