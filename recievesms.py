
import requests

RECEIVESMS_API_URL = "https://receive-smss.com/free-phone-number"

def get_free_number():
    """Fetches a free temporary phone number from Receive-SMS."""
    response = requests.get(RECEIVESMS_API_URL)
    if response.status_code == 200:
        data = response.json()
        return data.get("number")
    return "Failed to get phone number"

def receive_sms(number):
    """Fetches SMS messages for the temporary phone number."""
    inbox_api_url = f"https://receive-smss.com/get-messages?number={number}"
    response = requests.get(inbox_api_url)
    if response.status_code == 200:
        return response.json().get("messages", [])
    return "Failed to fetch messages"