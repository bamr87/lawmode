#!/usr/bin/env python3
"""Test xAI Grok with code that should trigger legal risks."""

import os
import sys
from lawmode import LawModeAgent
from lawmode.config import LawModeConfig

# Code with multiple legal issues
test_code = """
import requests
import json

# GDPR violation: Collecting PII without consent
def signup_user(request):
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    address = request.POST.get('address')
    
    # Storing unencrypted PII
    user_data = {
        'email': email,
        'phone': phone,
        'address': address,
        'ip': request.META.get('REMOTE_ADDR')
    }
    
    # No encryption at rest
    db.users.insert(user_data)
    
    # Sharing with third parties without consent
    analytics.track(email, user_data)
    marketing_api.send(email, user_data)
    
    # No data minimization
    return {'status': 'success', 'user_id': user_data}

# License violation: Using GPL code
def process_data(data):
    # This function uses GPL-licensed library
    from gpl_library import process
    return process(data)

# Security issue: SQL injection risk
def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return db.execute(query)

# Export control: Strong encryption without proper handling
def encrypt_data(data):
    from cryptography.hazmat.primitives.ciphers import Cipher
    # Using AES-256 which may have export restrictions
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    return cipher.encrypt(data)
"""

def main():
    """Test LawMode with xAI Grok on risky code."""
    print("=" * 70)
    print("LawMode.ai - xAI Grok Test (Risky Code)")
    print("=" * 70)
    print()
    
    # Get API key
    xai_key = os.getenv("XAI_API_KEY") or os.getenv("GROK_API_KEY")
    if not xai_key or xai_key.startswith("your-"):
        print("⚠️  Please set XAI_API_KEY environment variable")
        print("   export XAI_API_KEY='xai-your-key-here'")
        sys.exit(1)
    
    print(f"✓ Using xAI API Key: {xai_key[:15]}...")
    print()
    
    # Configure
    config = LawModeConfig.from_file()
    config.llm.provider = "grok"
    config.llm.model = "grok-2-1212"
    config.llm.api_key = xai_key
    
    print(f"Configuration:")
    print(f"  Provider: {config.llm.provider}")
    print(f"  Model: {config.llm.model}")
    print()
    
    # Initialize
    print("Initializing agent...")
    agent = LawModeAgent(config)
    print("✓ Agent ready")
    print()
    
    # Review
    print("Analyzing code for legal compliance issues...")
    print("-" * 70)
    review = agent.review_code(test_code, file_path="risky_code.py")
    print("-" * 70)
    print()
    
    # Results
    print("=" * 70)
    print("LEGAL REVIEW RESULTS")
    print("=" * 70)
    print(f"Review ID: {review.review_id}")
    print(f"Timestamp: {review.timestamp}")
    print(f"Jurisdictions: {', '.join(review.jurisdictions) if review.jurisdictions else 'Auto-detected'}")
    print(f"Domain: {review.domain or 'Not detected'}")
    print()
    
    # Risk summary
    severity_counts = {}
    for risk in review.risks:
        sev = risk.severity.value
        severity_counts[sev] = severity_counts.get(sev, 0) + 1
    
    print("Risk Summary:")
    for severity in ["Critical", "High", "Medium", "Low"]:
        count = severity_counts.get(severity, 0)
        if count > 0:
            emoji = "🔴" if severity == "Critical" else "🟡" if severity == "High" else "🔵" if severity == "Medium" else "🟢"
            print(f"  {emoji} {severity}: {count}")
    
    print(f"\nTotal Risks Found: {len(review.risks)}")
    print()
    
    # Detailed risks
    if review.risks:
        print("=" * 70)
        print("DETAILED RISK ANALYSIS")
        print("=" * 70)
        print()
        
        for i, risk in enumerate(review.risks, 1):
            print(f"{i}. [{risk.severity.value}] {risk.id}: {risk.title}")
            print(f"   📜 Law: {risk.law}")
            if risk.citation:
                print(f"   🔗 Citation: {risk.citation}")
            print(f"   📝 Description: {risk.description}")
            print(f"   ✅ Mitigation: {risk.mitigation}")
            if risk.file_path:
                print(f"   📁 File: {risk.file_path}")
            print()
    else:
        print("✓ No legal risks identified in this code")
    
    # Generate artifacts
    print("=" * 70)
    print("Generating artifacts...")
    artifacts = agent.generate_artifacts(review)
    print("✓ Artifacts generated:")
    for name, path in artifacts.items():
        print(f"   - {name}: {path}")
    
    print()
    print("=" * 70)
    print("✅ Review Complete!")
    print("=" * 70)
    print()
    print("⚠️  NOT LEGAL ADVICE: Automated analysis for informational purposes only.")

if __name__ == "__main__":
    main()

