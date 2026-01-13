import ast
from typing import List, Type
from assumeless.rules.ast_rule import ASTRule
from assumeless.analysis.ast_visitor import AnalysisVisitor
from assumeless.core.models import Finding, Invisibility, BlastRadius, FailureMode

class EnvVarRule(ASTRule):
    id = "AL-ENV-01"
    name = "Direct os.environ Access"
        
    def subscribe(self) -> List[Type[ast.AST]]:
        return [ast.Subscript]

    def visit(self, node: ast.AST, visitor: AnalysisVisitor) -> None:
        if isinstance(node, ast.Subscript):
            if self._is_os_environ(node.value):
                line_content = visitor.get_line_content(node.lineno)
                
                visitor.add_finding(Finding(
                    id=self.id,
                    file_path=visitor.file_path,
                    line_number=node.lineno,
                    content=line_content,
                    description="Direct access to environment variable assumes it exists.",
                    invisibility=Invisibility.IMPLICIT,
                    blast_radius=BlastRadius.SYSTEM, 
                    failure_mode=FailureMode.CRASH, 
                    rule_name=self.name
                ))

    def _is_os_environ(self, node: ast.AST) -> bool:
        if isinstance(node, ast.Attribute):
            if node.attr == "environ":
               if isinstance(node.value, ast.Name) and node.value.id == "os":
                   return True
        return False
