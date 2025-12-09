#!/usr/bin/env python3
"""
Debug script for LawMode Chain Builder
Use this to debug the multi-chain reasoning engine
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from lawmode.chains import build_lawmode_chains
from lawmode.config import LawModeConfig

# Sample code to analyze
SAMPLE_CODE = """
def collect_user_data():
    email = request.form.get('email')
    # No consent check
    store_in_database(email)
"""


def main():
    print("🔗 LawMode Chain Builder Debug Session")
    print("=" * 50)
    
    # Load configuration
    print("\n1. Loading configuration...")
    config = LawModeConfig.from_file()
    print(f"   ✓ Config loaded")
    
    # Build chain
    print("\n2. Building legal reasoning chain...")
    from lawmode.llm.factory import create_llm_backend
    llm_backend = create_llm_backend(config.llm)
    chain = build_lawmode_chains(llm_backend)
    print(f"   ✓ Chain built")
    
    # Prepare input
    print("\n3. Preparing input...")
    from datetime import datetime
    initial_state = {
        "code": SAMPLE_CODE,
        "file_path": "debug_test.py",
        "commit_sha": None,
        "timestamp": datetime.utcnow().isoformat(),
    }
    print(f"   - Code length: {len(SAMPLE_CODE)} chars")
    print(f"   - File path: {initial_state['file_path']}")
    
    # Invoke chain
    print("\n4. Invoking chain...")
    print("   (This may take a moment as it runs through all 8 chains)")
    
    try:
        result = chain.invoke(initial_state)
        
        print(f"\n5. Chain Results:")
        print(f"   - Keys in result: {list(result.keys())}")
        
        for key, value in result.items():
            if isinstance(value, str) and len(value) > 100:
                print(f"   - {key}: {value[:100]}...")
            elif isinstance(value, list) and len(value) > 0:
                print(f"   - {key}: [{len(value)} items]")
            else:
                print(f"   - {key}: {value}")
        
        print("\n✅ Chain execution complete!")
        
    except Exception as e:
        print(f"\n❌ Chain execution error: {e}")
        import traceback
        traceback.print_exc()
        raise
    
    print("=" * 50)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

