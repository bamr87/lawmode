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
exports.LawModeClient = void 0;
const vscode = __importStar(require("vscode"));
class LawModeClient {
    async callLawModeAPI(code, filePath) {
        const config = vscode.workspace.getConfiguration('lawmode');
        // In production, this would call the LawMode API or local CLI
        // For MVP, we'll simulate or call local CLI process
        try {
            // Option 1: Call local CLI via subprocess
            const { exec } = require('child_process');
            const { promisify } = require('util');
            const execAsync = promisify(exec);
            // Write code to temp file
            const fs = require('fs');
            const path = require('path');
            const os = require('os');
            const tempFile = path.join(os.tmpdir(), `lawmode_${Date.now()}.tmp`);
            fs.writeFileSync(tempFile, code);
            // Call lawmode CLI
            const { stdout } = await execAsync(`lawmode scan "${tempFile}" --json`);
            // Clean up
            fs.unlinkSync(tempFile);
            return JSON.parse(stdout);
        }
        catch (error) {
            // Fallback: return mock data for MVP
            console.error('LawMode CLI error:', error);
            return this.getMockReview(code, filePath);
        }
    }
    async reviewCode(code, filePath) {
        return this.callLawModeAPI(code, filePath);
    }
    getMockReview(code, filePath) {
        // Mock review for MVP demonstration
        const risks = [];
        // Simple heuristics for MVP
        // Check for GDPR violation: fetch + email without consent
        const hasFetch = code.toLowerCase().includes('fetch');
        const hasEmail = code.toLowerCase().includes('useremail') ||
            code.toLowerCase().includes('user_email') ||
            code.toLowerCase().includes('email');
        const hasConsent = code.toLowerCase().includes('consent');
        if (hasFetch && hasEmail && !hasConsent) {
            risks.push({
                id: 'R001',
                severity: 'High',
                title: 'Potential GDPR data minimization violation',
                law: 'GDPR Art. 5(1)(c)',
                citation: 'https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679',
                description: 'User email collected without explicit consent mechanism',
                mitigation: 'Add consent wrapper and data minimization check',
                file_path: filePath,
                line_start: undefined,
                line_end: undefined,
            });
        }
        // Check for GPL license issue
        const hasGpl = code.toLowerCase().includes('gpl');
        const hasLicense = code.toLowerCase().includes('license');
        if (hasGpl && !hasLicense) {
            risks.push({
                id: 'R002',
                severity: 'Critical',
                title: 'Potential GPL license contamination',
                law: 'GPL-3.0',
                citation: undefined,
                description: 'GPL-licensed code detected without proper license header',
                mitigation: 'Add license header or use permissive alternative',
                file_path: filePath,
                line_start: undefined,
                line_end: undefined,
            });
        }
        return {
            review_id: `mock-${Date.now()}`,
            commit_sha: undefined,
            timestamp: new Date().toISOString(),
            jurisdictions: ['US', 'EU'],
            domain: undefined,
            risks: risks,
            history: [],
            signature: undefined,
            metadata: {},
        };
    }
}
exports.LawModeClient = LawModeClient;
//# sourceMappingURL=client.js.map