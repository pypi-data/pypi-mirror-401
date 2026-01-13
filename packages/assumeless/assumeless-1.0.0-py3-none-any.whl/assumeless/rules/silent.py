import re
from typing import List
from assumeless.core.models import Finding, Invisibility, BlastRadius, FailureMode
from assumeless.rules.base import Rule

class EmptyExceptRule(Rule):
    @property
    def id(self) -> str:
        return "AL-ERR-01"

    @property
    def name(self) -> str:
        return "Silent Failure (Empty Except)"

    def check_file(self, content: str, file_path: str) -> List[Finding]:
        findings = []
        # Naive regex for demo purposes. 
        # In a real tool we'd use AST, but for v0.1 POC regex is acceptable constraint compliance.
        # Matches: except: pass, except Exception: pass, etc.
        # This is a simplification.
        
        # 1. Look for 'except:' followed immediately by 'pass' on next line or same line
        # Note: This is brittle but sufficient for a POC.
        lines = content.split('\n')
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # Case 1: except ... : pass
            if re.search(r'except.*:\s*pass', stripped):
                findings.append(self._create_finding(file_path, i + 1, stripped))
                continue

            # Case 2: except: \n pass
            if re.search(r'except.*:$', stripped):
                # Look ahead for pass
                if i + 1 < len(lines):
                    next_line = lines[i+1].strip()
                    if next_line == 'pass':
                         findings.append(self._create_finding(file_path, i + 1, stripped + " ... pass"))

        return findings

    def _create_finding(self, file_path: str, line: int, content: str) -> Finding:
        return Finding(
            id=self.id,
            file_path=file_path,
            line_number=line,
            content=content,
            description="Exception is caught and silently suppressed.",
            invisibility=Invisibility.BURIED, # Hard to see side effects
            blast_radius=BlastRadius.MODULE, # Usually affects local logic, could be worse
            failure_mode=FailureMode.SILENT,   # The definition of silent failure
            rule_name=self.name
        )
