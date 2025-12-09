#!/usr/bin/env python3
"""Full test with xAI Grok-4-fast-non-reasoning model."""

import os
import sys
from lawmode import LawModeAgent
from lawmode.config import LawModeConfig

# Comprehensive test code with multiple legal issues
test_code = """
import requests
import json
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# GDPR violation: Collecting PII without consent
def signup_user(request):
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    address = request.POST.get('address')
    ssn = request.POST.get('ssn')  # Highly sensitive data
    
    # Storing unencrypted PII
    user_data = {
        'email': email,
        'phone': phone,
        'address': address,
        'ssn': ssn,  # GDPR violation - storing SSN
        'ip': request.META.get('REMOTE_ADDR'),
        'timestamp': datetime.now().isoformat()
    }
    
    # No encryption at rest
    db.users.insert(user_data)
    
    # Sharing with third parties without consent
    analytics.track(email, user_data)
    marketing_api.send(email, user_data)
    third_party_service.upload(user_data)
    
    # No data minimization - collecting more than needed
    return {'status': 'success', 'user_id': user_data}

# License violation: Using GPL code in proprietary project
def process_data(data):
    # This function uses GPL-licensed library
    from gpl_library import process
    result = process(data)
    # No license header or attribution
    return result

# Security issue: SQL injection risk
def get_user(user_id):
    # SQL injection vulnerability
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return db.execute(query)

# Export control: Strong encryption without proper handling
def encrypt_data(data, key):
    # Using AES-256 which may have export restrictions (EAR/ITAR)
    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
        backend=default_backend()
    )
    return cipher.encrypt(data)

# Accessibility: Missing ARIA labels
def render_form():
    return '''
    <form>
        <input type="text" name="email" />
        <input type="password" name="password" />
        <button type="submit">Submit</button>
    </form>
    '''

# Copyright: Potential code snippet without attribution
def calculate_hash(data):
    # This looks like copied code from Stack Overflow
    return hashlib.sha256(data.encode()).hexdigest()
"""

def main():
    """Full test with Grok-4-fast-non-reasoning."""
    print("=" * 70)
    print("LawMode.ai - Full Test with grok-4-fast-non-reasoning")
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
    
    # Configure for grok-4-fast-non-reasoning
    print("Configuring LawMode for grok-4-fast-non-reasoning...")
    config = LawModeConfig.from_file()
    config.llm.provider = "grok"
    config.llm.model = "grok-4-fast-non-reasoning"
    config.llm.api_key = xai_key
    
    print(f"  Provider: {config.llm.provider}")
    print(f"  Model: {config.llm.model}")
    print(f"  Temperature: {config.llm.temperature}")
    print(f"  Max Tokens: {config.llm.max_tokens}")
    print()
    
    # Initialize agent
    print("Initializing LawMode agent...")
    try:
        agent = LawModeAgent(config)
        print("✓ Agent initialized successfully")
        print()
    except Exception as e:
        print(f"❌ ERROR: Failed to initialize agent: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Review code
    print("Analyzing code for legal compliance issues...")
    print("-" * 70)
    print("Test Code Preview:")
    print(test_code[:200] + "...")
    print("-" * 70)
    print()
    
    try:
        review = agent.review_code(test_code, file_path="risky_code.py")
        print("✓ Review completed successfully")
        print()
    except Exception as e:
        print(f"❌ ERROR: Review failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Display results
    print("=" * 70)
    print("LEGAL REVIEW RESULTS")
    print("=" * 70)
    print(f"Review ID: {review.review_id}")
    print(f"Timestamp: {review.timestamp}")
    print(f"Jurisdictions: {', '.join(review.jurisdictions) if review.jurisdictions else 'Not detected'}")
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
            desc = risk.description[:300] + "..." if len(risk.description) > 300 else risk.description
            print(f"   📝 Description: {desc}")
            mit = risk.mitigation[:300] + "..." if len(risk.mitigation) > 300 else risk.mitigation
            print(f"   ✅ Mitigation: {mit}")
            if risk.file_path:
                print(f"   📁 File: {risk.file_path}")
            if risk.line_start:
                print(f"   📍 Lines: {risk.line_start}-{risk.line_end or risk.line_start}")
            print()
    else:
        print("✓ No legal risks identified in this code")
    
    # Generate artifacts
    print("=" * 70)
    print("Generating artifacts...")
    try:
        artifacts = agent.generate_artifacts(review)
        print("✓ Artifacts generated:")
        for name, path in artifacts.items():
            print(f"   - {name}: {path}")
    except Exception as e:
        print(f"⚠️  Warning: Artifact generation failed: {e}")
    
    # Performance metrics
    print()
    print("=" * 70)
    print("PERFORMANCE METRICS")
    print("=" * 70)
    print(f"Model Used: {config.llm.model}")
    print(f"Provider: {config.llm.provider}")
    print(f"Risks Identified: {len(review.risks)}")
    print(f"Chains Executed: {len(review.history)}")
    print()
    
    print("=" * 70)
    print("✅ Full Test Complete!")
    print("=" * 70)
    print()
    print("⚠️  NOT LEGAL ADVICE: Automated analysis for informational purposes only.")

if __name__ == "__main__":
    main()

