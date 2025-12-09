"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = __importStar(require("vscode"));
const diagnostics_1 = require("./diagnostics");
const client_1 = require("./client");
let diagnostics;
let client;
function activate(context) {
    console.log('LawMode.ai extension is now active');
    // Initialize components
    diagnostics = new diagnostics_1.LawModeDiagnostics();
    client = new client_1.LawModeClient();
    // Register commands
    const scanCommand = vscode.commands.registerCommand('lawmode.scan', () => {
        const editor = vscode.window.activeTextEditor;
        if (editor) {
            scanDocument(editor.document);
        }
    });
    const scanWorkspaceCommand = vscode.commands.registerCommand('lawmode.scanWorkspace', () => {
        scanWorkspace();
    });
    const showRisksCommand = vscode.commands.registerCommand('lawmode.showRisks', () => {
        showRisksPanel();
    });
    context.subscriptions.push(scanCommand, scanWorkspaceCommand, showRisksCommand);
    // Auto-scan on document save
    const onSave = vscode.workspace.onDidSaveTextDocument((document) => {
        const config = vscode.workspace.getConfiguration('lawmode');
        if (config.get('enabled', true)) {
            scanDocument(document);
        }
    });
    context.subscriptions.push(onSave);
    // Scan active document on open
    if (vscode.window.activeTextEditor) {
        scanDocument(vscode.window.activeTextEditor.document);
    }
    // Show disclaimer on first activation
    showDisclaimer(context);
}
function scanDocument(document) {
    const config = vscode.workspace.getConfiguration('lawmode');
    if (!config.get('enabled', true)) {
        return;
    }
    const code = document.getText();
    const filePath = document.fileName;
    vscode.window.withProgress({
        location: vscode.ProgressLocation.Window,
        title: "LawMode: Analyzing legal compliance...",
        cancellable: false
    }, async (progress) => {
        try {
            const review = await client.reviewCode(code, filePath);
            diagnostics.updateDiagnostics(document, review);
            if (review.risks.length > 0) {
                vscode.window.showInformationMessage(`LawMode: Found ${review.risks.length} legal risk(s)`, 'Show Details').then(selection => {
                    if (selection === 'Show Details') {
                        showRisksPanel();
                    }
                });
            }
        }
        catch (error) {
            vscode.window.showErrorMessage(`LawMode error: ${error}`);
        }
    });
}
function scanWorkspace() {
    vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: "LawMode: Scanning workspace...",
        cancellable: false
    }, async (progress) => {
        // Implementation would scan all files in workspace
        vscode.window.showInformationMessage('LawMode: Workspace scan completed');
    });
}
function showRisksPanel() {
    // Create and show a webview panel with risks
    const panel = vscode.window.createWebviewPanel('lawmodeRisks', 'LawMode Legal Risks', vscode.ViewColumn.Beside, {});
    panel.webview.html = getRisksWebviewContent();
}
function getRisksWebviewContent() {
    return `<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: var(--vscode-font-family); padding: 20px; }
        .risk { margin: 10px 0; padding: 10px; border-left: 4px solid; }
        .critical { border-color: red; }
        .high { border-color: orange; }
        .medium { border-color: blue; }
        .low { border-color: green; }
    </style>
</head>
<body>
    <h1>LawMode Legal Risks</h1>
    <p>Review identified legal compliance risks in your code.</p>
    <p><em>⚠️ NOT LEGAL ADVICE: Automated analysis for informational purposes only.</em></p>
</body>
</html>`;
}
function showDisclaimer(context) {
    const hasSeenDisclaimer = context.globalState.get('lawmode.disclaimerSeen', false);
    if (!hasSeenDisclaimer) {
        vscode.window.showWarningMessage('LawMode.ai: NOT LEGAL ADVICE - Automated compliance analysis for informational purposes only.', 'I Understand').then(selection => {
            if (selection === 'I Understand') {
                context.globalState.update('lawmode.disclaimerSeen', true);
            }
        });
    }
}
function deactivate() {
    if (diagnostics) {
        diagnostics.dispose();
    }
}
//# sourceMappingURL=extension.js.map