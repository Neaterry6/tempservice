import random

# Country code mapping
COUNTRY_CODES = {
    "Nigeria": "+234",
    "USA": "+1",
    "UK": "+44",
    "Canada": "+1",
    "India": "+91"
}

def generate_temp_number(country):
    """Generate a temporary phone number based on the selected country."""
    if country in COUNTRY_CODES:
        return f"{COUNTRY_CODES[country]}{random.randint(1000000000, 9999999999)}"
    return "Invalid country selected!"