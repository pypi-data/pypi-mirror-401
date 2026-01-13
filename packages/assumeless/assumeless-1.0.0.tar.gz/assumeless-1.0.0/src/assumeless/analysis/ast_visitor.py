import ast
from typing import List
from assumeless.core.models import Finding

class AnalysisVisitor(ast.NodeVisitor):
    """
    Base visitor for traversing Python ASTs to find assumption patterns.
    Specific strategies will inherit or compose with this.
    """
    def __init__(self, file_path: str, source_lines: List[str]):
        self.file_path = file_path
        self.source_lines = source_lines
        self.findings: List[Finding] = []
        self.current_scope: List[str] = [] # Stack of function/class names

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.current_scope.append(node.name)
        self.generic_visit(node)
        self.current_scope.pop()

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.current_scope.append(node.name)
        self.generic_visit(node)
        self.current_scope.pop()

    def add_finding(self, finding: Finding) -> None:
        self.findings.append(finding)

    def get_line_content(self, lineno: int) -> str:
        """Safe line retrieval (1-indexed input)"""
        if 1 <= lineno <= len(self.source_lines):
            return self.source_lines[lineno - 1].strip()
        return ""
