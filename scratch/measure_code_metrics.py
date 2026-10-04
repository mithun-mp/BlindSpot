import os
import ast
import sys

sys.stdout.reconfigure(encoding='utf-8')
WORKSPACE = r"C:\Dev\Projects\Multimodel\Multimodel_Blindspot-main"
BLINDSPOT = os.path.join(WORKSPACE, "blindspot")
TESTS = os.path.join(WORKSPACE, "tests")

def analyze_dir(dpath):
    total_loc = 0
    non_empty_loc = 0
    py_files = 0
    total_classes = 0
    total_functions = 0
    for root, _, files in os.walk(dpath):
        if "__pycache__" in root:
            continue
        for f in files:
            if f.endswith(".py"):
                py_files += 1
                fp = os.path.join(root, f)
                with open(fp, "r", encoding="utf-8", errors="ignore") as fh:
                    lines = fh.readlines()
                total_loc += len(lines)
                non_empty_loc += sum(1 for line in lines if line.strip() and not line.strip().startswith("#"))
                try:
                    tree = ast.parse("".join(lines), filename=fp)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.ClassDef):
                            total_classes += 1
                        elif isinstance(node, ast.FunctionDef):
                            total_functions += 1
                except Exception:
                    pass
    return {
        "files": py_files,
        "total_loc": total_loc,
        "non_empty_loc": non_empty_loc,
        "classes": total_classes,
        "functions": total_functions,
    }

bs_metrics = analyze_dir(BLINDSPOT)
test_metrics = analyze_dir(TESTS)

print("=== BLINDSPOT CORE METRICS ===")
for k, v in bs_metrics.items():
    print(f"  {k}: {v}")

print("\n=== TESTS METRICS ===")
for k, v in test_metrics.items():
    print(f"  {k}: {v}")
