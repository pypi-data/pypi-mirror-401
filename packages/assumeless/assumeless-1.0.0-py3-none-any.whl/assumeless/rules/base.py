from abc import ABC, abstractmethod
from typing import List
from assumeless.core.models import Finding

class Rule(ABC):
    """
    Base class for all assumption detection rules.
    Rules MUST NOT assign judgments or severity.
    They only assist in creating findings with objective signals.
    """
    
    @property
    @abstractmethod
    def id(self) -> str:
        """Stable unique identifier for the rule (e.g. SUB-01)"""
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Human readable name of the rule"""
        pass

    @abstractmethod
    def check_file(self, content: str, file_path: str) -> List[Finding]:
        """
        Analyze a file pattern and return findings.
        Args:
            content: The full text content of the file.
            file_path: Relative path to the file.
        Returns:
            List[Finding]: Observable assumptions.
        """
        pass
