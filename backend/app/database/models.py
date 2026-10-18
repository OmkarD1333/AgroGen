from datetime import date, datetime
from typing import Optional, List
from sqlalchemy import (
    Integer,
    BigInteger,
    Float,
    String,
    Boolean,
    Text,
    Date,
    DateTime,
    Index,
    ForeignKey,
    CheckConstraint,
    Identity,
    text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship, synonym
from .database import Base


class User(Base):
    __tablename__ = "users"

    __table_args__ = (
        CheckConstraint(
            "preferred_lang IN ('mr', 'en', 'hi')",
            name="check_users_preferred_language",
        ),
        Index("idx_users_role", "role"),
        Index("idx_users_google_id", "google_id"),
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        Identity(always=False),
        primary_key=True,
        autoincrement=True,
    )
    full_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )
    email: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        unique=True,
        index=True,
    )
    password_hash: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="farmer",
        server_default=text("'farmer'"),
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=text("true"),
    )
    google_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        unique=True,
    )
    avatar_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
    )
    auth_provider: Mapped[str] = mapped_column(
        String(50),
        nullable=True,
        default="local",
        server_default=text("'local'"),
    )
    phone: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
        unique=True,
    )
    preferred_lang: Mapped[Optional[str]] = mapped_column(
        String(10),
        nullable=True,
        default="en",
        server_default=text("'en'"),
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    id = synonym("user_id")
    preferred_language = synonym("preferred_lang")

    farmer_profile: Mapped[Optional["FarmerProfile"]] = relationship(
        "FarmerProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    crops: Mapped[List["Crop"]] = relationship(
        "Crop",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    weather_history: Mapped[List["WeatherHistory"]] = relationship(
        "WeatherHistory",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    chat_history: Mapped[List["ChatHistory"]] = relationship(
        "ChatHistory",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    notifications: Mapped[List["Notification"]] = relationship(
        "Notification",
        back_populates="user",
        cascade="all, delete-orphan",
    )


class FarmerProfile(Base):
    __tablename__ = "farmer_profile"

    profile_id: Mapped[int] = mapped_column(
        Integer,
        Identity(always=False),
        primary_key=True,
        autoincrement=True,
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    village: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )
    district: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )
    state: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        default="Maharashtra",
        server_default=text("'Maharashtra'"),
    )

    id = synonym("profile_id")

    user: Mapped["User"] = relationship(
        "User",
        back_populates="farmer_profile",
    )


class Crop(Base):
    __tablename__ = "crops"

    crop_id: Mapped[int] = mapped_column(
        Integer,
        Identity(always=False),
        primary_key=True,
        autoincrement=True,
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
    )
    crop_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    soil_type: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )
    sowing_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
    )
    growth_stage: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )

    id = synonym("crop_id")
    name = synonym("crop_name")

    user: Mapped["User"] = relationship(
        "User",
        back_populates="crops",
    )
    disease_history: Mapped[List["DiseaseHistory"]] = relationship(
        "DiseaseHistory",
        back_populates="crop",
        cascade="all, delete-orphan",
    )

    disease_diagnoses = synonym("disease_history")


class DiseaseHistory(Base):
    __tablename__ = "disease_history"

    disease_id: Mapped[int] = mapped_column(
        Integer,
        Identity(always=False),
        primary_key=True,
        autoincrement=True,
    )
    crop_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("crops.crop_id", ondelete="CASCADE"),
        nullable=False,
    )
    disease_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )
    confidence_score: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
    )
    image_path: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
    )
    treatment: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    detected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    id = synonym("disease_id")
    confidence = synonym("confidence_score")
    created_at = synonym("detected_at")
    treatment_mr = synonym("treatment")
    treatment_en = synonym("treatment")

    crop: Mapped["Crop"] = relationship(
        "Crop",
        back_populates="disease_history",
    )
    recommendations: Mapped[List["Recommendation"]] = relationship(
        "Recommendation",
        back_populates="disease_history",
        cascade="all, delete-orphan",
    )


DiseaseDiagnosis = DiseaseHistory


class Recommendation(Base):
    __tablename__ = "recommendations"

    recommendation_id: Mapped[int] = mapped_column(
        Integer,
        Identity(always=False),
        primary_key=True,
        autoincrement=True,
    )
    disease_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("disease_history.disease_id", ondelete="CASCADE"),
        nullable=False,
    )
    fertilizer: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    irrigation: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    pesticide: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    advisory: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    id = synonym("recommendation_id")

    disease_history: Mapped["DiseaseHistory"] = relationship(
        "DiseaseHistory",
        back_populates="recommendations",
    )


class WeatherHistory(Base):
    __tablename__ = "weather_history"

    weather_id: Mapped[int] = mapped_column(
        Integer,
        Identity(always=False),
        primary_key=True,
        autoincrement=True,
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
    )
    temperature: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
    )
    humidity: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
    )
    rainfall: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
    )
    wind_speed: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
    )
    forecast_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
    )

    id = synonym("weather_id")

    user: Mapped["User"] = relationship(
        "User",
        back_populates="weather_history",
    )


class ChatHistory(Base):
    __tablename__ = "chat_history"

    chat_id: Mapped[int] = mapped_column(
        Integer,
        Identity(always=False),
        primary_key=True,
        autoincrement=True,
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
    )
    question: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    response: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    language: Mapped[Optional[str]] = mapped_column(
        String(10),
        nullable=True,
        default="en",
        server_default=text("'en'"),
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    id = synonym("chat_id")
    created_at = synonym("timestamp")

    user: Mapped["User"] = relationship(
        "User",
        back_populates="chat_history",
    )


ChatMessage = ChatHistory


class Notification(Base):
    __tablename__ = "notifications"

    notification_id: Mapped[int] = mapped_column(
        Integer,
        Identity(always=False),
        primary_key=True,
        autoincrement=True,
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    type: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        default="general",
        server_default=text("'general'"),
    )
    status: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        default="unread",
        server_default=text("'unread'"),
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    id = synonym("notification_id")

    @property
    def is_read(self) -> bool:
        return self.status == "read"

    @is_read.setter
    def is_read(self, val: bool):
        self.status = "read" if val else "unread"

    user: Mapped["User"] = relationship(
        "User",
        back_populates="notifications",
    )


class GovernmentScheme(Base):
    __tablename__ = "government_schemes"

    scheme_id: Mapped[int] = mapped_column(
        Integer,
        Identity(always=False),
        primary_key=True,
        autoincrement=True,
    )
    scheme_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    eligibility: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    benefits: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    application_link: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
    )

    id = synonym("scheme_id")
    title_en = synonym("scheme_name")


class MandiMarketPrice(Base):
    __tablename__ = "mandi_market_prices"

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(always=False),
        primary_key=True,
        autoincrement=True,
    )
    district: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    market: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )
    commodity: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    variety: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )
    min_price: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    max_price: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    modal_price: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    arrival_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        autoincrement=True,
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    token_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    revoked_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
