from flask import Flask, request, Response
import africastalking
import threading
import os

app = Flask(__name__)

# === 1. Africa's Talking Sandbox Credentials ===
username = 'sandbox'
api_key = 'atsk_40303b14f9e27e8c0f08d18ea3b8327cdf8cb7f1f8c036d198ac38ee5aea7e27b0e6a746'
africastalking.initialize(username, api_key)
sms = africastalking.SMS

# === 2. Set your sandbox shortcode ===
SANDBOX_SHORTCODE = "44905"  # Replace this with your actual sandbox shortcode (e.g. "" if allowed)

# === 3. Function to auto-send SMS after server starts ===
def auto_send_sms():
    try:
        response = sms.send("👋 Hello, AT Ninja!", ["+2349013413496"], sender=SANDBOX_SHORTCODE)
        print(f"📨 Auto-sent SMS: {response}")
    except Exception as e:
        print(f"❌ Auto-send error: {e}")

# === 4. Manual /send route to test delivery ===
@app.route('/send')
def send_sms():
    try:
        response = sms.send("📣 This is a manual test message!", ["+2349013413496"], sender=SANDBOX_SHORTCODE)
        return f"✅ Message sent: {response}"
    except Exception as e:
        return f"❌ Sending failed: {e}"

# === 5. Route for Incoming Messages ===
@app.route('/incoming-messages', methods=['POST'])
def incoming_messages():
    data = request.get_json(force=True)
    print(f"📩 Incoming message...\n{data}")

    sender_number = data.get("from")
    message_text = data.get("text", "").strip().lower()
    shortcode = data.get("to") or SANDBOX_SHORTCODE

    if message_text == "hi":
        reply = "👋 Hello there! Type HELP to see what I can do."
    elif message_text == "help":
        reply = "📋 MENU: RECHARGE, BALANCE, STOP."
    elif message_text == "recharge":
        reply = "🔋 Recharge code: 1234-5678. You're welcome!"
    elif message_text == "balance":
        reply = "💰 Your balance is ₦500.00"
    elif message_text == "stop":
        reply = "🚫 You've been unsubscribed."
    elif message_text == "start":
        reply = "✅ You've been re-subscribed. Welcome back!"
    else:
        reply = "❓ Unknown command. Try HI or HELP."

    try:
        response = sms.send(reply, [sender_number], sender=shortcode)
        print(f"🤖 Auto-reply sent: {response}")
    except Exception as e:
        print(f"❌ Auto-reply failed: {e}")

    return Response(status=200)

# === 6. Route for Delivery Reports ===
@app.route('/delivery-reports', methods=['POST'])
def delivery_reports():
    data = request.get_json(force=True)
    print(f"📦 Delivery report received:\n{data}")
    return Response(status=200)

# === 7. Root Route ===
@app.route('/')
def home():
    return "✅ Africa's Talking Flask App (Sandbox) Running with Shortcode."

# === 8. Start Server and Auto-Send Test SMS ===
if __name__ == '__main__':
    threading.Timer(2.0, auto_send_sms).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
