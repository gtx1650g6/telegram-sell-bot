#     __  __           _         _              ____       _             _      _   
#    |  \/  | __ _  __| | ___   | |__  _   _   |  _ \ __ _| |_ _ __ ___ | | ___| |_ 
#    | |\/| |/ _` |/ _` |/ _ \  | '_ \| | | |  | |_) / _` | __| '__/ _ \| |/ _ \ __|
#    | |  | | (_| | (_| |  __/  | |_) | |_| |  |  __/ (_| | |_| | | (_) | |  __/ |_ 
#    |_|  |_|\__,_|\__,_|\___|  |_.__/ \__, |  |_|   \__,_|\__|_|  \___/|_|\___|\__|
#                                      |___/                                       

from aiogram import Router, types
from keyboards import items_kb
import os
import random

router = Router()

@router.message(lambda message: message.text.lower()[2:] == "купить товар")
async def items_handler(message: types.Message):
    """Обрабатывает сообщения о магазине"""
    from utils import read_file
    data = read_file("config/settings.json")
    await message.answer(f"🎁 *Выберите нужный вам товар:*\n├📄 [Инструкция покупки]({data["instruction"]})\n└📰 [ТГК с новостями по товару]({data["telegram-channel-link"]})",
                         parse_mode='Markdown',
                         disable_web_page_preview=True,
                         reply_markup=items_kb())
    
# сделай возможность сразу несколько раз купить товар 1-5 товаров макс
# стоит учесть что если товара мало, то придётся в инлайн клавиатуре кнопки убрать
# например в наличии 3 товара - 3 кнопки, а не 5
def buy_item(item_name: str) -> str:
    items = os.listdir(f"./items/{item_name}")
    get_item = items[0]
    item = open(f"./items/{item_name}/{get_item}", "r")
    data = item.read()
    item.close()
    os.remove(f"./items/{item_name}/{get_item}")
    return data

def add_item(item_name: str, data: str) -> bool:
    path = f"./items/{item_name}"
    file_name = random.randint(99,999999)
    file = open(f"{path}/{file_name}.txt", "w", encoding="utf-8")
    file.write(data)
    file.close()
    return True