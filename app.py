from flask import Flask, request, render_template, redirect, session
import random
import string
from db import register_user, verify_user

app = Flask(__name__)
app.secret_key = "supersecretkey"

def generate_temp_email():
    domains = ["tempmail.com", "guerrillamail.com", "mailinator.com"]
    username = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    return f"{username}@{random.choice(domains)}"

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
        temp_email = generate_temp_email()
        return render_template("index.html", email=temp_email)
    
    return render_template("index.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)