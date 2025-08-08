import asyncio
import uvloop
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
import redis.asyncio as aioredis
from bot.core.config import settings
from bot.core.logger import logger
from bot.db.base import engine, Base, AsyncSessionLocal
from bot.handlers import start as h_start
from bot.handlers import menu as h_menu
from bot.handlers import post_listing as h_post
from bot.handlers import search as h_search
from bot.handlers import moderation as h_mod

async def on_startup(bot: Bot):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Bot started")

async def get_session_middleware(handler, event, data):
    async with AsyncSessionLocal() as session:
        data["session"] = session
        return await handler(event, data)

async def main():
    uvloop.install()
    bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    redis = aioredis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
    storage = RedisStorage(redis=redis)
    dp = Dispatcher(storage=storage)

    dp.update.outer_middleware(get_session_middleware)

    dp.include_router(h_start.router)
    dp.include_router(h_menu.router)
    dp.include_router(h_post.router)
    dp.include_router(h_search.router)
    dp.include_router(h_mod.router)

    await on_startup(bot)
    await dp.start_polling(bot, allowed_updates=types.ALL_UPDATE_TYPES)

if __name__ == "__main__":
    asyncio.run(main())
