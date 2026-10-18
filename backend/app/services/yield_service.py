from typing import Dict, Any


def calculate_yield(
    crop_name: str,
    land_area_acres: float,
    soil_type: str = "Black Soil",
    season: str = "Kharif",
    rainfall_mm: float = 800.0,
    fertilizer_used_kg: float = 100.0,
) -> Dict[str, Any]:
    """
    Calculate estimated crop yield per acre and projected revenue
    based on Maharashtra regional benchmarks.
    """
    benchmarks = {
        "cotton": {"base_quintals_per_acre": 8.5, "price_per_quintal": 7200.0},
        "soybean": {"base_quintals_per_acre": 10.0, "price_per_quintal": 4800.0},
        "sugarcane": {"base_quintals_per_acre": 380.0, "price_per_quintal": 315.0},
        "wheat": {"base_quintals_per_acre": 15.0, "price_per_quintal": 2275.0},
        "onion": {"base_quintals_per_acre": 90.0, "price_per_quintal": 1800.0},
        "rice": {"base_quintals_per_acre": 18.0, "price_per_quintal": 2300.0},
        "maize": {"base_quintals_per_acre": 22.0, "price_per_quintal": 2100.0},
        "tur": {"base_quintals_per_acre": 6.5, "price_per_quintal": 7500.0},
    }

    clean_crop = crop_name.strip().lower()
    crop_data = benchmarks.get(clean_crop, {"base_quintals_per_acre": 12.0, "price_per_quintal": 3000.0})

    # Modifiers based on soil and rainfall
    soil_factor = 1.1 if "black" in soil_type.lower() else (0.95 if "red" in soil_type.lower() else 1.0)
    
    rain_factor = 1.0
    if rainfall_mm < 500:
        rain_factor = 0.8
    elif rainfall_mm > 1200:
        rain_factor = 0.95
    else:
        rain_factor = 1.05

    fertilizer_factor = 1.05 if fertilizer_used_kg >= 100 else 0.95

    yield_per_acre = crop_data["base_quintals_per_acre"] * soil_factor * rain_factor * fertilizer_factor
    total_yield = round(yield_per_acre * land_area_acres, 2)
    revenue = round(total_yield * crop_data["price_per_quintal"], 2)

    tips_mr = [
        "वेळेवर पाणी व्यवस्थापन ठेवा, विशेषतः फुलोऱ्याच्या अवस्थेत.",
        "माती परीक्षणावर आधारित संतुलित खतांचा वापर करा (NPK).",
        "कीड व रोगांचा प्रादुर्भाव टाळण्यासाठी निंबोळी अर्क ५% फवारा.",
    ]
    tips_en = [
        "Maintain timely irrigation, particularly during flowering and pod development stages.",
        "Apply balanced NPK fertilization based on soil testing card.",
        "Spray 5% neem seed kernel extract (NSKE) as preventive pest repellent.",
    ]

    return {
        "crop_name": crop_name,
        "estimated_yield_quintals": total_yield,
        "estimated_yield_per_acre": round(yield_per_acre, 2),
        "estimated_revenue_inr": revenue,
        "confidence_score": 0.89,
        "tips_mr": tips_mr,
        "tips_en": tips_en,
    }
