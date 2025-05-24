from flask import Flask, request, render_template, redirect, session, jsonify
import random
import string
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
    conn.commit()
    conn.close()

def register_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

def verify_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return bool(user)

init_db()

# Store temp emails, phone numbers, and messages
temp_data = {}

def generate_temp_email():
    domains = ["tempmail.com", "guerrillamail.com", "mailinator.com"]
    username = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    return f"{username}@{random.choice(domains)}"

def generate_temp_number(country):
    country_codes = {
        "Nigeria": "+234",
        "USA": "+1",
        "UK": "+44",
        "Canada": "+1",
        "India": "+91"
    }
    if country in country_codes:
        return f"{country_codes[country]}{random.randint(1000000000, 9999999999)}"
    return "Invalid country selected!"

@app.route("/")
def welcome():
    return render_template("welcome.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        register_user(username, password)
        return redirect("/login")
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if verify_user(username, password):
            session["user"] = username
            return redirect("/generator")
        else:
            return "Invalid credentials, try again!"
    return render_template("login.html")

@app.route("/generator", methods=["GET", "POST"])
def generator():
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        country = request.form.get("country")
        temp_email = generate_temp_email()
        temp_phone = generate_temp_number(country)

        temp_data["email"] = temp_email
        temp_data["phone"] = temp_phone
        temp_data["messages"] = []

        return render_template("index.html", email=temp_email, phone=temp_phone)
    
    return render_template("index.html")

@app.route("/inbox", methods=["GET"])
def check_inbox():
    if "user" not in session:
        return redirect("/login")

    return render_template("inbox.html", messages=temp_data.get("messages", []))

@app.route("/send", methods=["POST"])
def send_message():
    if "user" not in session:
        return redirect("/login")

    message = request.form.get("message")
    if message:
        temp_data["messages"].append(message)
        return jsonify({"status": "Message sent!"})
    return jsonify({"error": "No message provided!"})

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)