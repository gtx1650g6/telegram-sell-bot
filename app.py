#     __  __           _         _              ____       _             _      _   
#    |  \/  | __ _  __| | ___   | |__  _   _   |  _ \ __ _| |_ _ __ ___ | | ___| |_ 
#    | |\/| |/ _` |/ _` |/ _ \  | '_ \| | | |  | |_) / _` | __| '__/ _ \| |/ _ \ __|
#    | |  | | (_| | (_| |  __/  | |_) | |_| |  |  __/ (_| | |_| | | (_) | |  __/ |_ 
#    |_|  |_|\__,_|\__,_|\___|  |_.__/ \__, |  |_|   \__,_|\__|_|  \___/|_|\___|\__|
#                                      |___/                                       

from aiogram import Bot, Dispatcher
from utils import read_file
import asyncio
import handlers.profiles
import handlers.rights
import handlers.other
import handlers.callbacks
import handlers.items
import handlers.admin

token = read_file("config/settings.json")["telegram"]

bot = Bot(token=token)
dp = Dispatcher()

async def main():

    dp.include_routers(handlers.profiles.router,
                       handlers.rights.router,
                       handlers.other.router,
                       handlers.callbacks.router,
                       handlers.items.router,
                       handlers.admin.router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    try: 
        print("BOT STARTED")
        asyncio.run(main()) 
    except KeyboardInterrupt: 
        print("BOT STOPPED")

