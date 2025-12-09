# LawMode.ai

The world's first always-on AI lawyer that lives inside the developer workflow.

## Overview

LawMode.ai automatically reviews every line of code, prompt, and commit using a multi-chain AI legal agent that produces auditable, reference-rich legal artifacts and blocks non-compliant changes via pull-request gating.

LawMode runs continuously in your development workflow, automatically reviewing:
- ✅ Every line of code you write
- ✅ Every commit you make
- ✅ Every pull request you open
- ✅ Every prompt you craft
- ✅ Every dependency you add

## Features

- 🔍 **Multi-Chain Legal Reasoning**: 8-chain deterministic legal reasoning pipeline
- 🤖 **AI-Agnostic**: Supports OpenAI GPT-4o and xAI Grok models
- 📚 **Tool-Forced Research**: Zero hallucinations with forced citation retrieval
- 🚫 **PR Gating**: Automatically blocks non-compliant changes
- 📝 **Auditable Artifacts**: Complete legal review trail in `lawmode/` folder
- 🔌 **Multiple Channels**: GitHub App, VSCode Extension, CLI, GitLab, Bitbucket

## How It Works

1. **Automatic Detection**: LawMode scans your code changes in real-time
2. **Multi-Chain Analysis**: 8 specialized legal reasoning chains analyze your code
3. **Risk Identification**: Potential legal issues are flagged with severity levels
4. **Artifact Generation**: Complete legal review artifacts are created in `.lawmode/` folder
5. **PR Gating**: Critical risks automatically block merges (configurable)

## What Gets Reviewed

LawMode checks for compliance issues across multiple legal domains:

- **Privacy Compliance**: GDPR, CCPA, PIPEDA violations
- **License Compliance**: GPL contamination, unlicensed code
- **Accessibility**: WCAG compliance issues
- **Security**: OWASP top 10, export control (EAR/ITAR)
- **Copyright**: Potential infringement from copied code
- **Regulatory**: Industry-specific compliance (fintech, healthcare, etc.)

## Quick Start

### Installation & Setup

```bash
# Install
pip install -e .

# Set up environment variables
cp .env.example .env
# Edit .env and add your LLM API key

# For OpenAI:
export OPENAI_API_KEY="your-api-key-here"

# For xAI Grok:
export XAI_API_KEY="your-xai-api-key-here"
export LAWMODE_LLM_PROVIDER="grok"
export LAWMODE_LLM_MODEL="grok-2-1212"
```

### CLI Usage

```bash
# Scan a directory
lawmode scan ./src

# Scan a git diff
lawmode scan --diff HEAD~1

# Scan with specific jurisdiction
lawmode scan --jurisdiction US-CA,EU
```

### GitHub Integration

Install the LawMode GitHub App from the GitHub Marketplace. It will automatically review PRs and block critical risks.

### VSCode Extension

Install "LawMode" from the VSCode marketplace. Get inline legal compliance warnings as you code.

## Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest

# Run linting
ruff check .
```

## Configuration

Customize LawMode behavior via `.lawmode/policy.yaml`:

```yaml
policy:
  jurisdictions:
    - US-CA
    - EU
    - UK
  
  severity_gating:
    critical: block
    high: require_approval
    medium: comment
    low: comment

llm:
  provider: openai  # or grok
  model: gpt-4o
```

See [INSTALL.md](./INSTALL.md) for detailed configuration options.

## Privacy & Security

- All analysis happens locally or in your secure environment
- Code is never stored unless you explicitly commit artifacts
- Self-hostable enterprise version available
- Bring your own LLM API keys

## Architecture

See [PRD.md](./PRD.md) for complete product requirements and architecture details.

## Disclaimer

**NOT LEGAL ADVICE**: LawMode.ai provides automated legal compliance analysis for informational purposes only. It does not constitute legal advice, and you should consult with qualified legal counsel for legal matters.

