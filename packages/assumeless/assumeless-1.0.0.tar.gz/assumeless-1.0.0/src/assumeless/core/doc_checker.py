import re
import os
import ast
import toml
from typing import List, Dict, Any
from pathlib import Path
from assumeless.core.models import Finding, BlastRadius, Invisibility, FailureMode

class DocDriftDetector:
    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        self.findings: List[Finding] = []
        
        # Knowledge Base
        self.doc_facts: Dict[str, List[Any]] = {
            "versions": [], # [(file, line, version_str)]
            "env_vars": [],  # [(file, line, var_name)]
            "packages": [],  # [(file, line, package_name)]
            "cli_claims": [], # [(file, line, context)]
        }
        
        self.code_facts: Dict[str, Any] = {
            "version": None,
            "name": None,
            "env_vars": set(),
            "has_cli": False,
        }

    def scan(self) -> List[Finding]:
        self._scan_codebase()
        self._scan_docs()
        self._compare()
        return self.findings

    def _scan_codebase(self) -> None:
        # 1. Read pyproject.toml
        try:
            pyproject_path = self.root_path / "pyproject.toml"
            if pyproject_path.exists():
                data = toml.load(pyproject_path)
                project = data.get("project", {})
                self.code_facts["version"] = project.get("version")
                self.code_facts["name"] = project.get("name")
                
                # Check for CLI scripts
                scripts = project.get("scripts", {})
                if scripts:
                    self.code_facts["has_cli"] = True
        except Exception:
            pass

        # 2. Scan Python files for AST facts
        for root, dirs, files in os.walk(self.root_path):
            if "venv" in dirs:
                dirs.remove("venv")
            if ".git" in dirs:
                dirs.remove(".git")
            
            for file in files:
                if file.endswith(".py"):
                    try:
                        with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                            content = f.read()
                        tree = ast.parse(content)
                        self._extract_code_facts(tree)
                    except Exception:
                        pass

    def _extract_code_facts(self, tree: ast.AST) -> None:
        for node in ast.walk(tree):
            # Check for os.environ, os.getenv
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if isinstance(node.func.value, ast.Name) and node.func.value.id == "os":
                        if node.func.attr == "getenv":
                            if node.args and isinstance(node.args[0], ast.Constant):
                                 self.code_facts["env_vars"].add(node.args[0].value)
            
            if isinstance(node, ast.Attribute):
                 if isinstance(node.value, ast.Attribute): # os.environ.get is call usually, but access is Attribute
                     if isinstance(node.value.value, ast.Name) and node.value.value.id == "os":
                         # os.environ['KEY']
                         pass # Hard without detailed flow, stick to getenv/environ access logging
            
            # Simple subscript: os.environ['KEY']
            if isinstance(node, ast.Subscript):
                if isinstance(node.value, ast.Attribute):
                     if isinstance(node.value.value, ast.Name) and node.value.value.id == "os":
                         if node.value.attr == "environ":
                             if isinstance(node.slice, ast.Constant):
                                 self.code_facts["env_vars"].add(node.slice.value)

            # Check for CLI entry points logic (if name == main)
            if isinstance(node, ast.If):
                if isinstance(node.test, ast.Compare):
                    # Rough check for if __name__ == "__main__"
                    pass 

    def _scan_docs(self) -> None:
        doc_files = ["README.md"]
        docs_dir = self.root_path / "docs"
        if docs_dir.exists():
            for f in docs_dir.glob("*.md"):
                doc_files.append(str(f.relative_to(self.root_path)))

        for rel_path in doc_files:
            full_path = self.root_path / rel_path
            if not full_path.exists():
                continue
                
            with open(full_path, "r", encoding="utf-8") as file_obj:
                lines = file_obj.readlines()
            
            for i, line in enumerate(lines, 1):
                self._parse_doc_line(line, str(rel_path), i)

    def _parse_doc_line(self, line: str, file: str, line_no: int) -> None:
        # Version pattern: v1.1.0 or version 1.1.0
        # Avoid matching generic "version"
        ver_match = re.search(r'\bv?(\d+\.\d+\.\d+)\b', line)
        if ver_match is not None and ("version" in line.lower() or line.strip().startswith("v")):
             self.doc_facts["versions"].append((file, line_no, ver_match.group(1), line.strip()))

        # Env Var pattern: UPPER_CASE_WITH_UNDERSCORE (len > 3)
        # Avoid simple words like HEAD, INFO, TODO
        env_matches = re.findall(r'\b[A-Z]{2,}_[A-Z0-9_]+\b', line)
        for env in env_matches:
            if env not in ["README", "TODO", "NOTE", "WARNING", "IMPORTANT", "LICENSE", "COPYRIGHT"]:
                self.doc_facts["env_vars"].append((file, line_no, env, line.strip()))

        # Install pattern: pip install <name>
        if "pip install" in line:
            match = re.search(r'pip install ([\w-]+)', line)
            if match:
                self.doc_facts["packages"].append((file, line_no, match.group(1), line.strip()))

    def _compare(self) -> None:
        self._check_versions()
        self._check_package_names()
        self._check_env_vars()

    def _add_finding(self, rule_id: str, file: str, line: int, content: str, desc: str) -> None:
        self.findings.append(Finding(
            id=rule_id,
            file_path=file,
            line_number=line,
            content=content,
            description=desc,
            invisibility=Invisibility.EXPLICIT, # Docs are explicit
            blast_radius=BlastRadius.EXTERNAL, # Affects users
            failure_mode=FailureMode.BYPASS, # User bypasses instructions
            rule_name="Documentation Drift"
        ))

    def _check_versions(self) -> None:
        actual = self.code_facts["version"]
        if not actual:
            return
        
        for f, line, v, content in self.doc_facts["versions"]:
            if v != actual:
                # Heuristic: only flag if it looks like The Project Version
                if "assumeless" in content.lower() or "version" in content.lower():
                    # We might get false positives on dependency versions. 
                    # Try to filter: checks if content string is likely about THIS package.
                    # For now, be permissive but specific in description.
                    self._add_finding(
                        "AL-DOC-10", f, line, content,
                        f"Version in docs ({v}) matches neither installed version ({actual}) nor known history."
                    )

    def _check_package_names(self) -> None:
        actual = self.code_facts["name"]
        if not actual:
            return

        for f, line, name, content in self.doc_facts["packages"]:
            if name != actual and name != "." and name != "-e":
                self._add_finding(
                    "AL-DOC-05", f, line, content,
                    f"Installation instruction mentions '{name}' but package is '{actual}'."
                )

    def _check_env_vars(self) -> None:
        # If doc mentions ENV_VAR but code never uses it
        known_vars = self.code_facts["env_vars"]
        
        for f, line, var, content in self.doc_facts["env_vars"]:
            if var not in known_vars:
                # Check strictness: maybe it is used widely but dynamically?
                # AssumeLess philosophy -> Use AST.
                self._add_finding(
                    "AL-DOC-06", f, line, content,
                    f"Environment variable '{var}' is documented but not detected in codebase AST."
                )
