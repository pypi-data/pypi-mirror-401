import enum
from dataclasses import dataclass, field
from typing import Set


class Invisibility(enum.Enum):
    """
    Measure of how difficult a risk is to spot during code review.
    """
    EXPLICIT = "EXPLICIT" # Plainly visible code (e.g., hardcoded path)
    IMPLICIT = "IMPLICIT" # Inferable from context
    HIDDEN = "HIDDEN"     # Requires knowledge of external state
    BURIED = "BURIED"     # Swallowed errors or deep dependency logic

class BlastRadius(enum.Enum):
    """
    Measure of the potential impact area if the assumption fails.
    """
    LOCAL = "LOCAL"       # Function scope
    MODULE = "MODULE"     # Module/Class scope
    SYSTEM = "SYSTEM"     # Application/Process scope
    DATA = "DATA"         # Persistence/Database scope (Critical)
    EXTERNAL = "EXTERNAL" # 3rd party API or Customer impact

class FailureMode(enum.Enum):
    """
    How the system manifests the failure when the assumption breaks.
    """
    CRASH = "CRASH"       # Unhandled exception
    HANG = "HANG"         # Resource exhaustion or loop
    SILENT = "SILENT"     # Logic proceeds with incorrect state
    BYPASS = "BYPASS"     # Security check skipped
    CORRUPTION = "CORRUPTION" # Data integrity loss

@dataclass
class Finding:
    """
    Represents a detected assumption pattern.
    This is an observation, not a verdict.
    """
    id: str
    file_path: str
    line_number: int
    content: str
    description: str
    
    # Core Diagnostics
    invisibility: Invisibility
    blast_radius: BlastRadius
    failure_mode: FailureMode
    
    # Debug/Context
    rule_name: str
    tags: Set[str] = field(default_factory=set)
    
    @property
    def location_str(self) -> str:
        return f"{self.file_path}:{self.line_number}"
