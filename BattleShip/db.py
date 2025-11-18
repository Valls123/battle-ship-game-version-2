import sqlite3
from datetime import datetime

DB_NAME = "battleship.db"


def init_db():
    """Создание таблицы, если её ещё нет."""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            outcome TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


def add_result(outcome: str):
    """Добавить результат игры (win / lose)."""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO results (outcome, date) VALUES (?, ?)",
        (outcome, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )

    conn.commit()
    conn.close()


def get_stats():
    """Возвращает количество побед и поражений."""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM results WHERE outcome = 'win'")
    wins = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM results WHERE outcome = 'lose'")
    losses = cur.fetchone()[0]

    conn.close()
    return wins, losses
