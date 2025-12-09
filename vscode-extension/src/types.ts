export type Severity = 'Critical' | 'High' | 'Medium' | 'Low';

export interface Risk {
    id: string;
    severity: Severity;
    title: string;
    law: string;
    citation?: string;
    description: string;
    mitigation: string;
    file_path?: string;
    line_start?: number;
    line_end?: number;
    code_snippet?: string;
}

export interface ReviewResult {
    review_id: string;
    commit_sha?: string;
    timestamp: string;
    jurisdictions: string[];
    domain?: string;
    risks: Risk[];
    history: string[];
    signature?: string;
    metadata: Record<string, any>;
}

