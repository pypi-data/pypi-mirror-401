from typing import List
from assumeless.core.models import Finding

MAGIC_TOKEN = "# assumeless: ignore"

class SuppressionFilter:
    """
    Handles inline suppression comments.
    Must be deterministic and resilient.
    """
    
    def apply(self, findings: List[Finding], source_lines: List[str]) -> List[Finding]:
        """
        Filter out findings that are suppressed on their line or the line above.
        """
        if not findings or not source_lines:
            return []
            
        active_findings = []
        for f in findings:
            if self._is_suppressed(f, source_lines):
                continue
            active_findings.append(f)
            
        return active_findings

    def _is_suppressed(self, f: Finding, lines: List[str]) -> bool:
        # Check current line (1-indexed input in Finding)
        line_idx = f.line_number - 1
        
        # Check current line (1-indexed input in Finding)
        line_idx = f.line_number - 1
        
        # Safety Check
        if line_idx < 0 or line_idx >= len(lines):
            return False

        # Case 1: Same line ignore
        if MAGIC_TOKEN in lines[line_idx]:
            return True
            
        # Case 2: Use on previous line
        if line_idx > 0:
            if MAGIC_TOKEN in lines[line_idx - 1]:
                return True
                
        return False
