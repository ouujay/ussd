from flask import Flask, request, Response
import africastalking
import threading
import os

app = Flask(__name__)

# === 1. Initialize SDK with Sandbox credentials ===
username = 'sandbox'
api_key = 'atsk_40303b14f9e27e8c0f08d18ea3b8327cdf8cb7f1f8c036d198ac38ee5aea7e27b0e6a746'
africastalking.initialize(username, api_key)
sms = africastalking.SMS

# === 2. Set your sandbox shortcode ===
SANDBOX_SHORTCODE = "25102"  # Replace with your actual sandbox shortcode (e.g., "44905" if it's set)

# === 3. Automatically send test SMS on server start ===
def auto_send_sms():
    try:
        response = sms.send("👋 Hello, AT Ninja! This is a test from Flask.", ["+2349013413496"], SANDBOX_SHORTCODE)
        print(f"📨 Auto-sent SMS: {response}")
    except Exception as e:
        print(f"❌ Auto-sending failed: {e}")

# === 4. Manual send route for testing ===
@app.route('/send')
def send_sms():
    try:
        response = sms.send("📣 This is a manual test message!", ["+2349013413496"], SANDBOX_SHORTCODE)
        return f"✅ Message sent: {response}"
    except Exception as e:
        return f"❌ Sending failed: {e}"

# === 5. Handle incoming SMS messages and auto-reply ===
@app.route('/incoming-messages', methods=['POST'])
def incoming_messages():
    data = request.get_json(force=True)
    print(f"📩 Incoming message:\n{data}")

    sender_number = data.get("from")
    user_message = data.get("text", "").strip().lower()
    shortcode = data.get("to") or SANDBOX_SHORTCODE

    if user_message == "hi":
        reply = "👋 Hello! Type HELP to see what I can do."
    elif user_message == "help":
        reply = "🧠 Available commands: RECHARGE, BALANCE, STOP."
    elif user_message == "recharge":
        reply = "🔋 Recharge code: 1234-5678."
    elif user_message == "balance":
        reply = "💰 Your balance is ₦500.00"
    elif user_message == "stop":
        reply = "🚫 You’ve been unsubscribed."
    elif user_message == "start":
        reply = "✅ Welcome back! You're subscribed again."
    else:
        reply = "❓ Unknown command. Try typing: hi or help."

    try:
        response = sms.send(reply, [sender_number], shortcode)
        print(f"🤖 Auto-reply sent: {response}")
    except Exception as e:
        print(f"❌ Auto-reply failed: {e}")

    return Response(status=200)

# === 6. Handle delivery report logs ===
@app.route('/delivery-reports', methods=['POST'])
def delivery_reports():
    data = request.get_json(force=True)
    print(f"📦 Delivery report received:\n{data}")
    return Response(status=200)

# === 7. Root route ===
@app.route('/')
def home():
    return "🚀 Africa's Talking Flask SMS Bot is running in sandbox mode."

# === 8. Start Flask app ===
if __name__ == '__main__':
    threading.Timer(2.0, auto_send_sms).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
