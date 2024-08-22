#     __  __           _         _              ____       _             _      _   
#    |  \/  | __ _  __| | ___   | |__  _   _   |  _ \ __ _| |_ _ __ ___ | | ___| |_ 
#    | |\/| |/ _` |/ _` |/ _ \  | '_ \| | | |  | |_) / _` | __| '__/ _ \| |/ _ \ __|
#    | |  | | (_| | (_| |  __/  | |_) | |_| |  |  __/ (_| | |_| | | (_) | |  __/ |_ 
#    |_|  |_|\__,_|\__,_|\___|  |_.__/ \__, |  |_|   \__,_|\__|_|  \___/|_|\___|\__|
#                                      |___/                                       

from database.config import connection, cursor
from utils import log
import datetime
import shortuuid

def new(username: str, userid: int) -> None:
    """Добавление нового пользователя в базу данных | Никнейм цели, ID цели"""
    cursor.execute("SELECT 1 FROM users WHERE userid = ?", (userid,))
    existing_user = cursor.fetchone()

    if existing_user:
        print(f"Пользователь с ID {userid} уже существует в базе данных.")
    else:
        timestamp = datetime.datetime.now().isoformat()
        cursor.execute(
            """INSERT INTO users (userid, username, money, register_date, all_money, spend_money) VALUES (?, ?, ?, ?, ?, ?)""",
            (userid, username, 0, timestamp, 0, 0),
        )
        connection.commit()
        
        log.new_log(f"ID {userid}: Новый пользователь бота", "database")


def delete(id: int, deleter_userid: int) -> None:
    """Удаление пользователя из базы данных | ID цели, ID выдающего"""
    cursor.execute("DELETE FROM users WHERE id = ?", (id,))
    connection.commit()

    log.new_log(f"ID {deleter_userid}: Пользователь удалён из базы данных {id}", "database")


def data(userid: int, field_name: str):
    """Запрос любого | ID цели, Название поля | Возвращает требуемое"""
    cursor.execute(f"SELECT {field_name} FROM users WHERE userid = ?", (userid,))
    return cursor.fetchone()[0]


def balance(userid: int, money: int, operationid: int, uniqueid: int, transactionid: int) -> None:
    """Пополнение баланса | ID цели, Сумма пополнения, Идентификатор платежа системы, Уникальный идентификатор-uuid4, Транзакционный id"""
    timestamp = datetime.datetime.now().isoformat()
    cursor.execute(f'''UPDATE users SET money = money + ? WHERE userid = ?''', (money, userid))
    cursor.execute(f'''UPDATE users SET all_money = all_money + ? WHERE userid = ?''', (money, userid))
    cursor.execute(f'''INSERT INTO transactions (userid, username, amount, transactionid, reason, date) VALUES (?, ?, ?, ?, ?, ?)''', (userid, data(userid, "username"), money, transactionid, "Пополнение баланса", timestamp))
    connection.commit()

    log.new_log("{\n"+f"\tID {userid}: Баланс пополнен на {money}₽,\n\tИдентификатор платежа системы: {operationid},\n\tУникальный идентификатор-uuid4: {uniqueid},\n\tТранзакционный id: {transactionid}"+"\n}", "database")


def debalance(userid: int, money: int) -> None:
    """Списание баланса | ID цели, Сумма списания"""
    timestamp = datetime.datetime.now().isoformat()
    operation = shortuuid.uuid()
    cursor.execute(f'''UPDATE users SET spend_money = spend_money + ? WHERE userid = ?''', (money, userid))
    cursor.execute(f'''UPDATE users SET money = money - ? WHERE userid = ?''', (money, userid))
    cursor.execute(f'''INSERT INTO transactions (userid, username, amount, transactionid, reason, date) VALUES (?, ?, ?, ?, ?, ?)''', (userid, data(userid, "username"), money, operation, "Списание с баланса", timestamp))
    connection.commit()

    log.new_log("{\n"+f"\tID {userid}: Баланс списан на {money}₽,\n\tИдентификатор транзакции: {operation}"+"\n}", "database")


def profile(userid: int) -> tuple:
    """Запрос профиля | ID цели | Возвращает ID (0), Имя (1), Баланс (2), Дату регистрации (3), Всего пополнений (4), Всего затрат (5)"""
    cursor.execute("SELECT id, username, money, register_date, all_money, spend_money FROM users WHERE userid = ?", (userid,))
    data = cursor.fetchone()

    log.new_log(f"ID {userid}: Запросил свой профиль", "database")

    return data


def nickname(userid: int, nickname: str) -> None:
    """Обновление никнейма | ID цели, Новый никнейм"""
    cursor.execute("SELECT username FROM users WHERE userid = ?", (userid,))
    old_nickname = cursor.fetchone()[0] 
    
    cursor.execute(f'''UPDATE users SET username = ? WHERE userid = ?''', (nickname, userid))
    connection.commit()
    
    log.new_log(f"ID {userid}: Никнейм {old_nickname} изменён на {nickname}", "database")

