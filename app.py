from flask import Flask, request, Response
import africastalking
import threading
import os

app = Flask(__name__)

# === 1. Initialize SDK with Sandbox credentials ===
username = 'sandbox'
api_key = 'atsk_12d2b3f0b1f2bd1e0e5a16ee7241b5e6a88721f6656a0aec30df01d1d556d864cedf7703'
africastalking.initialize(username, api_key)
sms = africastalking.SMS

# === 2. Set your sandbox shortcode ===
SANDBOX_SHORTCODE = "54342"  # Use your actual sandbox shortcode from AT

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
    try:
        data = request.form.to_dict()
        print("🔥 WE GOT A MESSAGE!")
        print(data)
    except Exception as e:
        print(f"❌ ERROR in incoming-messages: {e}")
    return Response(status=200)

# === 6. Handle delivery report logs ===
@app.route('/delivery-reports', methods=['POST'])
def delivery_reports():
    data = request.form.to_dict()
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
