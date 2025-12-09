# Installation Guide

## Quick Start

### Prerequisites

- Python 3.10 or higher
- Git
- LLM API key (OpenAI or xAI Grok)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/lawmode/lawmode.git
   cd lawmode
   ```

2. **Install LawMode:**
   ```bash
   pip install -e .
   ```

   Or with development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

3. **Set up environment variables:**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and add your API key(s)
   # Or set directly:
   export OPENAI_API_KEY="your-api-key"
   # OR
   export XAI_API_KEY="your-xai-api-key"
   ```

4. **Configure LawMode:**
   ```bash
   # Edit .lawmode/policy.yaml or create your own
   cp .lawmode/policy.yaml ~/.lawmode/policy.yaml
   ```

5. **Test installation:**
   ```bash
   lawmode scan --help
   ```

## Docker Installation

### Build Docker Image

```bash
docker build -t lawmode:latest .
```

### Run with Docker Compose

```bash
# Set environment variables in .env file
echo "OPENAI_API_KEY=your-key" > .env

# Run
docker-compose up
```

## VSCode Extension

1. Open VSCode
2. Go to Extensions (Cmd+Shift+X)
3. Search for "LawMode"
4. Click Install

Or install from source:

```bash
cd vscode-extension
npm install
npm run compile
```

Then press F5 in VSCode to run the extension in a new window.

## GitHub Integration

### GitHub Actions

The `.github/workflows/lawmode.yml` file is included. To use it:

1. Copy the workflow to your repository's `.github/workflows/` directory
2. Add your LLM API key as a GitHub secret:
   - Go to Settings → Secrets and variables → Actions
   - Add `OPENAI_API_KEY` or `XAI_API_KEY`

### GitHub App (Coming Soon)

The GitHub App is under development. For now, use GitHub Actions.

## Configuration

See `.lawmode/policy.yaml` for configuration options:

- `jurisdictions`: List of jurisdictions to check
- `severity_gating`: How to handle risks by severity
- `domains`: Industry domains (auto-detected)
- `llm`: LLM provider and model settings

### LLM Provider Configuration

LawMode supports two LLM providers:

#### OpenAI
- **API Key**: `OPENAI_API_KEY`
- **Default Model**: `gpt-4o`
- **Available Models**: `gpt-4o`, `gpt-4-turbo`, `gpt-4`, `gpt-3.5-turbo`
- **Get API Key**: https://platform.openai.com/api-keys

#### xAI Grok
- **API Key**: `XAI_API_KEY` or `GROK_API_KEY`
- **Default Model**: `grok-2-1212`
- **Available Models**:
  - `grok-2-1212` - Latest stable model (recommended)
  - `grok-3` - Latest Grok 3 model
  - `grok-3-mini` - Smaller, faster Grok 3
  - `grok-4-0709` - Grok 4 model
  - `grok-4-fast-reasoning` - Fast reasoning variant
  - `grok-4-fast-non-reasoning` - Fast non-reasoning variant
  - `grok-code-fast-1` - Code-specific model
  - `grok-2-vision-1212` - Vision-capable model
- **Get API Key**: https://console.x.ai/

Configure in `.lawmode/policy.yaml`:
```yaml
llm:
  provider: grok  # or openai
  model: grok-2-1212
  temperature: 0.1
  max_tokens: 4000
```

Or via environment variables:
```bash
export LAWMODE_LLM_PROVIDER="grok"
export LAWMODE_LLM_MODEL="grok-2-1212"
```

## Troubleshooting

### Import Errors

If you see import errors, make sure all dependencies are installed:

```bash
pip install -r requirements.txt
```

### API Key Issues

Make sure your API key is set:

```bash
echo $OPENAI_API_KEY  # Should show your OpenAI key
echo $XAI_API_KEY     # Should show your xAI Grok key
```

**xAI Grok API Key Troubleshooting:**
- API keys start with `xai-` prefix
- Verify key format: `echo $XAI_API_KEY | head -c 10`
- Check key hasn't expired or been revoked
- Get new key from: https://console.x.ai/

**Model Not Found Errors:**
- For Grok: Use valid model name (see list above)
- Default models: `gpt-4o` (OpenAI) or `grok-2-1212` (Grok)
- Check available models in `.env.example`

### Permission Errors

If you get permission errors, try:

```bash
pip install --user -e .
```

## Next Steps

- Read the [README.md](./README.md) for usage examples
- Check [PRD.md](./PRD.md) for complete product requirements
- See `.lawmode/policy.yaml` for configuration options

