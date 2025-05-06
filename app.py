from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# SQLite config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ussd_sessions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# DB init
db = SQLAlchemy(app)

# Session model
class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    text = db.Column(db.String(300), nullable=True)

# User account model
class UserAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    account_number = db.Column(db.String(20), nullable=False)
    balance = db.Column(db.String(20), nullable=False)

@app.route('/', methods=['POST', 'GET'])
def ussd_callback():
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "")

    # Check if user already has an account
    account = UserAccount.query.filter_by(phone_number=phone_number).first()

    # If not, create one with default data
    if not account:
        account = UserAccount(
            phone_number=phone_number,
            account_number="ACC" + phone_number[-4:],  # e.g. ACC1234
            balance="KES 10,000"
        )
        db.session.add(account)
        db.session.commit()

    # Save or update session in DB
    session = Session.query.filter_by(session_id=session_id).first()
    if not session:
        session = Session(session_id=session_id, phone_number=phone_number, text=text)
        db.session.add(session)
    else:
        session.text = text
    db.session.commit()

    # USSD Logic
    if text == "":
        response = "CON What would you want to check \n"
        response += "1. My Account \n"
        response += "2. My phone number"
    elif text == "1":
        response = "CON Choose account information you want to view \n"
        response += "1. Account number \n"
        response += "2. Account balance"
    elif text == "1*1":
        response = "END Your account number is " + account.account_number
    elif text == "1*2":
        response = "END Your balance is " + account.balance
    elif text == "2":
        response = "END This is your phone number " + phone_number
    else:
        response = "END Invalid input. Try again."

    return response

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
