from app.routes.auth import user_router
from app.routes.farmer import farmer_router
from app.routes.crops import crops_router
from app.routes.disease import disease_router
from app.routes.weather import weather_router
from app.routes.market import market_router
from app.routes.schemes import schemes_router
from app.routes.chatbot import chatbot_router
from app.routes.yield_prediction import yield_router
from app.routes.voice import voice_router
from app.routes.notifications import notifications_router
from app.routes.recommendations import recommendations_router

__all__ = [
    "user_router",
    "farmer_router",
    "crops_router",
    "disease_router",
    "weather_router",
    "market_router",
    "schemes_router",
    "chatbot_router",
    "yield_router",
    "voice_router",
    "notifications_router",
    "recommendations_router",
]
