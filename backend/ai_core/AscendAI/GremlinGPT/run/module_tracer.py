# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# !/usr/bin/env python3

"""
GremlinGPT v5 :: Module Integrity Directive

run/module_tracer.py

- Deep-scans project for all .py modules
- Maps direct imports and traces importability
- Reports as a rich table for system diagnosis/expansion
- No guesswork, no placeholders. State-of-the-art logic.
"""

import os
import importlib.util
from rich import print
from rich.table import Table

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def is_importable(module_path):
    """Check if a module is importable using importlib."""
    try:
        spec = importlib.util.spec_from_file_location("temp_module", module_path)
        if spec is None:
            return False
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return True
    except Exception:
        return False


def trace_calls():
    table = Table(title="GremlinGPT Module Interconnectivity")
    table.add_column("Module", style="cyan", no_wrap=True)
    table.add_column("Imports", style="green")
    table.add_column("Importable", style="magenta")

    for root, _, files in os.walk(BASE_DIR):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                # Normalize for pretty output
                module_name = (
                    os.path.relpath(path, BASE_DIR)
                    .replace("/", ".")
                    .replace("\\", ".")
                    .replace(".py", "")
                )
                try:
                    with open(path, encoding="utf-8") as f:
                        lines = f.readlines()
                    imports = [
                        line.strip()
                        for line in lines
                        if line.strip().startswith("import")
                        or line.strip().startswith("from")
                    ]
                    importable = (
                        "[bold green]Yes[/]"
                        if is_importable(path)
                        else "[bold red]No[/]"
                    )
                    table.add_row(module_name, "\n".join(imports), importable)
                except Exception as e:
                    table.add_row(
                        module_name, "[error] Could not read", "[bold red]No[/]"
                    )
                    print(f"[yellow][WARN][/yellow] Skipped {module_name}: {e}")

    print(table)


if __name__ == "__main__":
    trace_calls()
