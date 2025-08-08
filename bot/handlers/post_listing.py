from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from bot.states.listing import ListingForm
from bot.keyboards.common import categories_kb, cities_kb
from bot.core.i18n import T
from bot.db.repo import UserRepo
from bot.services.listings import create_listing

router = Router()

@router.message(F.text.in_({"➕ Подать объявление", "/post"}))
async def post_entry(message: Message, state: FSMContext):
    await state.set_state(ListingForm.category)
    await state.update_data(media=[])
    await message.answer(T["choose_category"], reply_markup=categories_kb().as_markup())

@router.callback_query(ListingForm.category, F.data.startswith("cat:"))
async def choose_category(call: CallbackQuery, state: FSMContext):
    category = call.data.split(":", 1)[1]
    await state.update_data(category=category)
    await state.set_state(ListingForm.city)
    await call.message.edit_text(T["choose_city"], reply_markup=cities_kb().as_markup())

@router.callback_query(ListingForm.city, F.data.startswith("city:"))
async def choose_city(call: CallbackQuery, state: FSMContext):
    city = call.data.split(":", 1)[1]
    await state.update_data(city=city)
    await state.set_state(ListingForm.title)
    await call.message.edit_text(T["enter_title"])

@router.message(ListingForm.title)
async def set_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text[:120])
    await state.set_state(ListingForm.description)
    await message.answer(T["enter_description"])

@router.message(ListingForm.description)
async def set_desc(message: Message, state: FSMContext):
    await state.update_data(description=message.text[:4096])
    data = await state.get_data()
    if data.get("category") == "free":
        await state.set_state(ListingForm.media)
        await message.answer(T["add_media"])
    else:
        await state.set_state(ListingForm.price)
        await message.answer(T["enter_price"])

@router.message(ListingForm.price)
async def set_price(message: Message, state: FSMContext):
    price = None
    if message.text and message.text.isdigit():
        price = int(message.text)
    await state.update_data(price=price)
    await state.set_state(ListingForm.media)
    await message.answer(T["add_media"])

@router.message(ListingForm.media, F.photo)
async def add_photo(message: Message, state: FSMContext):
    data = await state.get_data()
    media = data.get("media", [])
    if len(media) >= 10:
        return await message.answer("Достигнут лимит 10 файлов. Нажми 'Далее'.")
    file_id = message.photo[-1].file_id
    media.append(file_id)
    await state.update_data(media=media)

@router.message(ListingForm.media, F.video)
async def add_video(message: Message, state: FSMContext):
    data = await state.get_data()
    media = data.get("media", [])
    if len(media) >= 10:
        return await message.answer("Достигнут лимит 10 файлов. Нажми 'Далее'.")
    media.append(message.video.file_id)
    await state.update_data(media=media)

@router.message(ListingForm.media, F.text.casefold().in_({"далее", "готово", "next"}))
async def media_done(message: Message, state: FSMContext):
    await state.set_state(ListingForm.contact)
    await message.answer(T["enter_contact"])

@router.message(ListingForm.contact)
async def set_contact(message: Message, state: FSMContext, session):
    await state.update_data(contact=message.text[:128])
    data = await state.get_data()
    price_text = "Бесплатно" if data.get("category") == "free" else (f"Цена: {data.get('price')} ₪" if data.get('price') else "Цена не указана")
    preview = (
        f"<b>{data['title']}</b>\n"
        f"{data['description']}\n\n"
        f"Город: {data['city']}\n"
        f"Категория: {data['category']}\n"
        f"{price_text}\n"
        f"Контакт: {data['contact']}"
    )
    await state.set_state(ListingForm.review)
    await message.answer(preview, parse_mode="HTML")
    await message.answer(T["review_submit"] + "\nОтветь: 'Отправить' или 'Назад'")

@router.message(ListingForm.review, F.text.casefold() == "отправить")
async def submit_listing(message: Message, state: FSMContext, session):
    data = await state.get_data()
    user_repo = UserRepo(session)
    user = await user_repo.get_or_create(message.from_user.id)

    await create_listing(
        session,
        user_id=user.id,
        category=data["category"],
        city=data["city"],
        title=data["title"],
        description=data["description"],
        price=None if data["category"] == "free" else data.get("price"),
        media=data.get("media", []),
        contact=data["contact"],
    )
    await state.clear()
    await message.answer(T["queued"])

@router.message(ListingForm.review, F.text.casefold() == "назад")
async def review_back(message: Message, state: FSMContext):
    await state.set_state(ListingForm.contact)
    await message.answer(T["enter_contact"])
