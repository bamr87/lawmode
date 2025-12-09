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
exports.LawModeDiagnostics = void 0;
const vscode = __importStar(require("vscode"));
class LawModeDiagnostics {
    constructor() {
        this.diagnosticCollection = vscode.languages.createDiagnosticCollection('lawmode');
    }
    updateDiagnostics(document, review) {
        const diagnostics = [];
        for (const risk of review.risks) {
            if (!risk.file_path || risk.file_path !== document.fileName) {
                continue;
            }
            const range = this.getRiskRange(document, risk);
            const diagnostic = this.createDiagnostic(risk, range);
            diagnostics.push(diagnostic);
        }
        this.diagnosticCollection.set(document.uri, diagnostics);
    }
    getRiskRange(document, risk) {
        if (risk.line_start) {
            const startLine = Math.max(0, risk.line_start - 1);
            const endLine = risk.line_end ? Math.max(0, risk.line_end - 1) : startLine;
            return new vscode.Range(new vscode.Position(startLine, 0), new vscode.Position(endLine, Number.MAX_VALUE));
        }
        // Default to first line if no line info
        return new vscode.Range(0, 0, 0, Number.MAX_VALUE);
    }
    createDiagnostic(risk, range) {
        const severity = this.mapSeverity(risk.severity);
        const message = `${risk.title} (${risk.law}): ${risk.description}`;
        const diagnostic = new vscode.Diagnostic(range, message, severity);
        diagnostic.source = 'LawMode';
        diagnostic.code = risk.id;
        // Add hover information
        diagnostic.relatedInformation = [
            new vscode.DiagnosticRelatedInformation(new vscode.Location(vscode.Uri.file(risk.file_path || ''), range), `Mitigation: ${risk.mitigation}`)
        ];
        return diagnostic;
    }
    mapSeverity(severity) {
        switch (severity) {
            case 'Critical':
            case 'High':
                return vscode.DiagnosticSeverity.Error;
            case 'Medium':
                return vscode.DiagnosticSeverity.Warning;
            case 'Low':
                return vscode.DiagnosticSeverity.Information;
            default:
                return vscode.DiagnosticSeverity.Warning;
        }
    }
    dispose() {
        this.diagnosticCollection.dispose();
    }
}
exports.LawModeDiagnostics = LawModeDiagnostics;
//# sourceMappingURL=diagnostics.js.map