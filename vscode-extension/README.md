# LawMode.ai VSCode Extension

VSCode extension for LawMode.ai - inline legal compliance warnings as you code.

## Features

- 🔍 **Inline Diagnostics**: Red/yellow squiggles show legal risks in your code
- 💡 **Hover Tooltips**: Detailed risk information on hover
- 📊 **Risk Panel**: View all identified risks in a dedicated panel
- ⚡ **Auto-scan**: Automatically scans files on save
- 🎯 **Severity Filtering**: Configure minimum severity level to display

## Usage

1. Install the extension from the VSCode marketplace
2. Configure your LLM API key in settings
3. Code normally - LawMode will automatically highlight legal risks

## Configuration

Open VSCode settings and search for "LawMode":

- `lawmode.enabled`: Enable/disable LawMode (default: true)
- `lawmode.jurisdictions`: Jurisdictions to check (default: ["US", "EU"])
- `lawmode.severityLevel`: Minimum severity to display (default: "all")
- `lawmode.apiKey`: Your LLM API key
- `lawmode.llmProvider`: LLM provider (openai, grok)

## Commands

- `LawMode: Scan Current File` - Manually scan the active file
- `LawMode: Scan Workspace` - Scan all files in workspace
- `LawMode: Show Risks` - Open risks panel

## Disclaimer

⚠️ **NOT LEGAL ADVICE**: LawMode.ai provides automated legal compliance analysis for informational purposes only. This does not constitute legal advice. Consult qualified legal counsel for legal matters.

