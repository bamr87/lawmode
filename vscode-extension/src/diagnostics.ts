import * as vscode from 'vscode';
import { ReviewResult, Risk, Severity } from './types';

export class LawModeDiagnostics {
    private diagnosticCollection: vscode.DiagnosticCollection;

    constructor() {
        this.diagnosticCollection = vscode.languages.createDiagnosticCollection('lawmode');
    }

    updateDiagnostics(document: vscode.TextDocument, review: ReviewResult) {
        const diagnostics: vscode.Diagnostic[] = [];

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

    private getRiskRange(document: vscode.TextDocument, risk: Risk): vscode.Range {
        if (risk.line_start) {
            const startLine = Math.max(0, risk.line_start - 1);
            const endLine = risk.line_end ? Math.max(0, risk.line_end - 1) : startLine;
            return new vscode.Range(
                new vscode.Position(startLine, 0),
                new vscode.Position(endLine, Number.MAX_VALUE)
            );
        }
        // Default to first line if no line info
        return new vscode.Range(0, 0, 0, Number.MAX_VALUE);
    }

    private createDiagnostic(risk: Risk, range: vscode.Range): vscode.Diagnostic {
        const severity = this.mapSeverity(risk.severity);
        const message = `${risk.title} (${risk.law}): ${risk.description}`;

        const diagnostic = new vscode.Diagnostic(range, message, severity);
        diagnostic.source = 'LawMode';
        diagnostic.code = risk.id;
        
        // Add hover information
        diagnostic.relatedInformation = [
            new vscode.DiagnosticRelatedInformation(
                new vscode.Location(
                    vscode.Uri.file(risk.file_path || ''),
                    range
                ),
                `Mitigation: ${risk.mitigation}`
            )
        ];

        return diagnostic;
    }

    private mapSeverity(severity: Severity): vscode.DiagnosticSeverity {
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

