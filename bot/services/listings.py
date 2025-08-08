from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from bot.db.repo import ListingRepo
from bot.db.models import ListingCategory, ListingStatus

async def create_listing(session: AsyncSession, *, user_id: int, category: str, city: str, title: str, description: str, price: int | None, media: List[str] | None, contact: str):
    repo = ListingRepo(session)
    listing = await repo.create(
        user_id=user_id,
        category=ListingCategory(category),
        city=city,
        title=title,
        description=description,
        price=price,
        media=media or [],
        contact=contact,
        status=ListingStatus.queued,
    )
    await session.commit()
    return listing
