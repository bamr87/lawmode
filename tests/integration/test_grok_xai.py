#!/usr/bin/env python3
"""Test LawMode with xAI Grok API."""

import os
import sys
from lawmode import LawModeAgent
from lawmode.config import LawModeConfig

# Test code with potential legal issues
test_code = """
def collect_user_data():
    # Potential GDPR violation - collecting email without consent
    user_email = request.form.get('email')
    user_name = request.form.get('name')
    
    # Storing in database without encryption
    db.users.insert({
        'email': user_email,
        'name': user_name,
        'ip_address': request.remote_addr
    })
    
    # Sending to analytics without user consent
    analytics.track(user_email, {
        'event': 'signup',
        'name': user_name
    })
    
    return {'status': 'success'}
"""


def main():
    """Test LawMode with xAI Grok."""
    print("=" * 60)
    print("LawMode.ai - xAI Grok API Test")
    print("=" * 60)
    print()
    
    # Check for API key
    xai_key = os.getenv("XAI_API_KEY") or os.getenv("GROK_API_KEY")
    if not xai_key:
        print("❌ ERROR: XAI_API_KEY or GROK_API_KEY environment variable not set")
        print()
        print("Please set it with:")
        print("  export XAI_API_KEY='your-api-key-here'")
        print("  # OR")
        print("  export GROK_API_KEY='your-api-key-here'")
        print()
        print("Or create a .env file from .env.example")
        sys.exit(1)
    
    print(f"✓ Found xAI API Key (length: {len(xai_key)})")
    print(f"  Key preview: {xai_key[:10]}...")
    print()
    
    # Configure for Grok
    print("Configuring LawMode for xAI Grok...")
    config = LawModeConfig.from_file()
    config.llm.provider = "grok"
    config.llm.model = "grok-2-1212"  # or "grok-2", "grok-4-0709", "grok-beta"
    config.llm.api_key = xai_key
    
    print(f"  Provider: {config.llm.provider}")
    print(f"  Model: {config.llm.model}")
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
    print("Reviewing test code...")
    print("-" * 60)
    print("Test Code:")
    print(test_code)
    print("-" * 60)
    print()
    
    try:
        review = agent.review_code(test_code, file_path="test.py")
        print("✓ Review completed successfully")
        print()
    except Exception as e:
        print(f"❌ ERROR: Review failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Display results
    print("=" * 60)
    print("Review Results:")
    print("=" * 60)
    print(f"Review ID: {review.review_id}")
    print(f"Timestamp: {review.timestamp}")
    print(f"Jurisdictions: {', '.join(review.jurisdictions) if review.jurisdictions else 'Not detected'}")
    print(f"Domain: {review.domain or 'Not detected'}")
    print(f"Total Risks: {len(review.risks)}")
    print()
    
    if review.risks:
        print("Identified Risks:")
        print("-" * 60)
        for i, risk in enumerate(review.risks, 1):
            print(f"\n{i}. [{risk.severity.value}] {risk.id}: {risk.title}")
            print(f"   Law: {risk.law}")
            if risk.citation:
                print(f"   Citation: {risk.citation}")
            print(f"   Description: {risk.description[:150]}...")
            print(f"   Mitigation: {risk.mitigation[:150]}...")
    else:
        print("✓ No risks identified")
    
    print()
    print("=" * 60)
    print("Test completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()

