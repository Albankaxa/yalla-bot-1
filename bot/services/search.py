from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from bot.db.models import Listing, ListingStatus, ListingCategory
from typing import List

async def search_listings(session: AsyncSession, *, category: str, city: str, limit: int = 10) -> List[Listing]:
    stmt = (
        select(Listing)
        .where(Listing.status == ListingStatus.approved)
        .where(Listing.category == ListingCategory(category))
        .where(Listing.city == city)
        .order_by(Listing.created_at.desc())
        .limit(limit)
    )
    res = await session.execute(stmt)
    return res.scalars().all()
