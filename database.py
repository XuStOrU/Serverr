# database.py
import sqlite3

db = sqlite3.connect("fishing_bot.db")
sql = db.cursor()

# Таблица пользователей
sql.execute("""CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY,
    money INTEGER DEFAULT 0,
    xp INTEGER DEFAULT 0,
    level INTEGER DEFAULT 1,
    rod TEXT DEFAULT 'Старая удочка',
    bait TEXT DEFAULT 'Червь',
    location TEXT DEFAULT 'Местечко',
    last_fish INTEGER DEFAULT 0,
    total_caught INTEGER DEFAULT 0,
    max_weight REAL DEFAULT 0
)""")
db.commit()

def get_user(user_id):
    sql.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user = sql.fetchone()
    if not user:
        sql.execute("INSERT INTO users(user_id) VALUES(?)", (user_id,))
        db.commit()
        sql.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        user = sql.fetchone()
    return user

def update_user(user_id, **kwargs):
    for key, value in kwargs.items():
        sql.execute(f"UPDATE users SET {key}=? WHERE user_id=?", (value, user_id))
    db.commit()