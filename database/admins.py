#     __  __           _         _              ____       _             _      _   
#    |  \/  | __ _  __| | ___   | |__  _   _   |  _ \ __ _| |_ _ __ ___ | | ___| |_ 
#    | |\/| |/ _` |/ _` |/ _ \  | '_ \| | | |  | |_) / _` | __| '__/ _ \| |/ _ \ __|
#    | |  | | (_| | (_| |  __/  | |_) | |_| |  |  __/ (_| | |_| | | (_) | |  __/ |_ 
#    |_|  |_|\__,_|\__,_|\___|  |_.__/ \__, |  |_|   \__,_|\__|_|  \___/|_|\___|\__|
#                                      |___/                                       

from database.config import connection, cursor
from utils import log
import datetime

def new(username: str, userid: int, giver_username: str, giver_userid: int) -> None:
    """Добавление нового админа в базу данных | Никнейм цели, ID цели, Никнейм выдающего, ID выдающего"""
    timestamp = datetime.datetime.now().isoformat()
    cursor.execute(
        """INSERT INTO admins (userid, username, admin_since, giver_username, giver_userid) VALUES (?, ?, ?, ?, ?)""",
        (userid, username, timestamp, giver_username, giver_userid),
    )
    connection.commit()

    log.new_log(f"ID {giver_userid}: Новый админ добавлен в базу данных {userid}", "database")


def delete(userid: int, deleter_userid: int) -> None:
    """Удаление админа из базы данных | ID цели, ID выдающего"""
    cursor.execute("DELETE FROM admins WHERE userid = ?", (userid,))
    connection.commit()

    log.new_log(f"ID {deleter_userid}: Админ удалён из базы данных {userid}", "database")


def all() -> list:
    cursor.execute("SELECT * FROM admins")
    return cursor.fetchall()

def data(userid: int, field_name: str):
    """Запрос любого | ID цели, Название поля | Возвращает требуемое"""
    cursor.execute(f"SELECT {field_name} FROM users WHERE userid = ?", (userid,))
    return cursor.fetchone()[0]
