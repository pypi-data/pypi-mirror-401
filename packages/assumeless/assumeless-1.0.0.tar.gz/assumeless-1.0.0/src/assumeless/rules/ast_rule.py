from abc import ABC, abstractmethod
from typing import List, Type
import ast


from assumeless.analysis.ast_visitor import AnalysisVisitor

class ASTRule(ABC):
    """
    v1.0 AST Rule Interface.
    Rules subscribe to node types and are visited by the central dispatcher.
    """
    
    @property
    @abstractmethod
    def id(self) -> str:
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def subscribe(self) -> List[Type[ast.AST]]:
        """
        Return a list of AST Node types this rule cares about.
        e.g. [ast.Try, ast.FunctionDef]
        """
        pass

    @abstractmethod
    def visit(self, node: ast.AST, visitor: AnalysisVisitor) -> None:
        """
        Analyze a specific node.
        This rule MUST NOT walk the tree further specific to traversal logic.
        """
        pass
