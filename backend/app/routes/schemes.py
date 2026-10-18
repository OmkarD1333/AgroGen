from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies.db import get_db
from app.database.models import GovernmentScheme
from app.schemas.agriculture import GovernmentSchemeResponse

schemes_router = APIRouter(prefix="/schemes", tags=["schemes"])

DEFAULT_SCHEMES = [
    {
        "id": 1,
        "title_en": "PM Kisan Samman Nidhi Yojana",
        "title_mr": "प्रधानमंत्री किसान सन्मान निधी योजना",
        "category": "Financial Assistance",
        "description_en": "Direct income support of INR 6,000 per year in three equal installments to all landholding farmer families.",
        "description_mr": "सर्व पात्र शेतकरी कुटुंबांना वर्षाला ६,००० रुपये थेट आर्थिक मदत तीन समान हप्त्यांमध्ये दिली जाते.",
        "benefits": "INR 6,000 / year",
        "eligibility": "Small and marginal farmers holding cultivable land in India.",
        "application_link": "https://pmkisan.gov.in",
        "created_at": "2026-10-17T10:00:00",
    },
    {
        "id": 2,
        "title_en": "Namo Shetkari Mahasanman Nidhi (Maharashtra)",
        "title_mr": "नमो शेतकरी महासन्मान निधी योजना (महाराष्ट्र)",
        "category": "State Welfare",
        "description_en": "Additional INR 6,000 annual subsidy by Government of Maharashtra on top of PM-KISAN, making total INR 12,000/year.",
        "description_mr": "महाराष्ट्र शासनाकडून पीएम-किसान व्यतिरिक्त अतिरिक्त ६,००० रुपये वार्षिक अनुदान, एकूण १२,००० रुपये वार्षिक.",
        "benefits": "INR 6,000 / year supplementary assistance",
        "eligibility": "Farmers registered and eligible under PM-KISAN residing in Maharashtra.",
        "application_link": "https://mahadbt.maharashtra.gov.in",
        "created_at": "2026-10-17T10:00:00",
    },
    {
        "id": 3,
        "title_en": "Dr. Babasaheb Ambedkar Krushi Swavalamban Yojana",
        "title_mr": "डॉ. बाबासाहेब आंबेडकर कृषी स्वावलंबन योजना",
        "category": "Irrigation & Subsidy",
        "description_en": "Special capital subsidy for new well construction, solar agricultural pumps, and micro-irrigation systems.",
        "description_mr": "नवीन विहीर, सौर कृषी पंप, शेततळे आणि ठिबक सिंचनासाठी विशेष शासकीय अनुदान.",
        "benefits": "Up to 100% subsidy on micro-irrigation and wells",
        "eligibility": "Scheduled caste/tribe farmers holding 0.40 to 6.00 hectares land.",
        "application_link": "https://mahadbt.maharashtra.gov.in",
        "created_at": "2026-10-17T10:00:00",
    },
]


@schemes_router.get("", response_model=List[GovernmentSchemeResponse])
@schemes_router.get("/", response_model=List[GovernmentSchemeResponse])
async def get_schemes(
    search: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(GovernmentScheme)
    if search:
        query = query.filter(
            (GovernmentScheme.title_en.ilike(f"%{search}%"))
            | (GovernmentScheme.title_mr.ilike(f"%{search}%"))
            | (GovernmentScheme.category.ilike(f"%{search}%"))
        )

    schemes = query.all()
    if not schemes:
        return [GovernmentSchemeResponse(**s) for s in DEFAULT_SCHEMES]
    return schemes


@schemes_router.get("/{scheme_id}", response_model=GovernmentSchemeResponse)
async def get_scheme(
    scheme_id: int,
    db: Session = Depends(get_db),
):
    scheme = db.query(GovernmentScheme).filter(GovernmentScheme.id == scheme_id).first()
    if not scheme:
        for s in DEFAULT_SCHEMES:
            if s["id"] == scheme_id:
                return GovernmentSchemeResponse(**s)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scheme not found")
    return scheme
