# Integration Tests

This directory contains integration tests for LawMode.ai that test the full system with real API calls.

## Test Scripts

### `test_grok_simple.py`
Simple test script for xAI Grok - prompts for API key if not set.
- Tests basic functionality
- Interactive API key input
- Good for quick verification

### `test_grok_xai.py`
Basic xAI Grok API test.
- Tests API connection
- Verifies agent initialization
- Checks chain execution

### `test_grok_risks.py`
Test with code that should trigger legal risks.
- Tests risk detection capabilities
- Uses code with GDPR, license, and security issues
- Shows detailed risk analysis

### `test_grok4_fast.py`
Full test with grok-4-fast-non-reasoning model.
- Comprehensive test with multiple legal issues
- Tests all 8 chains
- Performance metrics included

### `test_local.py`
Local test file with legal compliance issues.
- Can be used with CLI: `lawmode test_local.py`
- Contains GDPR violations, license issues, SQL injection risks

## Running Tests

### Prerequisites
```bash
export XAI_API_KEY="your-xai-api-key-here"
export LAWMODE_LLM_PROVIDER="grok"
export LAWMODE_LLM_MODEL="grok-4-fast-non-reasoning"
```

### Run Individual Tests
```bash
# Simple test
python3 tests/integration/test_grok_simple.py

# Full test with risky code
python3 tests/integration/test_grok_risks.py

# Test with grok-4-fast-non-reasoning
python3 tests/integration/test_grok4_fast.py

# Test local file with CLI
lawmode tests/integration/test_local.py --verbose
```

### Run All Integration Tests
```bash
for test in tests/integration/test_*.py; do
    echo "Running $test..."
    python3 "$test"
    echo ""
done
```

## Test Files Used

- `test_local.py` - Can be scanned directly with CLI
- Other test scripts contain inline test code

## Notes

- These tests make real API calls and may incur costs
- Ensure API keys are set before running
- Tests verify end-to-end functionality including:
  - API connectivity
  - Agent initialization
  - Chain execution
  - Risk detection
  - Artifact generation

