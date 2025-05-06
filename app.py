from flask import Flask
import africastalking

# Initialize Flask app
app = Flask(__name__)

# Initialize Africa's Talking SDK
username = 'sandbox'
api_key = 'atsk_40303b14f9e27e8c0f08d18ea3b8327cdf8cb7f1f8c036d198ac38ee5aea7e27b0e6a746'
africastalking.initialize(username, api_key)
sms = africastalking.SMS


@app.route('/')
def home():
    return "Welcome to the Africa's Talking SMS sender!"


@app.route('/send')
def send_sms():
    recipients = ["+2349013413496"]  # Replace with your own phone number
    message = "Hey AT Ninja!"
    sender = "AFRICASTKNG"  # Use this for sandbox

    try:
        response = sms.send(message, recipients, sender)
        return f"✅ Message sent successfully: {response}"
    except Exception as e:
        return f"❌ Houston, we have a problem: {e}"


# For local testing (optional)
if __name__ == "__main__":
    app.run(debug=True)
