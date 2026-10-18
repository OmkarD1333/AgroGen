import os
import uuid
from pathlib import Path
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from app.dependencies.db import get_db, get_current_user
from app.database.models import User, Crop, DiseaseDiagnosis
from app.schemas.agriculture import DiseaseDiagnosisResponse
from app.services.disease_service import diagnose_leaf_image

disease_router = APIRouter(prefix="/disease", tags=["disease"])

UPLOAD_DIR = Path("uploads/disease")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@disease_router.post("/detect/{crop_id}", response_model=DiseaseDiagnosisResponse)
async def detect_disease(
    crop_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    crop = db.query(Crop).filter(Crop.id == crop_id, Crop.user_id == current_user.id).first()
    if not crop:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Crop not found")

    # Read image contents
    image_bytes = await file.read()
    if not image_bytes:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty image uploaded")

    # Save to disk
    ext = file.filename.split(".")[-1] if file.filename and "." in file.filename else "jpg"
    filename = f"{uuid.uuid4().hex}_{crop_id}.{ext}"
    file_path = UPLOAD_DIR / filename
    with open(file_path, "wb") as f:
        f.write(image_bytes)

    # Run AI inference
    result = diagnose_leaf_image(image_bytes, crop_hint=crop.name)

    diagnosis = DiseaseDiagnosis(
        crop_id=crop.id,
        image_path=f"/uploads/disease/{filename}",
        disease_name=result["disease_name"],
        confidence=result["confidence"],
        status="diagnosed",
        treatment_mr=result["treatment_mr"],
        treatment_en=result["treatment_en"],
    )

    db.add(diagnosis)
    db.commit()
    db.refresh(diagnosis)

    return diagnosis


@disease_router.get("/history/{crop_id}", response_model=List[DiseaseDiagnosisResponse])
async def get_history(
    crop_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    crop = db.query(Crop).filter(Crop.id == crop_id, Crop.user_id == current_user.id).first()
    if not crop:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Crop not found")

    return (
        db.query(DiseaseDiagnosis)
        .filter(DiseaseDiagnosis.crop_id == crop_id)
        .order_by(DiseaseDiagnosis.created_at.desc())
        .all()
    )
