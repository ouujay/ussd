from flask import Flask
import africastalking

# ✅ Create Flask app
app = Flask(__name__)

# ✅ Initialize Africa's Talking
username = 'sandbox'
api_key = 'atsk_40303b14f9e27e8c0f08d18ea3b8327cdf8cb7f1f8c036d198ac38ee5aea7e27b0e6a746'
africastalking.initialize(username, api_key)
sms = africastalking.SMS

@app.route('/')
def home():
    return "Welcome to your SMS sender"

@app.route('/send')
def send_sms():
    recipients = ["+2349013413496"]
    message = "Hey AT Ninja!"
    sender = "25102"  # Must be this in sandbox

    try:
        response = sms.send(message, recipients, sender)
        return f"✅ SMS sent!<br>{response}"
    except Exception as e:
        return f"❌ Error: {e}"
