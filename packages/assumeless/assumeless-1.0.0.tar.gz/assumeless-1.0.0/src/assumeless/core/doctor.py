from typing import List
from assumeless.core.models import Finding, Invisibility, BlastRadius, FailureMode

class CodeDoctor:
    """
    Decides which findings are important enough to show.
    """
    def examine(self, findings: List[Finding]) -> List[Finding]:
        # 1. Deduplicate by hash of (id + line) to prevent noise
        unique_findings = {f"{f.id}:{f.line_number}": f for f in findings}.values()
        
        scored = []
        for f in unique_findings:
            score = self._calculate_toxicity(f)
            if score > 0: # Filter out trivial issues
                scored.append((score, f))
        
        # Sort desc
        scored.sort(key=lambda x: x[0], reverse=True)
        
        # Return top 2
        return [x[1] for x in scored[:2]]

    def _calculate_toxicity(self, f: Finding) -> int:
        score = 0
        
        # Impact Baseline
        if f.blast_radius == BlastRadius.DATA:
            score += 100
        elif f.blast_radius == BlastRadius.SYSTEM:
            score += 50
        elif f.blast_radius == BlastRadius.MODULE:
            score += 20
        
        # Stealth Multiplier
        if f.invisibility == Invisibility.BURIED:
            score += 40
        elif f.invisibility == Invisibility.HIDDEN:
            score += 30
        
        # Mode Modifier
        if f.failure_mode == FailureMode.SILENT:
            score += 25
        if f.failure_mode == FailureMode.CORRUPTION:
            score += 50

        # Heuristic Combinations
        # A hidden system dependency is very bad (e.g. Env var hidden deep)
        if f.blast_radius == BlastRadius.SYSTEM and f.invisibility in (Invisibility.IMPLICIT, Invisibility.HIDDEN):
            score += 30

        # A silent data corruption is the worst possible bug
        if f.failure_mode == FailureMode.CORRUPTION and f.invisibility == Invisibility.BURIED:
            score += 200

        return score
