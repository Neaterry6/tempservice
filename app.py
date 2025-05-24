from flask import Flask, request, render_template, jsonify
from utils.tempmail import generate_temp_email
from utils.tempnumber import generate_temp_number

app = Flask(__name__)

# Store temp emails & phone numbers along with messages
temp_data = {}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        temp_email = generate_temp_email()
        temp_phone = generate_temp_number()
        temp_data["email"] = temp_email
        temp_data["phone"] = temp_phone
        temp_data["messages"] = []

        return render_template("index.html", email=temp_email, phone=temp_phone)

    return render_template("index.html")

@app.route("/inbox", methods=["GET"])
def check_inbox():
    return render_template("inbox.html", messages=temp_data.get("messages", []))

@app.route("/send", methods=["POST"])
def send_message():
    message = request.form.get("message")
    if message:
        temp_data["messages"].append(message)
        return jsonify({"status": "Message sent!"})
    return jsonify({"error": "No message provided!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
