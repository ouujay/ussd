from flask import Flask, request, Response
import africastalking

app = Flask(__name__)

# TODO: Initialize SDK
username = 'sandbox'
api_key = 'atsk_40303b14f9e27e8c0f08d18ea3b8327cdf8cb7f1f8c036d198ac38ee5aea7e27b0e6a746'
africastalking.initialize(username, api_key)
sms = africastalking.SMS

# TODO: Send SMS route (optional)
@app.route('/send')
def send_sms():
    recipients = ["+2349013413496"]
    message = "Reply to this message!"
    sender = "25102"  # 🔥 Use your actual shortcode here

    try:
        response = sms.send(message, recipients, sender)
        return f"✅ SMS sent: {response}"
    except Exception as e:
        return f"❌ Error: {e}"

# TODO: Incoming messages route
@app.route('/incoming-messages', methods=['POST'])
def incoming_messages():
    data = request.get_json(force=True)
    print(f"📩 Incoming message...\n{data}")
    return Response(status=200)

# ✅ Home route (optional)
@app.route('/')
def home():
    return "SMS send + receive service running."

