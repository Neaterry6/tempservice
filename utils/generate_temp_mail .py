import requests

TEMP_MAIL_API = "https://api.temp-mail.org/request/new/temp-mail"

def generate_temp_email():
    """Fetch a new temporary email from the TempMail API."""
    response = requests.get(TEMP_MAIL_API)
    if response.status_code == 200:
        return response.json().get("email")
    return "Failed to generate email"