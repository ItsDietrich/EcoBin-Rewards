import os
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-only-change-me")

DB_CFG = dict(
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", ""),
    database=os.getenv("DB_NAME", "ecoRewards"),
)

def db():
    return mysql.connector.connect(**DB_CFG)

@app.route("/")
def dashboard():
    conn = db(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, name, points FROM users ORDER BY created_at DESC LIMIT 50")
    users = cur.fetchall()
    cur.close(); conn.close()
    return render_template("dashboard.html", users=users)

@app.route("/user/<user_id>")
def user_page(user_id):
    conn = db(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, name, points FROM users WHERE id=%s", (user_id,))
    user = cur.fetchone()
    cur.execute("SELECT id, type, amount, bottle_type, created_at FROM transactions WHERE user_id=%s ORDER BY id DESC", (user_id,))
    tx = cur.fetchall()
    cur.close(); conn.close()
    return render_template("user.html", user=user, tx=tx)

@app.route("/deduct", methods=["POST"])
def deduct():
    user_id = request.form["user_id"]
    amount = int(request.form["amount"])
    reason = request.form.get("reason", "canteen")
    conn = db(); cur = conn.cursor()
    cur.execute("UPDATE users SET points = points - %s WHERE id=%s", (amount, user_id))
    cur.execute("INSERT INTO transactions (user_id, type, amount, bottle_type) VALUES (%s,'debit',%s,%s)", (user_id, amount, reason))
    conn.commit()
    cur.close(); conn.close()
    flash(f"Deducted {amount} points from {user_id}")
    return redirect(url_for("user_page", user_id=user_id))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")