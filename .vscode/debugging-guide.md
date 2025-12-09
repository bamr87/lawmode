# LawMode Debugging Guide

This guide explains how to use the VSCode debugger configurations for LawMode.

## Prerequisites

1. **Python Extension**: Install the Python extension for VSCode
2. **Debugpy**: Should be installed automatically, but if not:
   ```bash
   pip install debugpy
   ```
3. **Environment Setup**: Ensure your `.env` file is configured with API keys

## Debug Configurations

### 1. LawMode CLI - Scan File
- **Purpose**: Debug scanning a specific file
- **Usage**: 
  - Press F5 or select from Run menu
  - Enter file path when prompted (default: `examples/example_scan.py`)
- **Breakpoints**: Set breakpoints in `lawmode/cli.py` or `lawmode/core.py`

### 2. LawMode CLI - Scan Directory
- **Purpose**: Debug scanning an entire directory
- **Usage**: 
  - Press F5 or select from Run menu
  - Enter directory path when prompted (default: `lawmode`)
- **Breakpoints**: Set breakpoints in `lawmode/cli.py` or `lawmode/core.py`

### 3. LawMode CLI - Scan with Diff
- **Purpose**: Debug git diff analysis
- **Usage**: 
  - Press F5 or select from Run menu
  - Enter git diff spec when prompted (default: `HEAD~1`)
- **Breakpoints**: Set breakpoints in `lawmode/cli.py` or `lawmode/core.py`

### 4. LawMode Core Agent
- **Purpose**: Debug the core agent without CLI overhead
- **Usage**: 
  - Press F5 or select from Run menu
  - Runs `examples/debug_agent.py`
- **Breakpoints**: Set breakpoints in `lawmode/core.py` or `examples/debug_agent.py`

### 5. Current File
- **Purpose**: Debug any Python file you have open
- **Usage**: 
  - Open a Python file
  - Press F5 or select from Run menu
- **Breakpoints**: Set breakpoints in the current file

### 6. Pytest - All Tests
- **Purpose**: Debug all tests
- **Usage**: 
  - Press F5 or select from Run menu
  - Runs all tests in `tests/` directory
- **Breakpoints**: Set breakpoints in test files or code being tested

### 7. Pytest - Current Test File
- **Purpose**: Debug tests in the current file
- **Usage**: 
  - Open a test file
  - Press F5 or select from Run menu
- **Breakpoints**: Set breakpoints in test file or code being tested

### 8. Debug Chain Builder
- **Purpose**: Debug the multi-chain reasoning engine
- **Usage**: 
  - Press F5 or select from Run menu
  - Runs `examples/debug_chains.py`
- **Breakpoints**: Set breakpoints in `lawmode/chains/chain_builder.py` or `examples/debug_chains.py`

### 9. Debug LLM Backend
- **Purpose**: Debug LLM provider integration
- **Usage**: 
  - Press F5 or select from Run menu
  - Runs `examples/debug_llm.py`
- **Breakpoints**: Set breakpoints in `lawmode/llm/` files or `examples/debug_llm.py`

## Common Debugging Scenarios

### Debugging a Failed Review

1. Set breakpoint in `lawmode/core.py` at `review_code()` method
2. Use "LawMode CLI - Scan File" configuration
3. Step through the review process
4. Inspect `state` dictionary at each chain step

### Debugging Chain Execution

1. Set breakpoint in `lawmode/chains/chain_builder.py` at chain node functions
2. Use "Debug Chain Builder" configuration
3. Step through each of the 8 chains
4. Inspect intermediate results

### Debugging LLM Issues

1. Set breakpoint in `lawmode/llm/factory.py` or provider-specific files
2. Use "Debug LLM Backend" configuration
3. Inspect API calls and responses
4. Check for authentication/configuration issues

### Debugging Configuration Loading

1. Set breakpoint in `lawmode/config.py` at `from_file()` method
2. Use any configuration that loads config
3. Inspect loaded configuration values
4. Check environment variable overrides

## Debugging Tips

1. **Use `justMyCode: false`**: This allows stepping into library code if needed
2. **Set conditional breakpoints**: Right-click on breakpoint to add conditions
3. **Watch variables**: Add variables to watch panel for monitoring
4. **Call stack**: Use call stack panel to navigate through execution
5. **Debug console**: Use debug console to evaluate expressions

## Environment Variables

The debugger will use environment variables from `.env` file if present. You can also override them in `launch.json`:

```json
"env": {
    "OPENAI_API_KEY": "your-key",
    "XAI_API_KEY": "your-key",
    "LAWMODE_LLM_PROVIDER": "openai"
}
```

## Troubleshooting

### Debugger won't start
- Check Python interpreter path in settings
- Ensure `debugpy` is installed: `pip install debugpy`
- Check that the file/module exists

### Breakpoints not hitting
- Ensure `justMyCode: false` is set
- Check that you're running the correct configuration
- Verify the code path matches your breakpoint location

### Import errors
- Ensure `PYTHONPATH` includes workspace folder (already set in configs)
- Check that virtual environment is activated
- Verify all dependencies are installed

### API errors during debugging
- Check `.env` file has correct API keys
- Verify API keys are valid
- Check network connectivity

