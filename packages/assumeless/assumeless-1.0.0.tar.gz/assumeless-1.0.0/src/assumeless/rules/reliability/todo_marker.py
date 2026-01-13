import ast
from typing import List, Type
from assumeless.rules.ast_rule import ASTRule
from assumeless.analysis.ast_visitor import AnalysisVisitor
from assumeless.core.models import Finding, BlastRadius, Invisibility, FailureMode

class TODORule(ASTRule):
    id = "AL-LOGIC-04"
    name = "TODO Left in Code"
    
    def subscribe(self) -> List[Type[ast.AST]]:
        # TODOs are not AST nodes, they are comments. But we can access lines.
        # We can implement this by hooking into the Visitor initialization or 
        # scanning lines manually if we had a "File" subscriber.
        # Since we don't have a "File" node in standard AST traverse easily without Module...
        # We subscribe to Module.
        return [ast.Module]

    def visit(self, node: ast.AST, visitor: AnalysisVisitor) -> None:
        """
        Scans all lines for 'TODO'.
        """
        if not isinstance(node, ast.Module):
            return

        for i, line in enumerate(visitor.source_lines, 1):
            if "TODO" in line:
                # Basic check, might be in string literal but v1.0 philosophy is "AssumeLess" -> Report it.
                visitor.add_finding(Finding(
                    id=self.id,
                    file_path=visitor.file_path,
                    line_number=i,
                    content=line.strip(),
                    description="TODO marker detected in code",
                    blast_radius=BlastRadius.LOCAL,
                    invisibility=Invisibility.EXPLICIT, 
                    failure_mode=FailureMode.BYPASS, # Often implies unfinished logic
                    rule_name=self.name
                ))
