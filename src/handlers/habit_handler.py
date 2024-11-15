from aiogram import Router, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.command import Command
from aiogram import F
from api import Api
from typing import List


habit_router = Router()
max_habit_in_page = 4

def habits_inline_keyboard(habits_list: List[str], start_index: int, callback_pattern: str = "empty") -> InlineKeyboardMarkup:
    """
    Подготовленная страница кнопок с привычками

    Parameters
    ---
    habits_list: List[str]
        Список названий привычек пользователя

    start_index: int
        Индекс, с которого начинается чтение привычек для текущей "страницы"

    callback_pattern: str | None
        Шаблон для `callback_data` кнопок
    
    Return
    ---
    InlineKeyboardMarkup
        Клавиатура c названиями привычек.

        - Если кнопок больше чем `max_habit_in_page` - вернется максимально возможное кол-во кнопок и кнопка `Далее`, которая обновит набор.
        - Если есть привычки на предыдущих страницах (`start_index` > 0) - будет добавлена кнопка `Назад`.
    """
    keyboard_builder = InlineKeyboardBuilder()
    buttons =[]
    i = 0
    need_next_page = False
    for id, name in habits_list[start_index:]:
        if i >= max_habit_in_page:
            need_next_page = True
            break
        buttons.append(
            InlineKeyboardButton(text=name, callback_data=f"{callback_pattern}_{id}" if callback_pattern else None)
        )
        i += 1
    keyboard_builder.row(*buttons, width=2)

    last_row_buttons = []
    if start_index > 0:
        last_row_buttons.append(InlineKeyboardButton(text="Назад", callback_data=f'prev_page_{start_index - max_habit_in_page - 1}'))

    if need_next_page:
        last_row_buttons.append(InlineKeyboardButton(text="Далее", callback_data=f'next_page_{start_index + i + 1}'))

    keyboard_builder.row(*last_row_buttons)

    return keyboard_builder.as_markup()


@habit_router.message(Command("add_habit"))
async def add_habbit(message: types.Message):
    """Добавление новой привычки"""
    user_id = message.from_user.id

    Api.add_habit_to_user(user_id=user_id, habit_nm=message.text)
    await message.answer(text="Привычка добавлена")

@habit_router.message(Command("habits_list"))
async def get_list_habits(message: types.Message):
    """Получение списка привычек"""
    user_id = message.from_user.id
    habits_list = Api.list_user_habits(user_id=user_id)

    await message.answer(
        text="Ваши привычки:", reply_markup=habits_inline_keyboard(habits_list=habits_list, start_index=0)
    )

@habit_router.callback_query(F.data.startswith("next_page"))
async def next_page_callback(callback: types.CallbackQuery):
    """Callback для кнопки "Далее" """
    start_index = int(callback.data.title().lower().split('_')[-1])
    user_id=callback.from_user.id
    
    habits_list = Api.list_user_habits(user_id=user_id)
    new_keyboard = habits_inline_keyboard(habits_list=habits_list, start_index=start_index)
    
    await callback.message.edit_reply_markup(reply_markup=new_keyboard)

@habit_router.callback_query(F.data.startswith("prev_page"))
async def prev_page_callback(callback: types.CallbackQuery):
    """Callback для кнопки "Назад" """
    start_index = int(callback.data.title().lower().split('_')[-1])
    user_id=callback.from_user.id
    
    habits_list = Api.list_user_habits(user_id=user_id)
    new_keyboard = habits_inline_keyboard(habits_list=habits_list, start_index=start_index)
    
    await callback.message.edit_reply_markup(reply_markup=new_keyboard)

@habit_router.callback_query(F.data.startswith("event_habit"))
async def add_event_callback(callback: types.CallbackQuery):
    """Callback для добавления записи привычки"""
    user_id = callback.from_user.id
    habit_id = callback.data.split('_')[-1]
    Api.add_event(
        user_id=user_id,
        habit_id=habit_id
    )
    callback.message.delete_reply_markup()

    await callback.message.edit_text("Запись добавлена")

@habit_router.message(Command("add_event"))
async def add_event(message: types.Message):
    """Добавление записи о выполнении привычки"""
    user_id = message.from_user.id
    habits_list = Api.list_user_habits(user_id=user_id)

    await message.answer(
        text="Выберите привычку:", reply_markup=habits_inline_keyboard(habits_list=habits_list, start_index=0, callback_pattern="event_habit")
    )
