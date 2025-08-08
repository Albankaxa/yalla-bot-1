from aiogram import Router, F
from aiogram.types import Message
from bot.core.i18n import T
from bot.keyboards.common import categories_kb

router = Router()

@router.message(F.text == "/start")
async def start(message: Message):
    await message.answer(T["greet"], reply_markup=categories_kb().as_markup())
