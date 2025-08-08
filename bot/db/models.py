from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, DateTime, Boolean, JSON, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from bot.db.base import Base

class ListingStatus(str, enum.Enum):
    queued = "queued"
    approved = "approved"
    rejected = "rejected"
    archived = "archived"

class ListingCategory(str, enum.Enum):
    work = "work"
    rent = "rent"
    car = "car"
    events = "events"
    free = "free"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger, unique=True, index=True, nullable=False)
    lang = Column(String(5), default="ru")
    is_banned = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Listing(Base):
    __tablename__ = "listings"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    user = relationship("User")

    category = Column(Enum(ListingCategory), index=True, nullable=False)
    city = Column(String(64), index=True, nullable=False)

    title = Column(String(120), nullable=False)
    description = Column(Text, nullable=False)

    price = Column(Integer, nullable=True)
    tags = Column(JSON, nullable=True)
    media = Column(JSON, nullable=True)

    contact = Column(String(128), nullable=False)
    status = Column(Enum(ListingStatus), index=True, default=ListingStatus.queued)

    boosted_until = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Favorite(Base):
    __tablename__ = "favorites"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    listing_id = Column(Integer, ForeignKey("listings.id"), primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ModerationLog(Base):
    __tablename__ = "moderation_log"
    id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, ForeignKey("listings.id"), index=True)
    moderator_tg_id = Column(BigInteger, index=True)
    action = Column(String(32))
    reason = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
