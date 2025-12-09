# Lawyer Mode is Always On

LawMode.ai runs continuously in your development workflow, automatically reviewing:

- ✅ Every line of code you write
- ✅ Every commit you make
- ✅ Every pull request you open
- ✅ Every prompt you craft
- ✅ Every dependency you add

## How It Works

1. **Automatic Detection**: LawMode scans your code changes in real-time
2. **Multi-Chain Analysis**: 8 specialized legal reasoning chains analyze your code
3. **Risk Identification**: Potential legal issues are flagged with severity levels
4. **Artifact Generation**: Complete legal review artifacts are created in `lawmode/` folder
5. **PR Gating**: Critical risks automatically block merges (configurable)

## What Gets Reviewed

- **Privacy Compliance**: GDPR, CCPA, PIPEDA violations
- **License Compliance**: GPL contamination, unlicensed code
- **Accessibility**: WCAG compliance issues
- **Security**: OWASP top 10, export control (EAR/ITAR)
- **Copyright**: Potential infringement from copied code
- **Regulatory**: Industry-specific compliance (fintech, healthcare, etc.)

## Configuration

Customize LawMode behavior via `.lawmode/policy.yaml`:

```yaml
jurisdictions:
  - US-CA
  - EU
  - UK

severity_gating:
  critical: block
  high: require_approval
  medium: comment
  low: comment

domains:
  - fintech
  - healthcare
```

## Privacy & Security

- All analysis happens locally or in your secure environment
- Code is never stored unless you explicitly commit artifacts
- Self-hostable enterprise version available
- Bring your own LLM API keys

---

**Remember**: LawMode.ai is NOT legal advice. Always consult qualified legal counsel for legal matters.

