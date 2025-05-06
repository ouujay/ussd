import sqlite3

def get_user(phone):
    conn = sqlite3.connect('sms_ai.db')
    cursor = conn.cursor()
    cursor.execute("SELECT credits FROM users WHERE phone = ?", (phone,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def create_user_if_not_exists(phone):
    conn = sqlite3.connect('sms_ai.db')
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (phone, credits) VALUES (?, ?)", (phone, 0))
    conn.commit()
    conn.close()

def deduct_credit(phone):
    conn = sqlite3.connect('sms_ai.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET credits = credits - 1 WHERE phone = ? AND credits > 0", (phone,))
    conn.commit()
    conn.close()

def add_credit(phone, amount):
    conn = sqlite3.connect('sms_ai.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET credits = credits + ? WHERE phone = ?", (amount, phone))
    conn.commit()
    conn.close()
