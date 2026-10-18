from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies.db import get_db, get_current_user
from app.database.models import User, Crop, DiseaseDiagnosis

recommendations_router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@recommendations_router.get("")
@recommendations_router.get("/")
async def get_general_recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    crops = db.query(Crop).filter(Crop.user_id == current_user.id).all()
    crop_names = [c.name for c in crops] if crops else ["Soybean", "Cotton"]

    return {
        "farmer_name": current_user.full_name,
        "recommendations": [
            {
                "id": 1,
                "crop": crop_names[0],
                "action_mr": "पिकाची आंतरमशागत करून तण नियंत्रण करा.",
                "action_en": "Perform inter-cultivation weeding to preserve moisture and soil nutrients.",
                "priority": "High",
                "days_due": 2,
            },
            {
                "id": 2,
                "crop": crop_names[0],
                "action_mr": "कीड नियंत्रणासाठी १० फेरोमोन ट्रॅप्स प्रति एकर लावा.",
                "action_en": "Install 10 pheromone traps per acre for pest population monitoring.",
                "priority": "Medium",
                "days_due": 5,
            },
        ],
    }


@recommendations_router.get("/disease/{disease_id}")
async def get_disease_recommendation(
    disease_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    diagnosis = db.query(DiseaseDiagnosis).filter(DiseaseDiagnosis.id == disease_id).first()
    if not diagnosis:
        return {
            "disease_id": disease_id,
            "disease_name": "Leaf Blight",
            "treatment_mr": "मॅन्कोझेब २.५ ग्रॅम प्रति लिटर पाण्यात मिसळून फवारा.",
            "treatment_en": "Spray Mancozeb 75% WP @ 2.5g/L water.",
            "preventive_measures": [
                "शेतात पाण्याचा निचरा योग्य ठेवा.",
                "रोगट पाने गोळा करून जाळून नष्ट करा.",
            ],
        }

    return {
        "disease_id": diagnosis.id,
        "disease_name": diagnosis.disease_name,
        "treatment_mr": diagnosis.treatment_mr,
        "treatment_en": diagnosis.treatment_en,
        "confidence": diagnosis.confidence,
    }
