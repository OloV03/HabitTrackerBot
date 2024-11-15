from aiogram import Router, types
from aiogram.filters.command import Command
from api import Api

statistics_router = Router()


@statistics_router.message(Command("last"))
async def last_event(message: types.Message):
    """Последняя запись о привычке"""
    
    last_event = Api.last_event(
        message.from_user.id,
        message.text.split(' ')[1]
    )

    await message.answer(text=f"Дата последней записи: {last_event}")
