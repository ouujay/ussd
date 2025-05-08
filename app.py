from flask import Flask, request, Response
import africastalking
import threading
import os

app = Flask(__name__)

# === 1. Sandbox credentials ===
username = 'sandbox'
api_key = 'atsk_40303b14f9e27e8c0f08d18ea3b8327cdf8cb7f1f8c036d198ac38ee5aea7e27b0e6a746'
africastalking.initialize(username, api_key)
sms = africastalking.SMS

# === 2. Auto-send test message (no shortcode needed here) ===
def auto_send_sms():
    try:
        response = sms.send("👋 Welcome to the SMS bot!", ["+2349013413496"])
        print(f"📨 Auto-sent SMS: {response}")
    except Exception as e:
        print(f"❌ Auto-sending failed: {e}")

# === 3. Manual send test ===
@app.route('/send')
def send_sms():
    try:
        response = sms.send("🚀 This is a test SMS from /send route!", ["+2349013413496"])
        return f"✅ SMS sent: {response}"
    except Exception as e:
        return f"❌ Error sending SMS: {e}"

# === 4. Incoming message handler ===
@app.route('/incoming-messages', methods=['POST'])
def incoming_messages():
    data = request.form.to_dict()
    print(f"📩 Incoming message: {data}")

    sender_number = data.get('from')
    user_message = data.get('text', '').strip().lower()
    shortcode = data.get('to')  # ✅ Africa's Talking passes the shortcode here

    # Response logic
    if user_message == "hi":
        reply = "👋 Hello there! Type HELP to see options."
    elif user_message == "help":
        reply = "🧠 Available: RECHARGE, BALANCE, STOP."
    elif user_message == "recharge":
        reply = "🔋 Recharge successful. Code: 1234."
    elif user_message == "balance":
        reply = "💰 Your balance is ₦500."
    elif user_message == "stop":
        reply = "🚫 You've been unsubscribed."
    elif user_message == "start":
        reply = "✅ Welcome back!"
    else:
        reply = "❓ Unknown command. Try 'hi' or 'help'."

    # ✅ This is where we use the shortcode properly (as the sender for replies)
    try:
        response = sms.send(reply, [sender_number], sender=shortcode)  # ✅ Correct use
        print(f"🤖 Auto-reply sent: {response}")
    except Exception as e:
        print(f"❌ Auto-reply failed: {e}")

    return Response(status=200)

# === 5. Delivery reports ===
@app.route('/delivery-reports', methods=['POST'])
def delivery_reports():
    data = request.form.to_dict()
    print(f"📦 Delivery report received: {data}")
    return Response(status=200)

# === 6. Default route ===
@app.route('/')
def home():
    return "📱 Africa's Talking SMS Bot (Sandbox) is running."

# === 7. Start Flask app ===
if __name__ == '__main__':
    threading.Timer(2.0, auto_send_sms).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
