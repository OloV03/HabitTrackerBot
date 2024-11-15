from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from config_reader import config
from handlers.habit_handler import habit_router
from handlers.statistic_handler import statistics_router


class HabitTrackBot:
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()

    def __init__(self):
        self.dp.include_routers(
            habit_router,
            statistics_router,
        )

    @dp.message(Command("start"))
    async def welcome(message: types.message):
        await message.answer(text="Test")

    async def run_bot(self):
        await self.bot.delete_webhook(drop_pending_updates=True)
        await self.dp.start_polling(self.bot)
