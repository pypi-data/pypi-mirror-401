import ast
from typing import List, Type
from assumeless.rules.ast_rule import ASTRule
from assumeless.analysis.ast_visitor import AnalysisVisitor
from assumeless.core.models import Finding, BlastRadius, Invisibility, FailureMode

class MutableDefaultRule(ASTRule):
    id = "AL-GLOB-07"
    name = "Mutable Default Argument"
    
    def subscribe(self) -> List[Type[ast.AST]]:
        return [ast.FunctionDef]

    def visit(self, node: ast.AST, visitor: AnalysisVisitor) -> None:
        """
        Detects mutable default arguments (list, dict, set).
        Example: def foo(x=[]): ...
        """
        if not isinstance(node, ast.FunctionDef):
            return

        for default in node.args.defaults:
            is_mutable = False
            if isinstance(default, ast.List):
                is_mutable = True
            elif isinstance(default, ast.Dict):
                is_mutable = True
            elif isinstance(default, ast.Set):
                is_mutable = True
            # Note: We don't check for custom objects instantiated here, mostly literals.
            
            if is_mutable:
                visitor.add_finding(Finding(
                    id=self.id,
                    file_path=visitor.file_path,
                    line_number=node.lineno,
                    content=visitor.get_line_content(node.lineno),
                    description="Mutable default argument detected",
                    blast_radius=BlastRadius.MODULE,
                    invisibility=Invisibility.IMPLICIT, 
                    failure_mode=FailureMode.CORRUPTION,
                    rule_name="MutableDefaultRule"
                ))
