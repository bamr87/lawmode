"""
Test file for GDPR violation detection
This should trigger a High severity risk
"""

def fetch_user_email():
    """Fetches user email"""
    userEmail = "test@example.com"
    # Missing proper authorization
    return userEmail

def process_user_data():
    """Processes user data"""
    email = fetch_user_email()
    # Process email without proper authorization
    return email.upper()

