import re
from typing import List
from assumeless.core.models import Finding, Invisibility, BlastRadius, FailureMode
from assumeless.rules.base import Rule

class HardcodedPathRule(Rule):
    @property
    def id(self) -> str:
        return "AL-ENV-01"

    @property
    def name(self) -> str:
        return "Hardcoded Absolute Path"

    def check_file(self, content: str, file_path: str) -> List[Finding]:
        findings = []
        lines = content.split('\n')
        # Regex for Windows or Unix absolute paths in strings
        # e.g. "C:\Users", "/home/user", "/var/log"
        # Avoid imports or weak matches.
        
        # Matches typical linux absolute paths inside quotes
        unix_path_pattern = r'[\'"]/[a-zA-Z0-9_]+/[a-zA-Z0-9_/]+[\'"]'
        # Matches typical windows absolute paths inside quotes
        win_path_pattern = r'[\'"][a-zA-Z]:\\[a-zA-Z0-9_\\]+[\'"]'

        for i, line in enumerate(lines):
            if re.search(unix_path_pattern, line) or re.search(win_path_pattern, line):
                # Exclude imports
                if line.strip().startswith("import") or line.strip().startswith("from"):
                    continue

                findings.append(Finding(
                    id=self.id,
                    file_path=file_path,
                    line_number=i+1,
                    content=line.strip(),
                    description="Hardcoded absolute file system path detected.",
                    invisibility=Invisibility.EXPLICIT, # It's right there in the code
                    blast_radius=BlastRadius.SYSTEM,  # Breaks on different machines/deployments
                    failure_mode=FailureMode.CRASH,    # FileNotFoundError
                    rule_name=self.name
                ))
        return findings
