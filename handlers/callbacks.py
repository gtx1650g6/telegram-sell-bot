#     __  __           _         _              ____       _             _      _   
#    |  \/  | __ _  __| | ___   | |__  _   _   |  _ \ __ _| |_ _ __ ___ | | ___| |_ 
#    | |\/| |/ _` |/ _` |/ _ \  | '_ \| | | |  | |_) / _` | __| '__/ _ \| |/ _ \ __|
#    | |  | | (_| | (_| |  __/  | |_) | |_| |  |  __/ (_| | |_| | | (_) | |  __/ |_ 
#    |_|  |_|\__,_|\__,_|\___|  |_.__/ \__, |  |_|   \__,_|\__|_|  \___/|_|\___|\__|
#                                      |___/                                       

from aiogram import Router, types
from app import bot
from keyboards import payments_kb
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from uuid import uuid4
from Yoomoney import quick
from utils import yoo_pay_check
from keyboards import amount, price, item_buy_kb, go_to_payment, items_payments_kb, item_buy_kb, add_item_kb
from database import users
from handlers.items import buy_item, add_item
import shortuuid
import asyncio
import time

router = Router()

@router.callback_query(lambda c: c.data == 'balance')
async def balance_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "💳 Выберите платёжную систему:", reply_markup=payments_kb)

@router.callback_query(lambda c: c.data == 'transactions')
async def balance_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "🛠️ *В разработке...*", parse_mode='Markdown')

class Form(StatesGroup):
    waiting_for_amount = State()

@router.callback_query(lambda c: c.data == 'Yoomoney')
async def Yoomoney_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await asyncio.sleep(1)
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    
    await bot.answer_callback_query(callback_query.id)
    
    sent_message = await bot.send_message(callback_query.from_user.id, "🔢 Отправьте сумму пополнения:")
    await state.update_data(message_id=sent_message.message_id) 

    await state.set_state(Form.waiting_for_amount)

@router.message(Form.waiting_for_amount)
async def payment_system_handler(message: types.Message, state: FSMContext):
    
    data = await state.get_data()
    message_id = data.get('message_id')

    amount = (message.text)
    amount_id = message.message_id
    ### --- ахуенный костыль 5/5 --- ###
    numbers = [1,2,3,4,5,6,8,8,9,0]
    counter = []

    for letter in amount:
        if letter in str(numbers):
            counter.append("+")
        else:
            pass
    
    if len(counter) == len(amount):
        amount = int(amount)
        if amount < 2:
            await message.reply("Сумма пополнения ниже минимальной: 2₽")
        else:
            if message_id:
                await asyncio.sleep(1)
                await bot.delete_message(message.from_user.id, message_id)
            label = str(uuid4())
            transaction_id = shortuuid.uuid()
            link = quick.balance(amount, label)
            await asyncio.sleep(1)
            await bot.delete_message(message.from_user.id, amount_id)
            keyboard = go_to_payment(url=link)
            msg = await message.answer(f"💰 Сумма платежа: {amount}₽", reply_markup=keyboard)
            checker = await yoo_pay_check(message.from_user.id, label, transaction_id)
            await asyncio.sleep(1)
            await msg.delete()
            if checker == False:
                await message.answer(f"Платёж: {transaction_id} не оплачен.\n⌛️ Время платежа истекло.")
            else:
                await message.answer(f"Платёж: {transaction_id} оплачен.\n✅ Баланс пополнен на {amount}₽")
    else:
        await message.reply("Сумма пополнения должна быть числом.")
    counter.clear()
    await state.clear()
    ### --- ахуенный костыль 5/5 --- ###


####################
class Items_State(StatesGroup):
    items = State()

### --- 2 --- ###
@router.callback_query(lambda c: c.data == 'item-choose-payment', Items_State.items)
async def item_choose_payment_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    data = await state.get_data()
    await asyncio.sleep(1)
    await bot.delete_message(callback_query.from_user.id, data.get('message_money'))
    message = await bot.send_message(callback_query.from_user.id, "💳 Выберите платёжную систему:", reply_markup=items_payments_kb)
    money = data.get('need_money')
    await state.update_data(need_money=money, message_payment=message.message_id)
    await state.set_state(Items_State.items)

### --- 3 --- ###
@router.callback_query(lambda c: c.data == 'item-Yoomoney', Items_State.items)
async def item_Yoomoney_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    data = await state.get_data()
    money = data.get('need_money')
    await asyncio.sleep(1)
    await bot.delete_message(callback_query.from_user.id, data.get('message_payment'))
    label = str(uuid4())
    transaction_id = shortuuid.uuid()
    link = quick.balance(money, label)
    keyboard = go_to_payment(url=link)
    msg = await bot.send_message(callback_query.from_user.id, f"💰 Сумма платежа: {money}₽", reply_markup=keyboard)
    checker = await yoo_pay_check(callback_query.from_user.id, label, transaction_id)
    await asyncio.sleep(1)
    await bot.delete_message(callback_query.from_user.id, msg.message_id)
    if checker == False:
        await bot.send_message(callback_query.from_user.id, f"Платёж: {transaction_id} не оплачен.\n⌛️ Время платежа истекло.")
    else:
        await bot.send_message(callback_query.from_user.id, f"Платёж: {transaction_id} оплачен.\n✅ Баланс пополнен на {money}₽")

