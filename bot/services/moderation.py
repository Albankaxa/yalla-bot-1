from sqlalchemy.ext.asyncio import AsyncSession
from bot.db.repo import ListingRepo

async def approve_listing(session: AsyncSession, listing_id: int):
    repo = ListingRepo(session)
    await repo.approve(listing_id)
    await session.commit()

async def reject_listing(session: AsyncSession, listing_id: int, reason: str | None = None):
    repo = ListingRepo(session)
    await repo.reject(listing_id, reason)
    await session.commit()
