#!/usr/bin/env python3
"""Example script demonstrating LawMode usage."""

from lawmode import LawModeAgent
from lawmode.config import LawModeConfig

# Example code with potential legal issues
example_code = """
import requests

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

# GPL-licensed code snippet (potential contamination)
def gpl_function():
    # This function uses GPL-licensed code
    pass
"""


def main():
    """Run example scan."""
    print("LawMode.ai Example Scan\n")
    print("=" * 50)
    
    # Initialize agent
    config = LawModeConfig.from_file()
    agent = LawModeAgent(config)
    
    # Review code
    print("\nReviewing code...")
    review = agent.review_code(example_code, file_path="example.py")
    
    # Generate artifacts
    print("Generating artifacts...")
    artifacts = agent.generate_artifacts(review)
    
    # Display results
    print("\n" + "=" * 50)
    print("Review Results:")
    print(f"Review ID: {review.review_id}")
    print(f"Jurisdictions: {', '.join(review.jurisdictions)}")
    print(f"Domain: {review.domain or 'Not detected'}")
    print(f"\nFound {len(review.risks)} risk(s):\n")
    
    for risk in review.risks:
        print(f"  [{risk.severity.value}] {risk.id}: {risk.title}")
        print(f"    Law: {risk.law}")
        print(f"    Description: {risk.description}")
        print(f"    Mitigation: {risk.mitigation}")
        print()
    
    print("Artifacts generated:")
    for name, path in artifacts.items():
        print(f"  - {name}: {path}")
    
    print("\n" + "=" * 50)
    print("⚠️  NOT LEGAL ADVICE: Automated analysis for informational purposes only.")


if __name__ == "__main__":
    main()

