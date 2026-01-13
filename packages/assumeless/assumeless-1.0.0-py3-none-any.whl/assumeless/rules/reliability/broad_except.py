import ast
from typing import List, Type
from assumeless.rules.ast_rule import ASTRule
from assumeless.analysis.ast_visitor import AnalysisVisitor
from assumeless.core.models import Finding, BlastRadius, Invisibility, FailureMode

class BroadExceptionRule(ASTRule):
    id = "AL-ERR-02"
    name = "Broad Exception Catch"
    
    def subscribe(self) -> List[Type[ast.AST]]:
        return [ast.ExceptHandler]

    def visit(self, node: ast.AST, visitor: AnalysisVisitor) -> None:
        """
        Detects `except Exception:` or bare `except:`.
        """
        if not isinstance(node, ast.ExceptHandler):
            return

        is_broad = False
        if node.type is None:
            # Bare exception
            is_broad = True
        elif isinstance(node.type, ast.Name) and node.type.id == "Exception":
            is_broad = True
            
        if is_broad:
             visitor.add_finding(Finding(
                id=self.id,
                file_path=visitor.file_path,
                line_number=node.lineno,
                content=visitor.get_line_content(node.lineno),
                description="Broad exception handling detected",
                blast_radius=BlastRadius.MODULE,
                invisibility=Invisibility.IMPLICIT, 
                failure_mode=FailureMode.SILENT,
                rule_name=self.name
            ))
