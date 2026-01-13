import os
import toml
from typing import List
from dataclasses import dataclass, field

DEFAULT_CONFIG_FILENAME = "assumeless.toml"

@dataclass
class Config:
    """
    v1.0 Configuration Contract.
    Values here are immutable during a scan.
    """
    ignore_paths: List[str] = field(default_factory=list)
    ignore_rules: List[str] = field(default_factory=list)
    max_findings: int = 5
    enable_cache: bool = False
    
    @classmethod
    def load(cls, root_path: str = ".") -> 'Config':
        config_path = os.path.join(root_path, DEFAULT_CONFIG_FILENAME)
        
        if not os.path.exists(config_path):
             # print(f"DEBUG: Config not found at {config_path}")
             return cls()

        try:
            with open(config_path, "r") as f:
                data = toml.load(f)
            
            tool_config = data.get("tool", {}).get("assumeless", {})
                        
            return cls(
                ignore_paths=tool_config.get("ignore_paths", []),
                ignore_rules=tool_config.get("ignore_rules", []),
                max_findings=tool_config.get("max_findings", 5),
                enable_cache=tool_config.get("enable_cache", False)
            )
        except Exception as e:
            print(f"DEBUG: Config error: {e}")
            return cls()
