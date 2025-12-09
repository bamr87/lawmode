# Changelog

All notable changes to LawMode.ai will be documented in this file.

## [Unreleased]

### Changed
- Removed Groq and Anthropic provider support
- Now supports only OpenAI and xAI Grok providers
- Updated all documentation to reflect current provider support

### Added
- xAI Grok integration with custom LangChain wrapper
- Support for multiple Grok models (grok-2-1212, grok-3, grok-4 variants)
- Integration test suite in `tests/integration/`
- `LAWYER_MODE_IS_ALWAYS_ON.md` automatically copied to `.lawmode/` folder

### Removed
- Groq backend and dependencies (`langchain-groq`)
- Anthropic backend and dependencies (`langchain-anthropic`)
- Test files moved from root to `tests/integration/`

## [0.1.0] - 2025-12-06

### Added
- Initial MVP release
- Multi-chain legal reasoning engine (8 chains)
- GitHub PR integration
- VSCode extension
- CLI tool
- Artifact generation system
- Legal research tools (EUR-Lex, CourtListener, SPDX, Google Scholar)
- Audit trail and checkpointing

