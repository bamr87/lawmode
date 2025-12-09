"""SPDX license checker tool."""

import requests
from typing import Any, Dict, List

from lawmode.tools.base import LegalTool
from pydantic import BaseModel, Field


class SPDXInput(BaseModel):
    """Input schema for SPDX license tool."""

    license_name: str = Field(description="License identifier (e.g., 'MIT', 'GPL-3.0', 'Apache-2.0')")
    check_compatibility: bool = Field(default=False, description="Check compatibility with other licenses")


# Common license compatibility matrix
COMPATIBILITY_MATRIX: Dict[str, List[str]] = {
    "MIT": ["Apache-2.0", "BSD-3-Clause", "ISC", "MIT"],
    "Apache-2.0": ["Apache-2.0", "MIT", "BSD-3-Clause"],
    "GPL-3.0": ["GPL-3.0"],  # GPL is viral
    "GPL-2.0": ["GPL-2.0"],
    "LGPL-3.0": ["LGPL-3.0", "MIT", "Apache-2.0"],
    "BSD-3-Clause": ["MIT", "Apache-2.0", "BSD-3-Clause"],
    "ISC": ["MIT", "Apache-2.0", "ISC"],
}


def _create_spdx_tool() -> LegalTool:
    """Create SPDX license tool instance."""
    def _run(license_name: str, check_compatibility: bool = False) -> str:
        """Check SPDX license information."""
        try:
            # Normalize license name
            license_upper = license_name.upper().replace(" ", "-")
            
            result = f"SPDX License Check: {license_name}\n\n"
            
            # Check if it's a known SPDX license
            spdx_url = f"https://spdx.org/licenses/{license_upper}.html"
            
            # Determine license category
            if "GPL" in license_upper:
                result += "⚠️  WARNING: GPL licenses are copyleft/viral\n"
                result += "   - Requires derivative works to be GPL-licensed\n"
                result += "   - May contaminate proprietary code\n"
                result += "   - Consider LGPL or permissive alternatives\n\n"
            elif license_upper in ["MIT", "APACHE-2.0", "BSD-3-CLAUSE", "ISC"]:
                result += "✅ Permissive license - safe for commercial use\n\n"
            
            result += f"SPDX Identifier: {license_upper}\n"
            result += f"Reference: {spdx_url}\n"
            
            if check_compatibility:
                compatible = COMPATIBILITY_MATRIX.get(license_upper, [])
                if compatible:
                    result += f"\nCompatible licenses: {', '.join(compatible)}\n"
                else:
                    result += "\n⚠️  Compatibility check not available for this license\n"
            
            return result
        
        except Exception as e:
            return f"Error checking SPDX license: {str(e)}"
    
    from langchain_core.tools import StructuredTool
    return StructuredTool(
        name="spdx_license_check",
        description=(
            "Check SPDX license information, compatibility, and legal requirements. "
            "Use this to identify license conflicts, GPL contamination, and license compliance issues."
        ),
        args_schema=SPDXInput,
        func=_run,
    )


class SPDXLicenseTool:
    """Tool for checking SPDX licenses and compatibility."""
    
    def __new__(cls):
        return _create_spdx_tool()

