import ast
from typing import List, Type
from assumeless.rules.ast_rule import ASTRule
from assumeless.analysis.ast_visitor import AnalysisVisitor
from assumeless.core.models import Finding, BlastRadius, Invisibility, FailureMode

class UnclosedFileRule(ASTRule):
    id = "AL-PATH-08"
    name = "Unclosed File Handle"
    
    def subscribe(self) -> List[Type[ast.AST]]:
        # We listen for Assignments to catch `f = open(...)`
        return [ast.Assign]

    def visit(self, node: ast.AST, visitor: AnalysisVisitor) -> None:
        """
        Detects `f = open(...)` which suggests missing context manager.
        """
        if not isinstance(node, ast.Assign):
            return

        if isinstance(node.value, ast.Call):
            if isinstance(node.value.func, ast.Name):
                if node.value.func.id == "open":
                    # Found `x = open(...)`
                    visitor.add_finding(Finding(
                        id=self.id,
                        file_path=visitor.file_path,
                        line_number=node.lineno,
                        content=visitor.get_line_content(node.lineno),
                        description="Direct usage of 'open()' in assignment",
                        blast_radius=BlastRadius.SYSTEM,
                        invisibility=Invisibility.IMPLICIT,
                        failure_mode=FailureMode.SILENT,
                        rule_name="UnclosedFileRule"
                    ))
