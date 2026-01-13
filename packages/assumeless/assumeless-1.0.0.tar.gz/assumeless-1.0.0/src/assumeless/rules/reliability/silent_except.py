import ast
from typing import List, Type
from assumeless.rules.ast_rule import ASTRule
from assumeless.analysis.ast_visitor import AnalysisVisitor
from assumeless.core.models import Finding, Invisibility, BlastRadius, FailureMode

class SilentExceptionRule(ASTRule):
    id = "AL-ERR-01"
    name = "Silent Exception (Pass)"
        
    def subscribe(self) -> List[Type[ast.AST]]:
        return [ast.Try]

    def visit(self, node: ast.AST, visitor: AnalysisVisitor) -> None:
        # node is guaranteed to be ast.Try
        if isinstance(node, ast.Try):
            for handler in node.handlers:
                if self._is_empty_or_pass(handler.body):
                    line_content = visitor.get_line_content(handler.lineno)
                    
                    f = Finding(
                        id=self.id,
                        file_path=visitor.file_path,
                        line_number=handler.lineno,
                        content=line_content,
                        description="Exception block suppresses errors without logging or fallback.",
                        invisibility=Invisibility.BURIED,
                        blast_radius=BlastRadius.MODULE,
                        failure_mode=FailureMode.SILENT,
                        rule_name=self.name
                    )
                    visitor.add_finding(f)

    def _is_empty_or_pass(self, body: list[ast.stmt]) -> bool:
        if not body:
            return True
        if len(body) == 1:
            node = body[0]
            if isinstance(node, ast.Pass):
                return True
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant):
                 if node.value.value is Ellipsis: 
                     return True
        return False
