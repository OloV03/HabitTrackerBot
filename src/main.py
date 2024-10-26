import asyncio
from bot import HabitTrackBot

if __name__ == '__main__':
    bot = HabitTrackBot()
    asyncio.run(bot.run_bot())
