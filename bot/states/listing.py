from aiogram.fsm.state import StatesGroup, State

class ListingForm(StatesGroup):
    category = State()
    city = State()
    title = State()
    description = State()
    price = State()
    media = State()
    contact = State()
    review = State()
