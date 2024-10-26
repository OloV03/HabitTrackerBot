from aiogram import Router, types
from aiogram.filters.command import Command
from api import Api

habit_router = Router()


@habit_router.message(Command("add_habit"))
async def add_habbit(message: types.Message):
    user_id = message.from_user.id
    mes_text_arr = message.text.split(' ')

    Api.add_habit_to_user(user_id=user_id, habit_nm=mes_text_arr[1])
    await message.answer(text="Привычка добавлена")


@habit_router.message(Command("habits_list"))
async def get_list_habits(message: types.Message):
    user_id = message.from_user.id
    habits_list = Api.list_user_habits(user_id=user_id)

    text_mes = f"""Список привычек:
    {', '.join([f"{x.habit_id} - {x.habit_nm}" for x in habits_list])}
    """
    await message.answer(text=text_mes)

@habit_router.message(Command("add_event"))
async def add_event(message: types.Message):
    user_id = message.from_user.id
    mes_text_arr = message.text.split(' ')
    
    Api.add_event(
        user_id=user_id,
        habit_id=mes_text_arr[1],
        event_ts=mes_text_arr[2],
        comment=' '.join(mes_text_arr[3:])
    )

    await message.answer(text="Готово")
