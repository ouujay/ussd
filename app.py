from flask import Flask, request, Response
import africastalking
import threading

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
    sender = "25102"  # Your actual shortcode

    try:
        response = sms.send(message, recipients, sender)
        return f"✅ SMS sent: {response}"
    except Exception as e:
        return f"❌ Error: {e}"
@app.route('/incoming-messages', methods=['POST'])
def incoming_messages():
    data = request.form.to_dict()
    print(f"📩 Incoming message...\n{data}")

    sender_number = data.get('from')
    user_message = data.get('text', '').strip().lower()
    shortcode = data.get('to')

    # Logic for auto-response
    if user_message == "hi":
        reply = "Hello! 👋 This is an auto-response from our bot."
    elif user_message == "help":
        reply = "Need help? Reply with: MENU to see options."
    else:
        reply = "I didn’t understand that. Try typing: hi or help."

    # ✅ CORRECT usage of Africa's Talking SDK
    try:
        response = sms.send(reply, [sender_number], shortcode)
        print(f"🤖 Auto-reply sent: {response}")
    except Exception as e:
        print(f"❌ Auto-reply failed: {e}")

    return Response(status=200)

# TODO: Delivery reports route
@app.route('/delivery-reports', methods=['POST'])
def delivery_reports():
    data = request.form.to_dict()
    print(f"📦 Delivery report...\n{data}")
    return Response(status=200)

# ✅ Home route
@app.route('/')
def home():
    return "SMS system running (Send, Receive, Delivery Reports)."

# TODO: Call sendSMS after server starts
def auto_send_sms():
    try:
        response = sms.send(
            'Hello, AT Ninja!',
            ['+2349013413496'],
            sender='25102'
        )
        print(f"📨 Auto-sent SMS: {response}")
    except Exception as e:
        print(f"❌ Auto-sending failed: {e}")

if __name__ == '__main__':
    # Trigger SMS after a delay to allow Flask to start fully
    threading.Timer(2.0, auto_send_sms).start()
    app.run(debug=True)
