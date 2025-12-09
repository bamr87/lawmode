#!/usr/bin/env node
/**
 * Simple test script for LawMode extension mock functionality
 * Tests the mock review logic without requiring VSCode
 */

const fs = require('fs');
const path = require('path');

// Mock the getMockReview function logic
function getMockReview(code, filePath) {
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

// Test cases
const testFiles = [
    { file: 'test_files/test_gdpr.py', expectedRisks: 1, expectedSeverity: 'High' },
    { file: 'test_files/test_gpl.py', expectedRisks: 1, expectedSeverity: 'Critical' },
    { file: 'test_files/test_clean.py', expectedRisks: 0, expectedSeverity: null },
];

console.log('🧪 Testing LawMode Extension Mock Logic\n');

let passed = 0;
let failed = 0;

testFiles.forEach(({ file, expectedRisks, expectedSeverity }) => {
    const filePath = path.join(__dirname, file);
    
    if (!fs.existsSync(filePath)) {
        console.log(`❌ ${file}: File not found`);
        failed++;
        return;
    }
    
    const code = fs.readFileSync(filePath, 'utf8');
    const review = getMockReview(code, filePath);
    
    const actualRisks = review.risks.length;
    const actualSeverity = actualRisks > 0 ? review.risks[0].severity : null;
    
    const riskMatch = actualRisks === expectedRisks;
    const severityMatch = actualSeverity === expectedSeverity;
    
    if (riskMatch && severityMatch) {
        console.log(`✅ ${file}`);
        console.log(`   Found ${actualRisks} risk(s)`);
        if (actualRisks > 0) {
            console.log(`   Severity: ${actualSeverity}`);
            console.log(`   Title: ${review.risks[0].title}`);
        }
        passed++;
    } else {
        console.log(`❌ ${file}`);
        console.log(`   Expected: ${expectedRisks} risk(s), severity: ${expectedSeverity}`);
        console.log(`   Actual: ${actualRisks} risk(s), severity: ${actualSeverity}`);
        failed++;
    }
    console.log('');
});

console.log('='.repeat(50));
console.log(`Results: ${passed} passed, ${failed} failed`);

if (failed === 0) {
    console.log('✅ All tests passed!');
    process.exit(0);
} else {
    console.log('❌ Some tests failed');
    process.exit(1);
}

