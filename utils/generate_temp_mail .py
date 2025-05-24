import random
import string

def generate_temp_email():
    """Generate a temporary email address."""
    domains = ["tempmail.com", "guerrillamail.com", "mailinator.com"]
    username = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    return f"{username}@{random.choice(domains)}"