### --- 1 --- ###
@router.callback_query(lambda c: c.data == 'discord-nitro-full')
async def discord_nitro_full_callback(callback_query: types.CallbackQuery, state: FSMContext):
    item_price = price.discord_full()
    item_amount = amount('discord_nitro_full')
    user_balance = users.data(callback_query.from_user.id, "money")
    money = item_price - user_balance

    await bot.answer_callback_query(callback_query.id)
    
    if money < 2:
        money = 2

    await state.update_data(need_money=money)

    if item_amount == 0:
        await bot.send_message(callback_query.from_user.id, "Товар: Discord Nitro Boost закончился.")
        return
    
    if user_balance < item_price:
        message = await bot.send_message(callback_query.from_user.id, f"Недостаточно средств: {money}₽.",
                               reply_markup=item_buy_kb)
        await state.update_data(message_money=message.message_id)
        return

    message_2 = await bot.send_message(callback_query.from_user.id, f"Название: *Discord Nitro Boost*\nОписание: Гифт Discord Nitro Boost с гарантией 20 дней\nПреимущества:\n1️⃣ - Доступ к кастомным эмодзи.\n2️⃣ - Анимированный аватар.\n3️⃣ - Баннер в профиле.\n4️⃣ - 2 буста для серверов.\n5️⃣ - Внешний вид: цветные темы\nЦена: *{item_price}₽*\nВ наличии: *{amount('discord_nitro_full')}*",
                           reply_markup=item_buy_kb,
                           parse_mode='Markdown')
    await state.update_data(end_price=item_price,message_2=message_2.message_id)
    await state.update_data(item_name="Discord Nitro Boost")
    await state.set_state(Items_State.items)

@router.callback_query(lambda c: c.data == 'discord-nitro-basic')
async def discord_nitro_basic_callback(callback_query: types.CallbackQuery, state: FSMContext):
    item_price = price.discord_basic()
    item_amount = amount('discord_nitro_basic')
    user_balance = users.data(callback_query.from_user.id, "money")
    money = item_price - user_balance

    await bot.answer_callback_query(callback_query.id)
    
    if money < 2:
        money = 2

    await state.update_data(need_money=money)

    if item_amount == 0:
        await bot.send_message(callback_query.from_user.id, "Товар: Discord Nitro Basic закончился.")
        return
    
    if user_balance < item_price:
        message = await bot.send_message(callback_query.from_user.id, f"Недостаточно средств: {money}₽.",
                               reply_markup=item_buy_kb)
        await state.update_data(message_money=message.message_id)
        return

    message_2 = await bot.send_message(callback_query.from_user.id, f"Название: *Discord Nitro Basic*\nОписание: Гифт Discord Nitro Basic с гарантией 20 дней\nПреимущества:\n1️⃣ - Доступ к кастомным эмодзи.\n2️⃣ - Внешний вид: цветные темы.\nЦена: *{item_price}₽*\nВ наличии: *{amount('discord_nitro_basic')}*",
                           reply_markup=item_buy_kb,
                           parse_mode='Markdown')
    await state.update_data(end_price=item_price,message_2=message_2.message_id)
    await state.update_data(item_name="Discord Nitro Basic")
    await state.set_state(Items_State.items)

@router.callback_query(lambda c: c.data == 'discord-nitro-qr')
async def discord_nitro_qr_callback(callback_query: types.CallbackQuery, state: FSMContext):
    item_price = price.discord_qr()
    item_amount = amount('discord_nitro_qr')
    user_balance = users.data(callback_query.from_user.id, "money")
    money = item_price - user_balance

    await bot.answer_callback_query(callback_query.id)
    
    if money < 2:
        money = 2

    await state.update_data(need_money=money)

    if item_amount == 0:
        await bot.send_message(callback_query.from_user.id, "Товар: Discord Nitro QR закончился.")
        return
    
    if user_balance < item_price:
        message = await bot.send_message(callback_query.from_user.id, f"Недостаточно средств: {money}₽.",
                               reply_markup=item_buy_kb)
        await state.update_data(message_money=message.message_id)
        return

    message_2 = await bot.send_message(callback_query.from_user.id, f"Название: *Discord Nitro QR*\nОписание: Гифт Discord Nitro QR с гарантией 20 дней\nПреимущества:\n1️⃣ - Доступ к кастомным эмодзи.\n2️⃣ - Анимированный аватар.\n3️⃣ - Баннер в профиле.\n4️⃣ - 2 буста для серверов.\n5️⃣ - Внешний вид: цветные темы\nЦена: *{item_price}₽*\nВ наличии: *{amount('discord_nitro_full')}*",
                           reply_markup=item_buy_kb,
                           parse_mode='Markdown')
    await state.update_data(end_price=item_price,message_2=message_2.message_id)
    await state.update_data(item_name="Discord Nitro QR")
    await state.set_state(Items_State.items)

