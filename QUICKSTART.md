# Quick Start Guide

Get started with LawMode.ai in 5 minutes.

## 1. Installation

```bash
# Clone and install
git clone https://github.com/lawmode/lawmode.git
cd lawmode
pip install -e .
```

## 2. Set API Key

```bash
# Option 1: Use .env file (recommended)
cp .env.example .env
# Edit .env and add your API key

# Option 2: Set environment variable directly
export OPENAI_API_KEY="your-api-key-here"
# OR use xAI Grok
export XAI_API_KEY="your-xai-api-key-here"
```

## 3. Scan Your Code

### Scan a file:
```bash
lawmode scan path/to/file.py
```

### Scan a directory:
```bash
lawmode scan src/
```

### Scan git diff:
```bash
lawmode scan --diff HEAD~1
```

### Scan with specific jurisdictions:
```bash
lawmode scan --jurisdiction US-CA EU --diff HEAD~1
```

## 4. View Results

LawMode generates artifacts in `.lawmode/`:

- `review.json` - Complete review data
- `risks.yaml` - Risk summary
- `mitigations.md` - Detailed mitigations

## 5. GitHub Integration

Add to your `.github/workflows/lawmode.yml`:

```yaml
name: LawMode Review
on: [pull_request]
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: pip install lawmode
      - run: lawmode scan --diff ${{ github.event.pull_request.base.sha }}..${{ github.event.pull_request.head.sha }}
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```

## 6. VSCode Extension

1. Install from VSCode marketplace: "LawMode"
2. Configure API key in settings
3. Get inline warnings as you code!

## Example Output

```
LawMode.ai Legal Review
======================

Review Summary:
- Review ID: abc-123-def
- Jurisdictions: US, EU
- Total Risks: 2
- Critical: 1
- High: 1

Identified Risks:
[R001] [Critical] Potential GPL license contamination
  Law: GPL-3.0
  Mitigation: Add license header or use permissive alternative

[R002] [High] Potential GDPR data minimization violation
  Law: GDPR Art. 5(1)(c)
  Mitigation: Add consent wrapper and data minimization check
```

## Next Steps

- Read [README.md](./README.md) for detailed documentation
- Check [PRD.md](./PRD.md) for complete feature list
- Configure `.lawmode/policy.yaml` for custom policies

## Need Help?

- GitHub Issues: https://github.com/lawmode/lawmode/issues
- Documentation: https://docs.lawmode.ai
- Email: support@lawmode.ai

