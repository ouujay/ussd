from flask import Flask, request, Response, render_template
import africastalking
import threading

from utils import create_user_if_not_exists, deduct_credit, get_user,get_ai_response


app = Flask(__name__)

# Initialize Africa's Talking SDK
username = 'sandbox'
api_key = 'atsk_40303b14f9e27e8c0f08d18ea3b8327cdf8cb7f1f8c036d198ac38ee5aea7e27b0e6a746'
africastalking.initialize(username, api_key)
sms = africastalking.SMS

# Homepage
@app.route('/')
def home():
    return render_template("index.html")

# Send test SMS
@app.route('/send')
def send_sms():
    recipients = ["+2349013413496"]
    message = "Reply to this message!"
    sender = "25102"

    try:
        response = sms.send(message, recipients, sender)
        return f"✅ SMS sent: {response}"
    except Exception as e:
        return f"❌ Error: {e}"

# Receive SMS and auto-reply
@app.route('/incoming-messages', methods=['POST'])
def incoming_messages():
    data = request.get_json(force=True)
    phone = data.get('from')
    message = data.get('text')

    create_user_if_not_exists(phone)
    user_credits = get_user(phone)

    if user_credits is None or user_credits < 1:
        sms.send("You're out of credits. Please top up to continue.", [phone])
        return Response(status=200)

    # Get AI reply with trimming
    ai_reply = get_ai_response(message, max_chars=300)

    try:
        sms.send(ai_reply, [phone])
        deduct_credit(phone)
    except Exception as e:
        print(f"Auto-reply failed: {e}")

    return Response(status=200)

# Delivery reports route
@app.route('/delivery-reports', methods=['POST'])
def delivery_reports():
    data = request.form.to_dict()
    print(f"📦 Delivery report...\n{data}")
    return Response(status=200)

# Auto send message on server start
def auto_send_sms():
    try:
        response = sms.send(
            'Hello, AT Ninja!',
            ['+2349013413496'],
            sender='25102'
        )
        print(f"📨 Auto-sent SMS: {response}")
    except Exception as e:
        print(f"Auto-sending failed: {e}")

if __name__ == '__main__':
    threading.Timer(2.0, auto_send_sms).start()
    app.run(debug=True)
