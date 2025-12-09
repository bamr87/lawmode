import * as vscode from 'vscode';
import axios from 'axios';
import { ReviewResult, Severity } from './types';

export class LawModeClient {
    private async callLawModeAPI(code: string, filePath: string): Promise<ReviewResult> {
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
            
            return JSON.parse(stdout) as ReviewResult;
        } catch (error) {
            // Fallback: return mock data for MVP
            console.error('LawMode CLI error:', error);
            return this.getMockReview(code, filePath);
        }
    }

    async reviewCode(code: string, filePath: string): Promise<ReviewResult> {
        return this.callLawModeAPI(code, filePath);
    }

    private getMockReview(code: string, filePath: string): ReviewResult {
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
                severity: 'High' as Severity,
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
                severity: 'Critical' as Severity,
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

