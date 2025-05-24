from flask import Flask, request, render_template, jsonify
from receivesms import get_free_number, receive_sms
from tempmail import get_temp_email, receive_emails

app = Flask(__name__)

@app.route("/")
def welcome():
    return render_template("welcome.html")

@app.route("/generate_number", methods=["GET"])
def generate_number():
    """Generate a free temp phone number from Receive-SMS."""
    temp_number = get_free_number()
    return jsonify({"phone": temp_number})

@app.route("/inbox", methods=["GET"])
def check_sms_inbox():
    """Fetch SMS messages from Receive-SMS."""
    number = request.args.get("number")
    messages = receive_sms(number)
    return render_template("inbox.html", messages=messages)

@app.route("/generate_email", methods=["GET"])
def generate_email():
    """Generate a temp email from TempMail API."""
    temp_email = get_temp_email()
    return jsonify({"email": temp_email})

@app.route("/email_inbox", methods=["GET"])
def check_email_inbox():
    """Fetch inbox messages from TempMail API."""
    email = request.args.get("email")
    messages = receive_emails(email)
    return render_template("inbox.html", messages=messages)

if __name__ == "__main__":
    app.run(debug=True)