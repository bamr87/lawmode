#!/usr/bin/env python3
"""Local test file with legal compliance issues."""

import requests
import json

# GDPR violation: Collecting PII without consent
def signup_user(request):
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    
    # Storing unencrypted PII
    user_data = {
        'email': email,
        'phone': phone,
        'ip': request.META.get('REMOTE_ADDR')
    }
    
    # No encryption at rest
    db.users.insert(user_data)
    
    # Sharing with third parties without consent
    analytics.track(email, user_data)
    
    return {'status': 'success'}

# License violation: Using GPL code
def process_data(data):
    from gpl_library import process
    return process(data)

# Security issue: SQL injection risk
def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return db.execute(query)

