from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/game')
def game():
    return render_template('game.html')
# === 8. Start Flask app ===
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # ✅ Use Render-assigned port
    app.run(host='0.0.0.0', port=port)
