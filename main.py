
import os
import logging
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = os.getenv("YOUR_BOT_TOKEN")
if not API_TOKEN:
    raise ValueError("❌ Ошибка: переменная окружения 'YOUR_BOT_TOKEN' не задана.")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("👋 Привет! Добро пожаловать в Yalla Bot!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
