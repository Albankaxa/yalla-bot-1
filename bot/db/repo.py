from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from bot.db.models import User, Listing, ListingStatus

class UserRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create(self, tg_id: int, lang: str = "ru") -> User:
        res = await self.session.execute(select(User).where(User.tg_id == tg_id))
        user = res.scalar_one_or_none()
        if user:
            return user
        user = User(tg_id=tg_id, lang=lang)
        self.session.add(user)
        await self.session.flush()
        return user

class ListingRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, **data) -> Listing:
        listing = Listing(**data)
        self.session.add(listing)
        await self.session.flush()
        return listing

    async def by_status(self, status: ListingStatus, limit: int = 20):
        res = await self.session.execute(
            select(Listing).where(Listing.status == status).order_by(Listing.created_at.desc()).limit(limit)
        )
        return res.scalars().all()

    async def approve(self, listing_id: int):
        await self.session.execute(update(Listing).where(Listing.id == listing_id).values(status=ListingStatus.approved))

    async def reject(self, listing_id: int, reason: str | None = None):
        await self.session.execute(update(Listing).where(Listing.id == listing_id).values(status=ListingStatus.rejected))
