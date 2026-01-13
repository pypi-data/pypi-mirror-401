import unittest
import ast
from assumeless.analysis.ast_visitor import AnalysisVisitor
from assumeless.rules.reliability.mutable_defaults import MutableDefaultRule
from assumeless.rules.reliability.unclosed_files import UnclosedFileRule

class TestNewRules(unittest.TestCase):
    def test_mutable_default(self):
        code = """
def bad(a=[]):
    pass
def good(a=None):
    pass
"""
        tree = ast.parse(code)
        visitor = AnalysisVisitor("test.py", code.splitlines())
        rule = MutableDefaultRule()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                rule.visit(node, visitor)
        
        self.assertEqual(len(visitor.findings), 1)
        self.assertEqual(visitor.findings[0].id, "AL-GLOB-07")

    def test_unclosed_file(self):
        code = """
def risky():
    f = open("file.txt")
    
def safe():
    with open("file.txt") as f:
        pass
"""
        tree = ast.parse(code)
        visitor = AnalysisVisitor("test.py", code.splitlines())
        rule = UnclosedFileRule()
        
        for node in ast.walk(tree):
            # Dispatch manually for test
            if isinstance(node, ast.Assign):
                 rule.visit(node, visitor)
        
        self.assertEqual(len(visitor.findings), 1)
        self.assertEqual(visitor.findings[0].id, "AL-PATH-08")
        self.assertIn("Direct usage of 'open()'", visitor.findings[0].description)

if __name__ == '__main__':
    unittest.main()
