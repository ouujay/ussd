from flask import Flask, request, Response, render_template
import africastalking
import threading

from utils import (
    add_credit,
    create_user_if_not_exists,
    deduct_credit,
    get_user,
    get_ai_response
)

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

# Test SMS
@app.route('/send')
def send_sms():
    recipients = ["+2349013413496"]
    message = "Reply to this message!"

    try:
        response = sms.send(message, recipients)
        return f"✅ SMS sent: {response}"
    except Exception as e:
        return f"❌ Error: {e}"

# Handle incoming SMS
@app.route('/incoming-messages', methods=['POST'])
def incoming_messages():
    data = request.form.to_dict()
    phone = data.get('from')
    message = data.get('text')

    if not phone or not message:
        print("❌ Missing 'from' or 'text' in payload:", data)
        return Response(status=400)

    create_user_if_not_exists(phone)
    user_credits = get_user(phone)

    if user_credits is None or user_credits < 1:
        sms.send("You're out of credits. Please top up to continue.", [phone])
        return Response(status=200)

    ai_reply = get_ai_response(message.strip(), max_chars=300)

    try:
        sms.send(ai_reply, [phone])
        deduct_credit(phone)
    except Exception as e:
        print(f"❌ Auto-reply failed: {e}")

    return Response(status=200)

# Delivery report handler
@app.route('/delivery-reports', methods=['POST'])
def delivery_reports():
    data = request.form.to_dict()
    print(f"📦 Delivery report...\n{data}")
    return Response(status=200)

# Manual top-up test page
@app.route('/topup', methods=['GET', 'POST'])
def topup():
    if request.method == 'POST':
        phone = request.form.get('phone')
        amount = request.form.get('amount')

        try:
            amount = int(amount)
            create_user_if_not_exists(phone)
            add_credit(phone, amount)
            return f"✅ {amount} credits added to {phone}"
        except Exception as e:
            return f"❌ Error: {e}"

    return render_template("topup.html")

# Automatically send message when server starts
def auto_send_sms():
    try:
        response = sms.send("Hello, AT Ninja!", ["+2349013413496"])
        print(f"📨 Auto-sent SMS: {response}")
    except Exception as e:
        print(f"❌ Auto-sending failed: {e}")

# USSD Menu
@app.route('/ussd', methods=['POST'])
def ussd():
    session_id = request.values.get('sessionId')
    phone_number = request.values.get('phoneNumber')
    text = request.values.get('text', '')

    user_input = text.strip().split('*') if text else []
    response = ""

    if len(user_input) == 0:
        response = "CON Welcome to SmartBot\n1. Check Credit\n2. Top Up"
    elif user_input[0] == '1':
        credits = get_user(phone_number)
        response = f"END You have {credits or 0} credit(s) left."
    elif user_input[0] == '2':
        if len(user_input) == 1:
            response = "CON Enter amount to top up:"
        elif len(user_input) == 2:
            try:
                amount = int(user_input[1])
                create_user_if_not_exists(phone_number)
                add_credit(phone_number, amount)
                response = f"END {amount} credit(s) added successfully!"
            except:
                response = "END Invalid amount. Please try again."
        else:
            response = "END Invalid input. Start again."
    else:
        response = "END Invalid option. Try again."

    return Response(response, mimetype="text/plain")

# Start app
if __name__ == '__main__':
    threading.Timer(2.0, auto_send_sms).start()
    app.run(debug=True)
