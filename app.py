from flask import Flask, request, render_template, redirect
from twilio.rest import Client
import sqlite3

app = Flask(__name__)

# ⚠️ À configurer dans config.py
from config import TWILIO_SID, TWILIO_TOKEN, TWILIO_PHONE

client = Client(TWILIO_SID, TWILIO_TOKEN)

@app.route("/", methods=["GET", "POST"])
def dashboard():
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()

    if request.method == "POST":
        to = request.form["number"]
        msg = request.form["message"]
        client.messages.create(body=msg, from_=TWILIO_PHONE, to=to)
        c.execute("INSERT INTO messages (sender, content, direction) VALUES (?, ?, ?)", (to, msg, "out"))
        conn.commit()

    c.execute("SELECT * FROM messages ORDER BY id DESC")
    messages = c.fetchall()
    conn.close()
    return render_template("dashboard.html", messages=messages)

@app.route("/receive", methods=["POST"])
def receive():
    sender = request.form.get("From")
    content = request.form.get("Body")
    conn = sqlite3.connect('db.sqlite')
    conn.execute("INSERT INTO messages (sender, content, direction) VALUES (?, ?, ?)", (sender, content, "in"))
    conn.commit()
    conn.close()
    return "OK", 200

if __name__ == "__main__":
    app.run(debug=True)
