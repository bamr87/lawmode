#!/usr/bin/env python3
"""
Debug script for LawMode Agent
Use this to debug the core agent functionality
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from lawmode.core import LawModeAgent
from lawmode.config import LawModeConfig

# Sample code to analyze
SAMPLE_CODE = """
def fetch_user_email():
    userEmail = "test@example.com"
    # Missing consent check
    return userEmail

def process_data():
    # GPL code here
    pass
"""


def main():
    print("🔍 LawMode Agent Debug Session")
    print("=" * 50)
    
    # Load configuration
    print("\n1. Loading configuration...")
    config = LawModeConfig.from_file()
    print(f"   ✓ Config loaded")
    print(f"   - Provider: {config.llm.provider}")
    print(f"   - Model: {config.llm.model}")
    print(f"   - Jurisdictions: {config.policy.jurisdictions}")
    
    # Initialize agent
    print("\n2. Initializing agent...")
    agent = LawModeAgent(config)
    print(f"   ✓ Agent initialized")
    
    # Review code
    print("\n3. Reviewing code...")
    print(f"   Code length: {len(SAMPLE_CODE)} chars")
    
    review = agent.review_code(SAMPLE_CODE, file_path="debug_test.py")
    
    print(f"\n4. Review Results:")
    print(f"   - Review ID: {review.review_id}")
    print(f"   - Risks found: {len(review.risks)}")
    
    for i, risk in enumerate(review.risks, 1):
        print(f"\n   Risk {i}:")
        print(f"   - ID: {risk.id}")
        print(f"   - Severity: {risk.severity}")
        print(f"   - Title: {risk.title}")
        print(f"   - Law: {risk.law}")
        print(f"   - Description: {risk.description[:100]}...")
    
    # Generate artifacts
    print("\n5. Generating artifacts...")
    artifacts = agent.generate_artifacts(review)
    print(f"   ✓ Artifacts generated:")
    for key, path in artifacts.items():
        print(f"   - {key}: {path}")
    
    print("\n✅ Debug session complete!")
    print("=" * 50)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

