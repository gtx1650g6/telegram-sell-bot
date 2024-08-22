#     __  __           _         _              ____       _             _      _   
#    |  \/  | __ _  __| | ___   | |__  _   _   |  _ \ __ _| |_ _ __ ___ | | ___| |_ 
#    | |\/| |/ _` |/ _` |/ _ \  | '_ \| | | |  | |_) / _` | __| '__/ _ \| |/ _ \ __|
#    | |  | | (_| | (_| |  __/  | |_) | |_| |  |  __/ (_| | |_| | | (_) | |  __/ |_ 
#    |_|  |_|\__,_|\__,_|\___|  |_.__/ \__, |  |_|   \__,_|\__|_|  \___/|_|\___|\__|
#                                      |___/                                       

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from os import listdir
from utils import read_file

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🛒 Товар"), KeyboardButton(text="👤 Профиль")],
        [KeyboardButton(text="🔰 О магазине"), KeyboardButton(text="📱 Администраторы")],
        [KeyboardButton(text="⚜️ Создатель бота")]
    ],
    resize_keyboard=False,
    row_width=1 
)

admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🛒 Купить товар"), KeyboardButton(text="👤 Профиль")],
        [KeyboardButton(text="🔰 О магазине"), KeyboardButton(text="📱 Администраторы")],
        [KeyboardButton(text="⚙️ Админ панель")]
    ],
    resize_keyboard=False,
    row_width=1
)

payments_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Yoomoney", callback_data="Yoomoney")],
        [InlineKeyboardButton(text="В разработке...", callback_data="new-payment-method")],
    ]
)

profile_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Пополнить баланс", callback_data="balance")],
        [InlineKeyboardButton(text="Просмотреть транзакции", callback_data="transactions")],
    ]
)

def go_to_payment(url: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Перейти к оплате", url=url)]
        ]
    )

def move_kb(index: int, messages: list):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    buttons = []
    if index > 0:
        buttons.append(InlineKeyboardButton(text="Назад", callback_data="back"))
    if index < len(messages) - 1:
        buttons.append(InlineKeyboardButton(text="Вперёд", callback_data="forward"))
    
    if buttons:  # Добавляем кнопки в клавиатуру, если они есть
        keyboard.inline_keyboard.append(buttons)

    return keyboard

def amount(folder: str):
    return len(listdir(f"./items/{folder}"))

data = read_file("config/price.json")
class price:
    def discord_full() -> int:
        return data["discord-full"]

    def discord_basic() -> int:
        return data["discord-basic"]

    def discord_qr() -> int:
        return data["discord-qr"]

def items_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"Discord Nitro Boost | {price.discord_full()}₽ | {amount('discord_nitro_full')}шт.", callback_data="discord-nitro-full")],
            [InlineKeyboardButton(text=f"Discord Nitro Basic | {price.discord_basic()}₽ | {amount('discord_nitro_basic')}шт.", callback_data="discord-nitro-basic")],
            [InlineKeyboardButton(text=f"Discord Nitro QR | {price.discord_qr()}₽ | {amount('discord_nitro_qr')}шт.", callback_data="discord-nitro-qr")]
        ]
    )


item_buy_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Пополнить баланс", callback_data="item-choose-payment")]
    ]
)

items_payments_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Yoomoney", callback_data="item-Yoomoney")],
        [InlineKeyboardButton(text="В разработке...", callback_data="new-payment-method")],
    ]
)

item_buy_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Купить", callback_data="item-buying")]
    ]
)

admin_panel_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Добавить товар", callback_data="add-item")]
    ]
)

add_item_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Discord Nitro Boost", callback_data="add-item-discord-nitro-full")],
        [InlineKeyboardButton(text="Discord Nitro Basic", callback_data="add-item-discord-nitro-basic")],
        [InlineKeyboardButton(text="Discord Nitro QR", callback_data="add-item-discord-nitro-qr")],
    ]
)