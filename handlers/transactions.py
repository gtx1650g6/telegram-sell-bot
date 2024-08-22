#     __  __           _         _              ____       _             _      _   
#    |  \/  | __ _  __| | ___   | |__  _   _   |  _ \ __ _| |_ _ __ ___ | | ___| |_ 
#    | |\/| |/ _` |/ _` |/ _ \  | '_ \| | | |  | |_) / _` | __| '__/ _ \| |/ _ \ __|
#    | |  | | (_| | (_| |  __/  | |_) | |_| |  |  __/ (_| | |_| | | (_) | |  __/ |_ 
#    |_|  |_|\__,_|\__,_|\___|  |_.__/ \__, |  |_|   \__,_|\__|_|  \___/|_|\___|\__|
#                                      |___/                                       

from aiogram import Router, types
from aiogram.filters import Command
from keyboards import move_kb
from database import transactions

router = Router()

messages = []

current_index = 0

@router.message(Command("check"))
async def send_message(message: types.Message):
    global current_index
    
    transactions_list = transactions.get_all_from_userid(message.from_user.id)

    if len(transactions_list) == 0:
        await message.answer("У вас ещё нет транзакций")
        return

    for k in range(len(transactions_list)):
        messages.append(f"Тип: {transactions_list[k][2]}, Количество: {transactions_list[k][0]}\nID: {transactions_list[k][1]}")

    await message.answer(
        text=messages[current_index],
        reply_markup=await move_kb(current_index, messages)
    )

@router.callback_query(lambda c: c.data in ('back', 'forward'))
async def handle_callback_query(call: types.CallbackQuery):
    global current_index

    if call.data == 'back':
        current_index = max(0, current_index - 1)
    elif call.data == 'forward':
        current_index = min(len(messages) - 1, current_index + 1)

    await call.message.edit_text(
        text=messages[current_index],
        reply_markup=await move_kb(current_index, messages)
    )