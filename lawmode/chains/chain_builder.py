"""Build the 8-chain legal reasoning pipeline."""

from typing import Any, Dict, List

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END

from lawmode.llm import LLMBackend
from lawmode.tools import (
    EurLexTool,
    CourtListenerTool,
    SPDXLicenseTool,
    GoogleScholarTool,
)


class ChainState(Dict[str, Any]):
    """State passed between chains."""

    pass


def build_lawmode_chains(llm_backend: LLMBackend) -> StateGraph:
    """Build the 8-chain legal reasoning pipeline."""
    
    # Initialize tools
    tools = [
        EurLexTool(),
        CourtListenerTool(),
        SPDXLicenseTool(),
        GoogleScholarTool(),
    ]
    
    # Bind tools to LLM for forced tool use
    llm_with_tools = llm_backend.model.bind_tools(tools)
    
    # Build the graph
    workflow = StateGraph(ChainState)
    
    # Chain 1: Jurisdiction Detection
    workflow.add_node("detect_jurisdiction", _detect_jurisdiction_chain(llm_with_tools))
    
    # Chain 2: Domain Detection
    workflow.add_node("detect_domain", _detect_domain_chain(llm_with_tools))
    
    # Chain 3: Privacy Compliance (GDPR, CCPA)
    workflow.add_node("privacy_compliance", _privacy_compliance_chain(llm_with_tools))
    
    # Chain 4: License Compliance
    workflow.add_node("license_compliance", _license_compliance_chain(llm_with_tools))
    
    # Chain 5: Security & Export Control
    workflow.add_node("security_compliance", _security_compliance_chain(llm_with_tools))
    
    # Chain 6: Accessibility (WCAG)
    workflow.add_node("accessibility_compliance", _accessibility_compliance_chain(llm_with_tools))
    
    # Chain 7: Copyright & IP
    workflow.add_node("copyright_check", _copyright_check_chain(llm_with_tools))
    
    # Chain 8: Regulatory Domain-Specific
    workflow.add_node("regulatory_compliance", _regulatory_compliance_chain(llm_with_tools))
    
    # Set entry point
    workflow.set_entry_point("detect_jurisdiction")
    
    # Define execution flow
    workflow.add_edge("detect_jurisdiction", "detect_domain")
    workflow.add_edge("detect_domain", "privacy_compliance")
    workflow.add_edge("privacy_compliance", "license_compliance")
    workflow.add_edge("license_compliance", "security_compliance")
    workflow.add_edge("security_compliance", "accessibility_compliance")
    workflow.add_edge("accessibility_compliance", "copyright_check")
    workflow.add_edge("copyright_check", "regulatory_compliance")
    workflow.add_edge("regulatory_compliance", END)
    
    return workflow.compile()


def _detect_jurisdiction_chain(llm):
    """Chain 1: Detect applicable jurisdictions."""
    def chain(state: ChainState) -> ChainState:
        code = state.get("code", "")
        prompt = f"""Analyze the following code and detect applicable legal jurisdictions.

Code:
{code}

Identify jurisdictions based on:
- User location indicators (IP geolocation, address fields)
- Data processing locations (server regions, cloud providers)
- Business entity locations (company registration, tax IDs)
- Explicit jurisdiction mentions

Return JSON with jurisdictions array: {{"jurisdictions": ["US-CA", "EU", "UK"]}}
"""
        
        messages = [
            SystemMessage(content="You are a legal jurisdiction detection expert."),
            HumanMessage(content=prompt),
        ]
        
        response = llm.invoke(messages)
        # Handle both string and message content
        if hasattr(response, 'content'):
            state["jurisdiction_analysis"] = response.content
        else:
            state["jurisdiction_analysis"] = str(response)
        return state
    
    return chain


def _detect_domain_chain(llm):
    """Chain 2: Detect industry domain."""
    def chain(state: ChainState) -> ChainState:
        code = state.get("code", "")
        prompt = f"""Analyze the following code and detect the industry domain.

Code:
{code}

Identify domain based on:
- API integrations (payment processors → fintech)
- Medical data handling → healthcare
- Educational content → edtech
- E-commerce features → retail/commerce

Return JSON: {{"domain": "fintech"}}
"""
        
        messages = [
            SystemMessage(content="You are an industry domain detection expert."),
            HumanMessage(content=prompt),
        ]
        
        response = llm.invoke(messages)
        # Handle both string and message content
        if hasattr(response, 'content'):
            state["domain_analysis"] = response.content
        else:
            state["domain_analysis"] = str(response)
        return state
    
    return chain


