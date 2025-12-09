#!/usr/bin/env python3
"""
Debug script for LawMode LLM Backend
Use this to debug LLM provider integration
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from lawmode.llm.factory import create_llm_backend
from lawmode.config import LawModeConfig


def main():
    print("🤖 LawMode LLM Backend Debug Session")
    print("=" * 50)
    
    # Load configuration
    print("\n1. Loading configuration...")
    config = LawModeConfig.from_file()
    print(f"   ✓ Config loaded")
    print(f"   - Provider: {config.llm.provider}")
    print(f"   - Model: {config.llm.model}")
    
    # Create LLM backend
    print("\n2. Creating LLM backend...")
    try:
        llm_backend = create_llm_backend(config.llm)
        print(f"   ✓ Backend created: {type(llm_backend).__name__}")
    except Exception as e:
        print(f"   ❌ Failed to create backend: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Test simple invocation
    print("\n3. Testing simple invocation...")
    test_prompt = "What is GDPR?"
    
    try:
        print(f"   Prompt: {test_prompt}")
        response = llm_backend.invoke(test_prompt)
        print(f"   ✓ Response received")
        print(f"   Response length: {len(response.content)} chars")
        print(f"   Response preview: {response.content[:200]}...")
    except Exception as e:
        print(f"   ❌ Invocation failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Test streaming (if supported)
    print("\n4. Testing streaming...")
    try:
        print(f"   Prompt: {test_prompt}")
        chunks = []
        for chunk in llm_backend.stream(test_prompt):
            if hasattr(chunk, 'content'):
                chunks.append(chunk.content)
            else:
                chunks.append(str(chunk))
        
        full_response = "".join(chunks)
        print(f"   ✓ Stream received")
        print(f"   Chunks: {len(chunks)}")
        print(f"   Response length: {len(full_response)} chars")
        print(f"   Response preview: {full_response[:200]}...")
    except Exception as e:
        print(f"   ⚠️  Streaming not supported or failed: {e}")
    
    print("\n✅ LLM backend debug complete!")
    print("=" * 50)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

