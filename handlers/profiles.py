#     __  __           _         _              ____       _             _      _   
#    |  \/  | __ _  __| | ___   | |__  _   _   |  _ \ __ _| |_ _ __ ___ | | ___| |_ 
#    | |\/| |/ _` |/ _` |/ _ \  | '_ \| | | |  | |_) / _` | __| '__/ _ \| |/ _ \ __|
#    | |  | | (_| | (_| |  __/  | |_) | |_| |  |  __/ (_| | |_| | | (_) | |  __/ |_ 
#    |_|  |_|\__,_|\__,_|\___|  |_.__/ \__, |  |_|   \__,_|\__|_|  \___/|_|\___|\__|
#                                      |___/                                       

from aiogram import Router, types
from database import users, admins
from keyboards import profile_kb
import datetime

router = Router()

@router.message(lambda message: message.text.lower()[2:] == "профиль")
async def profile_message_handler(message: types.Message):
    id_for_db = message.from_user.id
    data = users.profile(id_for_db)
    time = datetime.datetime.fromisoformat(data[3])
    admins_list = admins.all()
    rights = "Пользователь"

    for k in range(len(admins_list)):
        if admins_list[k][1] == message.from_user.id:
            rights = "Администратор"

    await message.answer(
        f"<b>> <u>Данные телеграм аккаунта</u></b>\n\n📎 <b>Никнейм:</b> @{data[1]}\n✉ <b>Айди:</b> {id_for_db}\n\n\n<b>> <u>Данные аккаунта в боте</u></b>\n\n🆔 <b>Айди:</b> {data[0]} \n💳 <b>Баланс:</b> {data[2]}₽\n📅 <b>Дата регистрации:</b> {time.strftime("%d.%m.%Y")}\n🧩 <b>Права: </b> {rights}\n\n\n<b>> <u>Донат</u></b>\n\n📈 <b>Всего пополнений: </b>{data[4]}₽\n📉 <b>Всего потрачено: </b>{data[5]}₽",
        parse_mode="HTML",
        reply_markup=profile_kb
    )
