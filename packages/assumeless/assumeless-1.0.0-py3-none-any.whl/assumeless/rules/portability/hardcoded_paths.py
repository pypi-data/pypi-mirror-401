import ast
import re
from typing import List, Type
from assumeless.rules.ast_rule import ASTRule
from assumeless.analysis.ast_visitor import AnalysisVisitor
from assumeless.core.models import Finding, Invisibility, BlastRadius, FailureMode

class HardcodedPathRule(ASTRule):
    id = "AL-PATH-01"
    name = "Hardcoded Absolute Path"
        
    def subscribe(self) -> List[Type[ast.AST]]:
        return [ast.Constant]

    def visit(self, node: ast.AST, visitor: AnalysisVisitor) -> None:
        if isinstance(node, ast.Constant):
            if isinstance(node.value, str):
                if self._is_absolute_path(node.value):
                    visitor.add_finding(Finding(
                        id=self.id,
                        file_path=visitor.file_path,
                        line_number=node.lineno,
                        content=visitor.get_line_content(node.lineno),
                        description="Hardcoded absolute path limits portability.",
                        invisibility=Invisibility.EXPLICIT,
                        blast_radius=BlastRadius.SYSTEM,
                        failure_mode=FailureMode.CRASH,
                        rule_name=self.name
                    ))

    def _is_absolute_path(self, text: str) -> bool:
        if text.startswith("/") and len(text) > 2 and "/" in text[1:]:
             if not any(c.isspace() for c in text):
                 return True
        if re.match(r'[a-zA-Z]:\\[a-zA-Z0-9_\\]+', text):
            return True
        return False
