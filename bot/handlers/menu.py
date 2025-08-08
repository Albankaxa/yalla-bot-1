from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from bot.core.i18n import T
from bot.keyboards.common import categories_kb, cities_kb

router = Router()

@router.message(F.text.in_({"меню", "/menu", "menu"}))
async def show_menu(message: Message):
    await message.answer(T["greet"], reply_markup=categories_kb().as_markup())

@router.callback_query(F.data.startswith("cat:"))
async def on_category(call: CallbackQuery):
    await call.message.edit_text(T["choose_city"], reply_markup=cities_kb().as_markup())
