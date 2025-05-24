import requests

TEMPMAIL_API_URL = "https://api.temp-mail.org/request/new/temp-mail"

def get_temp_email():
    """Fetches a temporary email from TempMail API."""
    response = requests.get(TEMPMAIL_API_URL)
    if response.status_code == 200:
        data = response.json()
        return data.get("email")
    return "Failed to get email"

def receive_emails(email):
    """Fetch inbox messages for the temp email."""
    inbox_api_url = f"https://api.temp-mail.org/request/mail?email={email}"
    response = requests.get(inbox_api_url)
    if response.status_code == 200:
        return response.json().get("messages", [])
    return "Failed to fetch messages"