from typing import Any
from pathlib import Path
import subprocess
import sys

from tools.base import Tool, ToolInvocation, ToolResult
from config.config import Config

class LintFileTool(Tool):
    """Checks a Python file for syntax errors using py_compile."""

    name = "lint_file"
    description = "Checks a Python file for syntax errors."
    
    @property
    def schema(self):
        return {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Absolute path to the python file to lint",
            }
        },
        "required": ["path"],
    }

    async def execute(self, invocation: ToolInvocation) -> ToolResult:
        file_path = Path(invocation.params["path"])
        
        if not file_path.is_absolute():
             file_path = invocation.cwd / file_path

        if not file_path.exists():
            return ToolResult.error_result(f"File not found: {file_path}")

        try:
            # Run py_compile to check syntax
            # We use subprocess to isolate it
            cmd = [sys.executable, "-m", "py_compile", str(file_path)]
            
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True
            )
            
            if process.returncode == 0:
                return ToolResult.success_result(f"No syntax errors found in {file_path.name}.")
            else:
                # Syntax error found
                error_msg = process.stderr.strip()
                return ToolResult.error_result(f"Syntax Error:\n{error_msg}")

        except Exception as e:
            return ToolResult.error_result(f"Linting failed: {e}")
