# Testing the LawMode VSCode Extension

## Prerequisites

1. Node.js and npm installed
2. VSCode installed
3. Dependencies installed: `npm install`
4. Extension compiled: `npm run compile`

## Testing Methods

### Method 1: VSCode Extension Development Host (Recommended)

1. **Open the extension in VSCode:**
   ```bash
   cd vscode-extension
   code .
   ```

2. **Press F5** or go to Run > Start Debugging
   - This opens a new VSCode window (Extension Development Host)
   - The extension will be loaded in this new window

3. **Test the extension:**
   - Open a test file (e.g., create `test.py` with code that triggers risks)
   - The extension should automatically scan on file open/save
   - Check for diagnostics (red/yellow squiggles)
   - Hover over diagnostics to see details
   - Use Command Palette (Cmd+Shift+P) to run:
     - `LawMode: Scan Current File`
     - `LawMode: Show Risks`

### Method 2: Package and Install Locally

1. **Package the extension:**
   ```bash
   npm install -g vsce
   vsce package
   ```
   This creates a `.vsix` file.

2. **Install in VSCode:**
   - Open VSCode
   - Go to Extensions view
   - Click "..." menu > "Install from VSIX..."
   - Select the `.vsix` file

### Method 3: Unit Testing (Mock Mode)

The extension includes mock mode that works without the CLI:

1. Create a test file `test_gdpr.py`:
   ```python
   def fetch_user_email():
       userEmail = "test@example.com"
       # Missing consent check
       return userEmail
   ```

2. The extension should detect:
   - GDPR violation (fetch + userEmail + no consent)

3. Create a test file `test_gpl.py`:
   ```python
   # GPL code here
   def some_function():
       pass
   ```

4. The extension should detect:
   - GPL license contamination

## Test Scenarios

### Scenario 1: GDPR Violation Detection
- **File**: `test_gdpr.py`
- **Code**: Contains `fetch`, `userEmail`, but no `consent`
- **Expected**: High severity risk for GDPR violation

### Scenario 2: GPL License Issue
- **File**: `test_gpl.py`
- **Code**: Contains `GPL` but no `license`
- **Expected**: Critical severity risk for GPL contamination

### Scenario 3: Auto-scan on Save
- **File**: Any Python/JS/TS file
- **Action**: Save the file
- **Expected**: Extension automatically scans and shows diagnostics

### Scenario 4: Manual Scan Command
- **Action**: Open Command Palette > `LawMode: Scan Current File`
- **Expected**: Progress indicator, then diagnostics appear

### Scenario 5: Risks Panel
- **Action**: Command Palette > `LawMode: Show Risks`
- **Expected**: Webview panel opens showing risks

## Debugging

1. **Check Output Panel:**
   - View > Output
   - Select "Log (Extension Host)" or "LawMode"
   - Look for console.log messages

2. **Check Developer Tools:**
   - Help > Toggle Developer Tools
   - Check Console for errors

3. **Check Extension Host Logs:**
   - View > Output > "Log (Extension Host)"

## Configuration Testing

Test different configurations in `.vscode/settings.json`:

```json
{
  "lawmode.enabled": true,
  "lawmode.jurisdictions": ["US", "EU"],
  "lawmode.severityLevel": "all",
  "lawmode.llmProvider": "openai",
  "lawmode.apiKey": "your-key-here"
}
```

## Expected Behavior

- ✅ Extension activates on startup
- ✅ Disclaimer shown on first activation
- ✅ Auto-scan works on file save
- ✅ Diagnostics appear as squiggles
- ✅ Hover shows risk details
- ✅ Commands work via Command Palette
- ✅ Risks panel opens and displays content
- ✅ Configuration changes take effect

## Troubleshooting

- **Extension not activating**: Check Output panel for errors
- **No diagnostics**: Ensure `lawmode.enabled` is true
- **CLI errors**: Extension falls back to mock mode automatically
- **TypeScript errors**: Run `npm run compile` to rebuild

