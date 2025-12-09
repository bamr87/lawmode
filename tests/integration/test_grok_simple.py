#!/usr/bin/env python3
"""Simple test script for xAI Grok - prompts for API key if not set."""

import os
import sys
from lawmode import LawModeAgent
from lawmode.config import LawModeConfig

# Simple test code
test_code = """
def process_user_data(email, name):
    # Storing PII without encryption
    db.users.insert({'email': email, 'name': name})
    # Sending to third-party without consent
    analytics.track(email)
"""

def main():
    """Test LawMode with xAI Grok."""
    print("=" * 60)
    print("LawMode.ai - xAI Grok Simple Test")
    print("=" * 60)
    print()
    
    # Check for API key
    xai_key = os.getenv("XAI_API_KEY") or os.getenv("GROK_API_KEY")
    
    if not xai_key or xai_key.startswith("your-"):
        print("⚠️  xAI API key not found or is placeholder")
        print()
        print("Please set your xAI API key:")
        print("  export XAI_API_KEY='xai-your-actual-key-here'")
        print()
        print("Or run this script with:")
        print("  XAI_API_KEY='your-key' python3 test_grok_simple.py")
        print()
        
        # Try to get from user input
        try:
            key_input = input("Enter your xAI API key (or press Enter to skip): ").strip()
            if key_input and key_input.startswith("xai-"):
                xai_key = key_input
                os.environ["XAI_API_KEY"] = xai_key
                print("✓ API key set")
            else:
                print("Skipping test - no valid API key provided")
                sys.exit(0)
        except (EOFError, KeyboardInterrupt):
            print("\nSkipping test")
            sys.exit(0)
    
    print(f"✓ Found xAI API Key (length: {len(xai_key)})")
    print(f"  Key preview: {xai_key[:15]}...")
    print()
    
    # Configure for Grok
    print("Configuring LawMode for xAI Grok...")
    config = LawModeConfig.from_file()
    config.llm.provider = "grok"
    config.llm.model = "grok-2-1212"
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
            desc = risk.description[:200] + "..." if len(risk.description) > 200 else risk.description
            print(f"   Description: {desc}")
            mit = risk.mitigation[:200] + "..." if len(risk.mitigation) > 200 else risk.mitigation
            print(f"   Mitigation: {mit}")
    else:
        print("✓ No risks identified")
    
    print()
    print("=" * 60)
    print("✅ Test completed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main()

