from flask import Flask, request, Response
import africastalking
import threading
import os

app = Flask(__name__)

# === 1. Initialize Africa's Talking with LIVE credentials ===
username = 'sandbox'
api_key = 'atsk_40303b14f9e27e8c0f08d18ea3b8327cdf8cb7f1f8c036d198ac38ee5aea7e27b0e6a746'

africastalking.initialize(username, api_key)
sms = africastalking.SMS

# === 2. Define shortcode to use for sending messages ===
SHORTCODE = "44905"  # ✅ Your live shortcode

# === 3. Auto-send SMS when server starts ===
def auto_send_sms():
    try:
        response = sms.send("👋 Welcome to our SMS service!", ["+2349013413496"], sender=SHORTCODE)
        print(f"📨 Auto-sent SMS: {response}")
    except Exception as e:
        print(f"❌ Auto-sending failed: {e}")

# === 4. Send SMS manually via route ===
@app.route('/send')
def send_sms():
    recipients = ["+2349013413496"]
    message = "📣 Test: This is a live message from our service."
    try:
        response = sms.send(message, recipients, sender=SHORTCODE)
        return f"✅ SMS sent: {response}"
    except Exception as e:
        return f"❌ Error: {e}"

# === 5. Handle incoming SMS (automated reply logic) ===
@app.route('/incoming-messages', methods=['POST'])
def incoming_messages():
    data = request.form.to_dict()
    print(f"📩 Incoming message...\n{data}")

    sender_number = data.get('from')
    user_message = data.get('text', '').strip().lower()
    shortcode = data.get('to')

    # Auto-reply logic
    if user_message == "hi":
        reply = "👋 Hello there! Type HELP to see what I can do."
    elif user_message == "help":
        reply = "🧠 Options: RECHARGE, BALANCE, STOP."
    elif user_message == "recharge":
        reply = "⚡ Recharge code: 1234-5678. Done!"
    elif user_message == "balance":
        reply = "💰 Your current balance is ₦250.00"
    elif user_message == "stop":
        reply = "❌ You’ve been unsubscribed. Text START to rejoin."
    elif user_message == "start":
        reply = "✅ You're now subscribed again. Welcome back!"
    else:
        reply = "❓ Unknown command. Try typing: HI or HELP."

    # Send reply using AT
    try:
        response = sms.send(reply, [sender_number], sender=SHORTCODE)
        print(f"🤖 Auto-reply sent: {response}")
    except Exception as e:
        print(f"❌ Auto-reply failed: {e}")

    return Response(status=200)

# === 6. Handle delivery reports ===
@app.route('/delivery-reports', methods=['POST'])
def delivery_reports():
    data = request.form.to_dict()
    print(f"📦 Delivery report received:\n{data}")
    return Response(status=200)

# === 7. Default home page ===
@app.route('/')
def home():
    return "📱 SMS system running with shortcode 44905 (Live Mode)."

# === 8. Start Flask app with port binding for deployment ===
if __name__ == '__main__':
    # Auto-send a welcome SMS after 2 seconds when the server starts
    threading.Timer(2.0, auto_send_sms).start()
    
    port = int(os.environ.get("PORT", 10000))  # Render/Heroku uses dynamic ports
    app.run(host='0.0.0.0', port=port, debug=True)
