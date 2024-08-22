#     __  __           _         _              ____       _             _      _   
#    |  \/  | __ _  __| | ___   | |__  _   _   |  _ \ __ _| |_ _ __ ___ | | ___| |_ 
#    | |\/| |/ _` |/ _` |/ _ \  | '_ \| | | |  | |_) / _` | __| '__/ _ \| |/ _ \ __|
#    | |  | | (_| | (_| |  __/  | |_) | |_| |  |  __/ (_| | |_| | | (_) | |  __/ |_ 
#    |_|  |_|\__,_|\__,_|\___|  |_.__/ \__, |  |_|   \__,_|\__|_|  \___/|_|\___|\__|
#                                      |___/                                       

from aiogram import Router, types
from database import admins
from keyboards import admin_panel_kb

router = Router()

@router.message(lambda message: message.text.lower()[3:] == "админ панель")
async def admin_panel_handler(message: types.Message):
    """Обрабатывает сообщения о магазине"""
    
    admins_list = admins.all()
    admin_rights = False

    for k in range(len(admins_list)):
        if admins_list[k][1] == message.from_user.id:
            admin_rights = True

    if admin_rights == False:
        await message.reply("У вас недостаточно прав.")
        return
    
    await message.answer(f"📎 Ваш Никнейм: @{admins.data(message.from_user.id, 'username')}\n🆔 Ваш ID: {message.from_user.id}\n\n🔫 Выберите действие: ",
                         reply_markup=admin_panel_kb)
    