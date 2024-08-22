#     __  __           _         _              ____       _             _      _   
#    |  \/  | __ _  __| | ___   | |__  _   _   |  _ \ __ _| |_ _ __ ___ | | ___| |_ 
#    | |\/| |/ _` |/ _` |/ _ \  | '_ \| | | |  | |_) / _` | __| '__/ _ \| |/ _ \ __|
#    | |  | | (_| | (_| |  __/  | |_) | |_| |  |  __/ (_| | |_| | | (_) | |  __/ |_ 
#    |_|  |_|\__,_|\__,_|\___|  |_.__/ \__, |  |_|   \__,_|\__|_|  \___/|_|\___|\__|
#                                      |___/                                       

from aiogram import Router, types
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import Message
from database import users, admins
from keyboards import start_kb, admin_kb
import time

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    users.new(message.from_user.username, message.from_user.id)
    admins_list = admins.all()
    for k in range(len(admins_list)):
        if admins_list[k][1] == message.from_user.id:
            await message.answer(f'<b>Добро пожаловать, {message.from_user.full_name}!</b>',
                         parse_mode='HTML', 
                         reply_markup=admin_kb)
            return
        else:
            await message.answer(f'<b>Добро пожаловать, {message.from_user.full_name}!</b>',
                         parse_mode='HTML', 
                         reply_markup=start_kb)
            return

@router.message(Command('log'))
async def log_handler(message: types.Message, command: CommandObject):
    """Обрабатывает команду /log"""
    
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
        
        date = time.strftime('%d.%m.%Y')
        
        if len(args) == 1:
            folder = args[0]
            log = open(f'logs/{folder}/{date}.log', 'r', encoding='utf-8').read()
            
            await message.answer(f"<b>📒 Лог: {folder}</b>\n\n{log}", parse_mode='HTML')
        else:
            await message.reply("Неверное количество аргументов. Используйте /log <folder>")

@router.message(lambda message: message.text.lower()[2:] == "о магазине")
async def creator_message_handler(message: types.Message):
    """Обрабатывает сообщения о магазине"""
    file = open("config/about.txt", "r", encoding="utf-8")
    text = file.read()
    await message.answer(text,parse_mode='Markdown')
