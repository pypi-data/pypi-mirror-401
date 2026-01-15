from pathlib import Path
from typing import Any
from rich.console import Console
from rich.theme import Theme
from rich.rule import Rule
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich import box
from rich.prompt import Prompt
from rich.console import Group
from rich.syntax import Syntax
from rich.markdown import Markdown
from config.config import Config
from tools.base import ToolConfirmation
from utils.paths import display_path_rel_to_cwd
import re

from utils.text import truncate_text

AGENT_THEME = Theme(
    {
        # General
        "info": "cyan",
        "warning": "yellow",
        "error": "bright_red bold",
        "success": "green",
        "dim": "dim",
        "muted": "grey50",
        "border": "grey35",
        "highlight": "bold cyan",
        # Roles
        "user": "bright_blue bold",
        "assistant": "bright_white",
        # Tools
        "tool": "bright_magenta bold",
        "tool.read": "cyan",
        "tool.write": "yellow",
        "tool.shell": "magenta",
        "tool.network": "bright_blue",
        "tool.memory": "green",
        "tool.mcp": "bright_cyan",
        # Code / blocks
        "code": "white",
    }
)

_console: Console | None = None


def get_console() -> Console:
    global _console
    if _console is None:
        _console = Console(theme=AGENT_THEME, highlight=False)

    return _console


