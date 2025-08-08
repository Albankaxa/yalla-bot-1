from aiogram import Router, F
from aiogram.types import Message
from bot.core.config import settings
from bot.db.repo import ListingRepo
from bot.db.models import ListingStatus
from bot.services.moderation import approve_listing, reject_listing

router = Router()

@router.message(F.text.startswith("/admin"))
async def admin_help(message: Message):
    if message.from_user.id not in settings.ADMIN_IDS:
        return await message.answer("Нет доступа")
    await message.answer("Админ панель:\n/queue — показать 10 в очереди\n/approve <id>\n/reject <id> <причина>")

@router.message(F.text.startswith("/queue"))
async def show_queue(message: Message, session):
    if message.from_user.id not in settings.ADMIN_IDS:
        return await message.answer("Нет доступа")
    repo = ListingRepo(session)
    items = await repo.by_status(ListingStatus.queued, limit=10)
    if not items:
        return await message.answer("Очередь пуста")
    lines = ["Очередь:"]
    for it in items:
        lines.append(f"#{it.id} [{it.category}] {it.city} — {it.title}")
    await message.answer("\n".join(lines))

@router.message(F.text.startswith("/approve"))
async def cmd_approve(message: Message, session):
    if message.from_user.id not in settings.ADMIN_IDS:
        return await message.answer("Нет доступа")
    parts = message.text.split()
    if len(parts) < 2 or not parts[1].isdigit():
        return await message.answer("Используй: /approve <id>")
    await approve_listing(session, int(parts[1]))
    await message.answer("Одобрено")

@router.message(F.text.startswith("/reject"))
async def cmd_reject(message: Message, session):
    if message.from_user.id not in settings.ADMIN_IDS:
        return await message.answer("Нет доступа")
    parts = message.text.split(maxsplit=2)
    if len(parts) < 2 or not parts[1].isdigit():
        return await message.answer("Используй: /reject <id> <причина>")
    reason = parts[2] if len(parts) > 2 else None
    await reject_listing(session, int(parts[1]), reason)
    await message.answer("Отклонено")
