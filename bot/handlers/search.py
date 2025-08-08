from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from bot.keyboards.common import categories_kb, cities_kb
from bot.core.i18n import T
from bot.services.search import search_listings

router = Router()

@router.message(F.text.in_({"🔎 Найти", "/find"}))
async def search_entry(message: Message):
    await message.answer(T["choose_category"], reply_markup=categories_kb().as_markup())

@router.callback_query(F.data.startswith("cat:"))
async def search_choose_category(call: CallbackQuery):
    await call.message.edit_text(T["choose_city"], reply_markup=cities_kb().as_markup())

@router.callback_query(F.data.startswith("city:"))
async def search_choose_city(call: CallbackQuery, session):
    city = call.data.split(":", 1)[1]
    # demo: покажем последние FREE в городе
    listings = await search_listings(session, category="free", city=city, limit=5)
    if not listings:
        return await call.message.edit_text("По твоему запросу пока пусто.")
    text = ["Нашёл:"]
    for lst in listings:
        label = "Бесплатно" if lst.price is None else f"{lst.price} ₪"
        text.append(f"• <b>{lst.title}</b> — {label}\n{lst.description[:120]}…")
    await call.message.edit_text("\n\n".join(text), parse_mode="HTML")
