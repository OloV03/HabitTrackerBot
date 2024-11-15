from aiogram import Router, types
from aiogram.filters.command import Command
from api import Api
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

habit_router = Router()


@habit_router.message(Command("add_habit"))
async def add_habbit(message: types.Message):
    """Добавление новой привычки"""
    user_id = message.from_user.id
    mes_text_arr = message.text.split(' ')

    Api.add_habit_to_user(user_id=user_id, habit_nm=mes_text_arr[1])
    await message.answer(text="Привычка добавлена")


@habit_router.message(Command("habits_list"))
async def get_list_habits(message: types.Message):
    """Получение списка привычек"""
    user_id = message.from_user.id
    habits_list = Api.list_user_habits(user_id=user_id)

    keyboard_builder = InlineKeyboardBuilder()
    for id, name in habits_list:
        keyboard_builder.add(InlineKeyboardButton(text=name, callback_data=f'habit_{id}'))

    await message.answer(text="Список привычек", reply_markup=keyboard_builder.as_markup())

@habit_router.message(Command("add_event"))
async def add_event(message: types.Message):
    """Добавление записи о выполнении привычки"""
    user_id = message.from_user.id
    mes_text_arr = message.text.split(' ')
    
    Api.add_event(
        user_id=user_id,
        habit_id=mes_text_arr[1],
        event_ts=mes_text_arr[2],
        comment=' '.join(mes_text_arr[3:])
    )

    await message.answer(text="Готово")


