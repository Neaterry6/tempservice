from flask import Flask, request, render_template, jsonify
import random
import string
from utils.generate_temp_number import generate_temp_number

app = Flask(__name__)

temp_data = {}

def generate_temp_email():
    """Generate a temporary email address."""
    domains = ["tempmail.com", "guerrillamail.com", "mailinator.com"]
    username = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    return f"{username}@{random.choice(domains)}"

@app.route("/", methods=["GET", "POST"])
def index():
    """Homepage for generating temp emails and numbers."""
    if request.method == "POST":
        country = request.form.get("country")  # User selects country
        temp_email = generate_temp_email()
        temp_phone = generate_temp_number(country)

        temp_data["email"] = temp_email
        temp_data["phone"] = temp_phone
        temp_data["messages"] = []

        return render_template("index.html", email=temp_email, phone=temp_phone)

    return render_template("index.html")

@app.route("/inbox", methods=["GET"])
def check_inbox():
    """Inbox page to check received messages."""
    return render_template("inbox.html", messages=temp_data.get("messages", []))

@app.route("/send", methods=["POST"])
def send_message():
    """Allows users to send messages."""
    message = request.form.get("message")
    if message:
        temp_data["messages"].append(message)
        return jsonify({"status": "Message sent!"})
    return jsonify({"error": "No message provided!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
