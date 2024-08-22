#     __  __           _         _              ____       _             _      _   
#    |  \/  | __ _  __| | ___   | |__  _   _   |  _ \ __ _| |_ _ __ ___ | | ___| |_ 
#    | |\/| |/ _` |/ _` |/ _ \  | '_ \| | | |  | |_) / _` | __| '__/ _ \| |/ _ \ __|
#    | |  | | (_| | (_| |  __/  | |_) | |_| |  |  __/ (_| | |_| | | (_) | |  __/ |_ 
#    |_|  |_|\__,_|\__,_|\___|  |_.__/ \__, |  |_|   \__,_|\__|_|  \___/|_|\___|\__|
#                                      |___/                                       

from database.config import connection, cursor

def create_users_table() -> None:
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS users
        (id INTEGER PRIMARY KEY AUTOINCREMENT, userid INTEGER, username TEXT NOT NULL, money INTEGER, register_date TEXT, all_money INTEGER, spend_money INTEGER)''')
    connection.commit()


def create_admins_table() -> None:
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS admins
        (id INTEGER PRIMARY KEY AUTOINCREMENT, userid INTEGER, username TEXT NOT NULL, admin_since TEXT, giver_username TEXT NOT NULL, giver_userid INTEGER)''')
    connection.commit()


def create_transactions_table() -> None:
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS transactions
        (id INTEGER PRIMARY KEY AUTOINCREMENT, userid INTEGER, username TEXT NOT NULL, amount INTEGER, transactionid TEXT, reason TEXT, date TEXT)''')
    connection.commit()


def delete_table(table_name: str) -> None:
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    connection.commit()