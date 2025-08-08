from aiogram.utils.keyboard import InlineKeyboardBuilder

CATEGORIES = {
    "work": "👷 Работа",
    "rent": "🏠 Аренда жилья",
    "car": "🚗 Авто",
    "events": "🎭 Мероприятия",
    "free": "🎁 Даром",
}

CITIES = [
    "Тель-Авив", "Иерусалим", "Хайфа", "Беэр-Шева", "Нетания", "Ашдод",
    "Ришон-ле-Цион", "Петах-Тиква", "Херцлия", "Бат-Ям", "Холон", "Кфар-Саба",
]

def categories_kb() -> InlineKeyboardBuilder:
    kb = InlineKeyboardBuilder()
    for key, label in CATEGORIES.items():
        kb.button(text=label, callback_data=f"cat:{key}")
    kb.adjust(2)
    return kb

def cities_kb() -> InlineKeyboardBuilder:
    kb = InlineKeyboardBuilder()
    for city in CITIES:
        kb.button(text=city, callback_data=f"city:{city}")
    kb.adjust(2)
    return kb
