#     __  __           _         _              ____       _             _      _   
#    |  \/  | __ _  __| | ___   | |__  _   _   |  _ \ __ _| |_ _ __ ___ | | ___| |_ 
#    | |\/| |/ _` |/ _` |/ _ \  | '_ \| | | |  | |_) / _` | __| '__/ _ \| |/ _ \ __|
#    | |  | | (_| | (_| |  __/  | |_) | |_| |  |  __/ (_| | |_| | | (_) | |  __/ |_ 
#    |_|  |_|\__,_|\__,_|\___|  |_.__/ \__, |  |_|   \__,_|\__|_|  \___/|_|\___|\__|
#                                      |___/                                       

from aiogram import Router, types
from aiogram.filters import Command, CommandObject
from database import users, admins

router = Router()

@router.message(Command('rights'))
async def give_admin_rights_handler(message: types.Message, command: CommandObject):
    """Обрабатывает команду /rights <userid>"""
    
    admins_list = admins.all()
    admin_rights = False

    for k in range(len(admins_list)):
        if admins_list[k][1] == message.from_user.id:
            admin_rights = True

    if admin_rights == False:
        await message.reply("У вас недостаточно прав.")
        return
        
    args = command.args
    
    if args:
        args = args.split()

        if len(args) == 1:
            userid = args[0]
            try:
                userid = int(userid)
                try:
                    username = users.data(userid, 'username')
                    admins.new(username, userid, message.from_user.username, message.from_user.id)
                    await message.answer(f'Вы выдали админку {username}!')
                except TypeError:
                    await message.reply(f"Пользователь с ID {userid} не найден.")
            except ValueError:
                await message.reply("Неободимо ввести числовое значение.")
        else:
            await message.reply("Неверное количество аргументов. Используйте /rights <userid>")
    else:
        await message.reply("Введите ID пользователя после команды /rights.")

@router.message(Command('delete_admin'))
async def delete_admin_handler(message: types.Message, command: CommandObject):
    """Обрабатывает команду /delete_admin <userid>"""

    admins_list = admins.all()
    admin_rights = False

    for k in range(len(admins_list)):
        if admins_list[k][1] == message.from_user.id:
            admin_rights = True

    if admin_rights == False:
        await message.reply("У вас недостаточно прав.")
        return
    
    args = command.args
    if args:
        args = args.split()

        if len(args) == 1:
            userid = args[0]
            try:
                userid = int(userid)
                try:
                    username = users.data(userid, 'username')
                    admins.delete(userid, message.from_user.id)
                    await message.answer(f'Вы удалили админку {username}!')
                except TypeError:
                    await message.reply(f"Пользователь с ID {userid} не найден.")
            except ValueError:
                await message.reply("Необходимо ввести числовое значение.")

@router.message(Command('admins'))
async def admins_list_handler(message: types.Message):
    """Обрабатывает команду /admins"""
    admin_list = admins.all()
    tags = []
    ids = []

    for k in range(len(admin_list)):
        for j in range(len(admin_list[k])):
            if j == 1:
                ids.append(str(admin_list[k][j]))
            if j == 2:
                tags.append(f"@{admin_list[k][j]}")

    admin_info = [f"{tag} - {id_}" for tag, id_ in zip(tags, ids)]
    
    await message.answer(f'🛡️ <b><u>Администраторы</u></b>\n{"\n".join(admin_info)}', parse_mode='HTML')

@router.message(lambda message: message.text.lower()[2:] == "администраторы")
async def admins_list_message_handler(message: types.Message):
    admins_list = admins.all()
    tags = []
    ids = []

    for k in range(len(admins_list)):
        ids.append(admins_list[k][1])
        tags.append(f"@{admins_list[k][2]}")

    admin_info = [f"{tag} - {id_}" for tag, id_ in zip(tags, ids)]
    
    await message.answer(f'🛡️ <b><u>Администраторы</u></b>\n\n{"\n".join(admin_info)}', parse_mode='HTML')

@router.message(lambda message: message.text.lower()[3:] == "создатель бота")
async def creator_message_handler(message: types.Message):
    await message.answer("<b>По поводу создания бота писать только - @zxcvbnm7442.</b>",
                         parse_mode='HTML')