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
from together import Together
import re

# Initialize Together AI client
client = Together(api_key="your_together_api_key")

# Smart trimming by sentence
def trim_smart(text, max_chars=300):
    sentences = re.split(r'(?<=[.!?]) +', text)
    result = ''
    for sentence in sentences:
        if len(result) + len(sentence) <= max_chars:
            result += sentence + ' '
        else:
            break
    return result.strip()

# Main AI function
def get_ai_response(prompt, max_chars=300):
    try:
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            messages=[
                {
                    "role": "system",
                    "content": "Always respond like you're sending a short SMS. Keep replies under 300 characters. Be helpful, clear, and concise."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        full_response = response.choices[0].message.content.strip()
        return trim_smart(full_response, max_chars)
    except Exception as e:
        return "AI failed to respond. Try again later."
