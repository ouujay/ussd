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

# User profile model (registration)
class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    stage = db.Column(db.String(20), default="name")  # name, age, gender, done

@app.route('/', methods=['POST', 'GET'])
def ussd_callback():
    session_id = request.values.get("sessionId")
    service_code = request.values.get("serviceCode")
    phone_number = request.values.get("phoneNumber")
    text = request.values.get("text", "")

    # ✅ Prevent errors if phone_number is missing (e.g. browser visit)
    if not phone_number:
        return "This endpoint only handles USSD POST requests from Africa's Talking.", 400

    # ✅ Check or create user account
    account = UserAccount.query.filter_by(phone_number=phone_number).first()
    if not account:
        suffix = phone_number[-4:] if len(phone_number) >= 4 else "0000"
        account = UserAccount(
            phone_number=phone_number,
            account_number="ACC" + suffix,
            balance="KES 10,000"
        )
        db.session.add(account)
        db.session.commit()

    # ✅ Save or update session in DB
    session = Session.query.filter_by(session_id=session_id).first()
    if not session:
        session = Session(session_id=session_id, phone_number=phone_number, text=text)
        db.session.add(session)
    else:
        session.text = text
    db.session.commit()

    # ✅ Check or create user profile
    profile = UserProfile.query.filter_by(phone_number=phone_number).first()
    if not profile:
        profile = UserProfile(phone_number=phone_number)
        db.session.add(profile)
        db.session.commit()

    # ✅ REGISTRATION FLOW
    if profile.stage == "name":
        if text == "":
            return "CON Welcome! Please enter your name:"
        else:
            profile.name = text
            profile.stage = "age"
            db.session.commit()
            return f"CON Great, {text}! Now enter your age:"

    elif profile.stage == "age":
        if text.isdigit():
            profile.age = int(text)
            profile.stage = "gender"
            db.session.commit()
            return "CON Select your gender:\n1. Male\n2. Female"
        else:
            return "CON Please enter a valid age:"

    elif profile.stage == "gender":
        if text == "1":
            profile.gender = "Male"
            profile.stage = "done"
            db.session.commit()
            return "END Registration complete. Thank you!"
        elif text == "2":
            profile.gender = "Female"
            profile.stage = "done"
            db.session.commit()
            return "END Registration complete. Thank you!"
        else:
            return "CON Invalid choice. Select gender:\n1. Male\n2. Female"

    # ✅ USSD MENU (only if registration is done)
    if profile.stage == "done":
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

    # fallback
    return "END Something went wrong."

# ✅ Admin dashboard to view registered users
@app.route('/dashboard')
def dashboard():
    profiles = UserProfile.query.all()

    html = """
    <html>
    <head>
        <title>USSD Users Dashboard</title>
        <style>
            table { width: 80%%; border-collapse: collapse; margin: 20px auto; font-family: sans-serif; }
            th, td { padding: 10px; border: 1px solid #ddd; text-align: center; }
            th { background-color: #f2f2f2; }
            h2 { text-align: center; font-family: sans-serif; }
        </style>
    </head>
    <body>
        <h2>Registered Users</h2>
        <table>
            <tr>
                <th>ID</th>
                <th>Phone Number</th>
                <th>Name</th>
                <th>Age</th>
                <th>Gender</th>
                <th>Stage</th>
            </tr>
    """

    for p in profiles:
        html += f"""
            <tr>
                <td>{p.id}</td>
                <td>{p.phone_number}</td>
                <td>{p.name or '-'}</td>
                <td>{p.age or '-'}</td>
                <td>{p.gender or '-'}</td>
                <td>{p.stage}</td>
            </tr>
        """

    html += "</table></body></html>"
    return html

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
