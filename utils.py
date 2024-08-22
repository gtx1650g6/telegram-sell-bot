#     __  __           _         _              ____       _             _      _   
#    |  \/  | __ _  __| | ___   | |__  _   _   |  _ \ __ _| |_ _ __ ___ | | ___| |_ 
#    | |\/| |/ _` |/ _` |/ _ \  | '_ \| | | |  | |_) / _` | __| '__/ _ \| |/ _ \ __|
#    | |  | | (_| | (_| |  __/  | |_) | |_| |  |  __/ (_| | |_| | | (_) | |  __/ |_ 
#    |_|  |_|\__,_|\__,_|\___|  |_.__/ \__, |  |_|   \__,_|\__|_|  \___/|_|\___|\__|
#                                      |___/                                       

import time, json, time, asyncio
from yoomoney import Client

class log:
    def old_log(data: str, array: list) -> None:
        local = time.localtime()
        array.append(f"[DEBUG | {time.strftime("%d.%m.%Y %H:%M:%S", local)}] {data}")
        print("DEBUGGING...")


    def old_write(array: list, folder: str) -> None:
        file_txt = open(f'log-storage/{folder}/{time.strftime("%d.%m.%Y")}.log', 'a', encoding='utf-8')
        for data in array:
            file_txt.write(data+"\n")
        file_txt.close()


    def new_log(data: str, folder: str) -> None:
        """Логгирование действий | Данные для передачи, Папка хранения"""
        local = time.localtime()
        logged = f"[LOG | {time.strftime("%d.%m.%Y %H:%M:%S", local)}] {data}"
        print("LOGGING...")

        file_log = open(f'logs/{folder}/{time.strftime("%d.%m.%Y")}.log', 'a', encoding='utf-8')
        file_log.write(logged+"\n")
        file_log.close()

def read_file(path: str):
    file = open(path, "r", encoding="utf-8")
    data = json.load(file)
    file.close()
    return data

async def yoo_pay_check(id: int, label_u: str, transaction_id: str):
    """Проверка оплаты платёжной системы: Yoomoney | ID пользователя, ID платежа, ID транзакции"""
    from database import users
    token = read_file("config/settings.json")["yoomoney"]
    client = Client(token) 
    history = client.operation_history(label=label_u)
    start_time = time.time()
    time_limit = 3600
    while len(history.operations) == 0:
        elapsed_time = time.time() - start_time
        if elapsed_time > time_limit:
            return False
            
        print(f"Ожидаем оплаты... | {label_u}")
        await asyncio.sleep(3)
        history = client.operation_history(label=label_u)

        for operation in history.operations:
            users.balance(id, operation.amount, operation.operation_id, label_u, transaction_id)