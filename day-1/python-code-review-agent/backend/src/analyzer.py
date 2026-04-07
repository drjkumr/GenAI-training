import ast
import json
import sys

def analyze_python_code(code: str) -> dict:
    """
    Analyze Python code using AST for structural issues and patterns.
    Returns findings as JSON to stdout for Node.js to parse.
    """
    findings = {
        "syntax_valid": True,
        "errors": [],
        "functions": [],
        "imports": [],
        "classes": [],
        "issues": []
    }
    
    # Step 1: Check syntax validity
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        findings["syntax_valid"] = False
        findings["errors"].append({
            "type": "SyntaxError",
            "line": e.lineno or 0,
            "message": str(e)
        })
        print(json.dumps(findings))
        return findings
    
    # Step 2: Walk AST and collect structural info
    for node in ast.walk(tree):
        # Collect function definitions
        if isinstance(node, ast.FunctionDef):
            findings["functions"].append({
                "name": node.name,
                "line": node.lineno,
                "args": [arg.arg for arg in node.args.args]
            })
        
        # Collect class definitions
        elif isinstance(node, ast.ClassDef):
            findings["classes"].append({
                "name": node.name,
                "line": node.lineno
            })
        
        # Collect imports
        elif isinstance(node, ast.Import):
            for alias in node.names:
                findings["imports"].append({
                    "type": "import",
                    "module": alias.name,
                    "line": node.lineno
                })
        elif isinstance(node, ast.ImportFrom):
            findings["imports"].append({
                "type": "from",
                "module": node.module or "",
                "names": [alias.name for alias in node.names],
                "line": node.lineno
            })
        
        # Detect code quality issues
        # Issue: Bare except clause
        if isinstance(node, ast.ExceptHandler):
            if node.type is None:
                findings["issues"].append({
                    "type": "bare_except",
                    "line": node.lineno,
                    "severity": "high",
                    "message": "Bare 'except:' catches all exceptions (including KeyboardInterrupt). Specify exception types."
                })
        
        # Issue: unused variables (simple pattern: underscore assignment)
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "_":
                    findings["issues"].append({
                        "type": "unused_variable",
                        "line": node.lineno,
                        "severity": "low",
                        "message": "Underscore assignment detected (possibly unused)"
                    })
    
    # Output as JSON for Node.js to consume
    print(json.dumps(findings))
    return findings

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No code provided"}))
        sys.exit(1)
    
    # Read Python code from command line argument
    python_code = sys.argv[1]
    analyze_python_code(python_code)