def _privacy_compliance_chain(llm):
    """Chain 3: Privacy compliance (GDPR, CCPA, PIPEDA)."""
    def chain(state: ChainState) -> ChainState:
        code = state.get("code", "")
        jurisdictions = state.get("jurisdiction_analysis", "")
        
        prompt = f"""Analyze privacy compliance risks in the following code.

Code:
{code}
Jurisdictions: {jurisdictions}

Check for:
- GDPR violations (Art. 5, 6, 32): data minimization, consent, encryption
- CCPA violations: consumer rights, opt-out mechanisms
- PIPEDA violations: consent, purpose limitation
- PII transmission without encryption
- Missing consent mechanisms
- Excessive data collection

Use EUR-Lex tool to cite specific GDPR articles.
Return structured risk analysis.
"""
        
        messages = [
            SystemMessage(content="You are a privacy law compliance expert. Always use tools to cite legal sources."),
            HumanMessage(content=prompt),
        ]
        
        response = llm.invoke(messages)
        # Handle both string and message content
        if hasattr(response, 'content'):
            state["privacy_risks"] = response.content
        else:
            state["privacy_risks"] = str(response)
        return state
    
    return chain


def _license_compliance_chain(llm):
    """Chain 4: License compliance (GPL, SPDX)."""
    def chain(state: ChainState) -> ChainState:
        code = state.get("code", "")
        
        prompt = f"""Analyze license compliance risks in the following code.

Code:
{code}

Check for:
- GPL contamination (viral licenses in proprietary code)
- Missing license headers
- License incompatibilities
- Unlicensed third-party code

Use SPDX tool to check license compatibility.
Return structured risk analysis.
"""
        
        messages = [
            SystemMessage(content="You are a software license compliance expert. Always use SPDX tool for license checks."),
            HumanMessage(content=prompt),
        ]
        
        response = llm.invoke(messages)
        # Handle both string and message content
        if hasattr(response, 'content'):
            state["license_risks"] = response.content
        else:
            state["license_risks"] = str(response)
        return state
    
    return chain


def _security_compliance_chain(llm):
    """Chain 5: Security & export control (OWASP, EAR/ITAR)."""
    def chain(state: ChainState) -> ChainState:
        code = state.get("code", "")
        
        prompt = f"""Analyze security compliance risks in the following code.

Code:
{code}

Check for:
- OWASP Top 10 vulnerabilities
- Export control violations (EAR/ITAR) - encryption algorithms
- Insecure authentication
- SQL injection risks
- XSS vulnerabilities
- Missing security headers

Return structured risk analysis.
"""
        
        messages = [
            SystemMessage(content="You are a security compliance expert."),
            HumanMessage(content=prompt),
        ]
        
        response = llm.invoke(messages)
        # Handle both string and message content
        if hasattr(response, 'content'):
            state["security_risks"] = response.content
        else:
            state["security_risks"] = str(response)
        return state
    
    return chain


def _accessibility_compliance_chain(llm):
    """Chain 6: Accessibility compliance (WCAG)."""
    def chain(state: ChainState) -> ChainState:
        code = state.get("code", "")
        
        prompt = f"""Analyze accessibility compliance risks in the following code.

Code:
{code}

Check for WCAG 2.1 violations:
- Missing alt text on images
- Missing ARIA labels
- Keyboard navigation issues
- Color contrast problems
- Missing form labels

Return structured risk analysis.
"""
        
        messages = [
            SystemMessage(content="You are an accessibility compliance expert."),
            HumanMessage(content=prompt),
        ]
        
        response = llm.invoke(messages)
        # Handle both string and message content
        if hasattr(response, 'content'):
            state["accessibility_risks"] = response.content
        else:
            state["accessibility_risks"] = str(response)
        return state
    
    return chain


def _copyright_check_chain(llm):
    """Chain 7: Copyright & IP infringement."""
    def chain(state: ChainState) -> ChainState:
        code = state.get("code", "")
        
        prompt = f"""Analyze copyright and IP risks in the following code.

Code:
{code}

Check for:
- Copied code snippets without attribution
- Potential copyright infringement
- Missing copyright notices
- Trademark usage issues

Use Google Scholar tool for precedent research if needed.
Return structured risk analysis.
"""
        
        messages = [
            SystemMessage(content="You are a copyright and IP law expert."),
            HumanMessage(content=prompt),
        ]
        
        response = llm.invoke(messages)
        # Handle both string and message content
        if hasattr(response, 'content'):
            state["copyright_risks"] = response.content
        else:
            state["copyright_risks"] = str(response)
        return state
    
    return chain


def _regulatory_compliance_chain(llm):
    """Chain 8: Domain-specific regulatory compliance."""
    def chain(state: ChainState) -> ChainState:
        code = state.get("code", "")
        domain = state.get("domain_analysis", "")
        
        prompt = f"""Analyze domain-specific regulatory compliance risks.

Code:
{code}
Domain: {domain}

Check for industry-specific regulations:
- Fintech: PCI-DSS, SOX, MiFID II
- Healthcare: HIPAA, HITECH
- Education: FERPA, COPPA
- General: Industry-specific data handling requirements

Use legal research tools to cite specific regulations.
Return structured risk analysis.
"""
        
        messages = [
            SystemMessage(content="You are a regulatory compliance expert. Always use tools to cite regulations."),
            HumanMessage(content=prompt),
        ]
        
        response = llm.invoke(messages)
        # Handle both string and message content
        if hasattr(response, 'content'):
            state["regulatory_risks"] = response.content
        else:
            state["regulatory_risks"] = str(response)
        return state
    
    return chain