class TUI:
    def __init__(
        self,
        config: Config,
        console: Console | None = None,
    ) -> None:
        self.console = console or get_console()
        self._assistant_stream_open = False
        self._tool_args_by_call_id: dict[str, dict[str, Any]] = {}
        self.config = config
        self.cwd = self.config.cwd
        self._max_block_tokens = 2500

    def begin_assistant(self) -> None:
        self.console.print()
        self.console.print(Rule(Text("Assistant", style="assistant")))
        self._assistant_stream_open = True

    def end_assistant(self) -> None:
        if self._assistant_stream_open:
            self.console.print()
        self._assistant_stream_open = False

    def stream_assistant_delta(self, content: str) -> None:
        self.console.print(content, end="", markup=False)

    def _ordered_args(self, tool_name: str, args: dict[str, Any]) -> list[tuple]:
        _PREFERRED_ORDER = {
            "read_file": ["path", "offset", "limit"],
            "write_file": ["path", "create_directories", "content"],
            "edit": ["path", "replace_all", "old_string", "new_string"],
            "shell": ["command", "timeout", "cwd"],
            "list_dir": ["path", "include_hidden"],
            "grep": ["path", "case_insensitive", "pattern"],
            "glob": ["path", "pattern"],
            "todos": ["id", "action", "content"],
            "memory": ["action", "key", "value"],
        }

        preferred = _PREFERRED_ORDER.get(tool_name, [])
        ordered: list[tuple[str, Any]] = []
        seen = set()

        for key in preferred:
            if key in args:
                ordered.append((key, args[key]))
                seen.add(key)

        remaining_keys = set(args.keys() - seen)
        ordered.extend((key, args[key]) for key in remaining_keys)

        return ordered

    def _render_args_table(self, tool_name: str, args: dict[str, Any]) -> Table:
        table = Table.grid(padding=(0, 1))
        table.add_column(style="muted", justify="right", no_wrap=True)
        table.add_column(style="code", overflow="fold")

        for key, value in self._ordered_args(tool_name, args):
            if isinstance(value, str):
                if key in {"content", "old_string", "new_string"}:
                    line_count = len(value.splitlines()) or 0
                    byte_count = len(value.encode("utf-8", errors="replace"))
                    value = f"<{line_count} lines • {byte_count} bytes>"

            if isinstance(value, bool):
                value = str(value)

            table.add_row(key, value)

        return table

    def tool_call_start(
        self,
        call_id: str,
        name: str,
        tool_kind: str | None,
        arguments: dict[str, Any],
    ) -> None:
        self._tool_args_by_call_id[call_id] = arguments
        
        # Format args for the header
        arg_strs = []
        for k, v in arguments.items():
            if k in ("content", "old_string", "new_string"): continue # Skip big fields
            v_str = str(v)
            if "path" in k and self.cwd:
                try:
                    v_str = str(display_path_rel_to_cwd(v_str, self.cwd))
                except:
                    pass
            if len(v_str) > 30: v_str = v_str[:27] + "..."
            arg_strs.append(f"{v_str}") # Just values, or k=v? Claude usually uses clear summaries.
            
        # Specific formats
        if name == "glob":
            summary = f"Glob {arguments.get('pattern', '*')}"
        elif name == "grep":
            summary = f"Grep {arguments.get('pattern', '')}"
        elif name == "read_file":
            path = arguments.get("path", "")
            if self.cwd:
                try: path = str(display_path_rel_to_cwd(path, self.cwd)) 
                except: pass
            summary = f"Read {path}"
        elif name == "write_file":
             summary = f"Write {arguments.get('path', 'file')}"
        elif name == "list_dir":
             summary = f"List {arguments.get('path', '.')}"
        elif name == "shell":
             summary = f"Run {arguments.get('command', '')}"
        else:
             summary = f"{name}(" + ", ".join(arg_strs) + ")"

        # Print the "Start" bullet
        self.console.print(f"[bold cyan]●[/bold cyan] [bold]{summary}[/bold]")

    def tool_call_complete(
        self,
        call_id: str,
        name: str,
        tool_kind: str | None,
        success: bool,
        output: str,
        error: str | None,
        metadata: dict[str, Any] | None,
        diff: str | None,
        truncated: bool,
        exit_code: int | None,
    ) -> None:
        
        # Completion line with indented arrow
        indent = "  "
        icon = "Done" if success else "Failed"
        style = "dim" if success else "red"
        
        # Summary stats
        stats = []
        if metadata:
            if "matches" in metadata: stats.append(f"{metadata['matches']} matches")
            if "entries" in metadata: stats.append(f"{metadata['entries']} items")
            if "total_lines" in metadata: stats.append(f"{metadata.get('total_lines')} lines")
            
        stats_str = f" ({' · '.join(stats)})" if stats else ""
        
        # Print completion line
        self.console.print(f"{indent}[{style}]⎿  {icon}{stats_str}[/{style}]")
        
        # If there is important content (like read_file output or diffs), show it below
        # but keep it minimal
        if output.strip() and success:
             # Only for specific tools or if user requested
             if name in ("read_file", "cat", "grep", "shell"):
                 # Determine logic
                 lexer = "text"
                 if name == "read_file":
                      args = self._tool_args_by_call_id.get(call_id, {})
                      lexer = self._guess_language(args.get("path"))
                      
                 # Small vertical margin
                 display_out = output
                 if len(display_out) > 2000:
                     display_out = display_out[:2000] + "\n... (truncated)"
                     
                 # Render without panel, just plain syntax
                 self.console.print(Syntax(display_out, lexer, theme="monokai", word_wrap=True, indent_guides=True))

        if error:
            self.console.print(f"{indent}[red]{error}[/red]")
            
        if diff:
             self.console.print(Syntax(diff, "diff", theme="monokai", word_wrap=True))

    def handle_confirmation(self, confirmation: ToolConfirmation) -> bool:
        # Minimalist confirmation inline
        self.console.print()
        self.console.print(f"[bold yellow]![/bold yellow] [bold]Approval Required[/bold]: {confirmation.description}")
        if confirmation.command:
            self.console.print(f"  [dim]$ {confirmation.command}[/dim]")
            
        response = Prompt.ask("  [bold]Authorize?[/bold] (y/n)", choices=["y", "n", "yes", "no"], default="y")
        return response.lower() in {"y", "yes"}

    def _guess_language(self, path: str | None) -> str:
        if not path:
            return "text"
        suffix = Path(path).suffix.lower()
        return {
            ".py": "python",
            ".js": "javascript",
            ".jsx": "jsx",
            ".ts": "typescript",
            ".tsx": "tsx",
            ".json": "json",
            ".toml": "toml",
            ".yaml": "yaml",
            ".yml": "yaml",
            ".md": "markdown",
            ".sh": "bash",
            ".bash": "bash",
            ".zsh": "bash",
            ".rs": "rust",
            ".go": "go",
            ".java": "java",
            ".kt": "kotlin",
            ".swift": "swift",
            ".c": "c",
            ".h": "c",
            ".cpp": "cpp",
            ".hpp": "cpp",
            ".css": "css",
            ".html": "html",
            ".xml": "xml",
            ".sql": "sql",
        }.get(suffix, "text")

    def show_help(self) -> None:
        help_text = """
# DevAI Commands

* `/exit`      - Quit
* `/clear`     - Clear history
* `/config`    - View config
* `/model`     - Switch model
* `/help`      - Show this menu
        """
        self.console.print(Markdown(help_text))