### --- 4 --- ###
@router.callback_query(lambda c: c.data == 'item-buying', Items_State.items)
async def item_buying_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    data = await state.get_data()
    await bot.delete_message(callback_query.from_user.id, data.get('message_2'))
    item_price = data.get('end_price')
    item_name = data.get('item_name')
    users.debalance(callback_query.from_user.id, item_price)
    await asyncio.sleep(1)
    if item_name == "Discord Nitro Boost":
        await bot.send_message(callback_query.from_user.id, "❗️ Обязательно снимайте весь процесс покупки на видео от начала и до выявления какого-либо результата.\n❗️ Если активирует  НИТРО третье лицо, то он должен записать видео активации, чтобы предоставить в случае замены по грантии!")    
        await bot.send_message(callback_query.from_user.id, f"🦠 Дата покупки: {time.strftime("%Y-%m-%d %H:%M:%S")}\n🎲 Тип: Discord Nitro Boost\n🦸🏼‍♂️ Ваш ID: {users.data(callback_query.from_user.id, "userid")}")
        await bot.send_message(callback_query.from_user.id, f"🌵 Ваш товар:\n{buy_item("discord_nitro_full")}")
    elif item_name == "Discord Nitro Basic":
        await bot.send_message(callback_query.from_user.id, "❗️ Обязательно снимайте весь процесс покупки на видео от начала и до выявления какого-либо результата.\n❗️ Если активирует  НИТРО третье лицо, то он должен записать видео активации, чтобы предоставить в случае замены по грантии!")
        await bot.send_message(callback_query.from_user.id, f"🦠 Дата покупки: {time.strftime("%Y-%m-%d %H:%M:%S")}\n🎲 Тип: Discord Nitro Basic\n🦸🏼‍♂️ Ваш ID: {users.data(callback_query.from_user.id, "userid")}")
        await bot.send_message(callback_query.from_user.id, f"🌵 Ваш товар:\n{buy_item("discord_nitro_basic")}")
    elif item_name == "Discord Nitro QR":
        await bot.send_message(callback_query.from_user.id, "❗️ Обязательно снимайте весь процесс покупки на видео от начала и до выявления какого-либо результата.\n❗️ Если активирует  НИТРО третье лицо, то он должен записать видео активации, чтобы предоставить в случае замены по грантии!")
        await bot.send_message(callback_query.from_user.id, f"🦠 Дата покупки: {time.strftime("%Y-%m-%d %H:%M:%S")}\n🎲 Тип: Discord Nitro QR\n🦸🏼‍♂️ Ваш ID: {users.data(callback_query.from_user.id, "userid")}")
        await bot.send_message(callback_query.from_user.id, f"🌵 Ваш товар:\n{buy_item("discord_nitro_qr")}")
    await state.clear()
############################
class ItemState(StatesGroup):
    waiting_for_item_text = State()

@router.callback_query(lambda c: c.data == 'add-item')
async def add_item_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Выберите добавляемый товар:", 
                           reply_markup=add_item_kb)

@router.callback_query(lambda c: c.data == 'add-item-discord-nitro-full')
async def add_item_callback(callback: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback.id)
    await bot.send_message(callback.from_user.id, "Отправьте текстом товар. | Discord Nitro Boost")
    await state.update_data(item_name="discord_nitro_full")
    await state.set_state(ItemState.waiting_for_item_text)

@router.callback_query(lambda c: c.data == 'add-item-discord-nitro-basic')
async def add_item_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Отправьте текстом товар. | Discord Nitro Basic")
    await state.update_data(item_name="discord_nitro_basic")
    await state.set_state(ItemState.waiting_for_item_text)

@router.callback_query(lambda c: c.data == 'add-item-discord-nitro-qr')
async def add_item_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Отправьте текстом товар. | Discord Nitro QR")
    await state.update_data(item_name="discord_nitro_qr")
    await state.set_state(ItemState.waiting_for_item_text)

@router.message(ItemState.waiting_for_item_text)
async def process_item_text(message: types.Message, state: FSMContext):
    item_text = message.text
    data = await state.get_data()

    add_item(data['item_name'], item_text)
    await message.reply("Товар добавлен!")

    await state.clear()