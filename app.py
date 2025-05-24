from flask import Flask, request, render_template, redirect, session, jsonify
from receivesms import get_free_number, receive_sms
from tempmail import get_temp_email, receive_emails
from db import register_user, verify_user

app = Flask(__name__)
app.secret_key = "supersecretkey"

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
            return redirect("/dashboard")
        else:
            return "Invalid credentials, try again!"
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    return render_template("dashboard.html", username=session["user"])

@app.route("/generate_number", methods=["GET"])
def generate_number():
    """Generate a free temp phone number from Receive-SMS."""
    if "user" not in session:
        return redirect("/login")
    temp_number = get_free_number()
    return jsonify({"phone": temp_number})

@app.route("/inbox", methods=["GET"])
def check_sms_inbox():
    """Fetch SMS messages from Receive-SMS."""
    if "user" not in session:
        return redirect("/login")
    number = request.args.get("number")
    messages = receive_sms(number)
    return render_template("inbox.html", messages=messages)

@app.route("/generate_email", methods=["GET"])
def generate_email():
    """Generate a temp email from TempMail API."""
    if "user" not in session:
        return redirect("/login")
    temp_email = get_temp_email()
    return jsonify({"email": temp_email})

@app.route("/email_inbox", methods=["GET"])
def check_email_inbox():
    """Fetch inbox messages from TempMail API."""
    if "user" not in session:
        return redirect("/login")
    email = request.args.get("email")
    messages = receive_emails(email)
    return render_template("inbox.html", messages=messages)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")