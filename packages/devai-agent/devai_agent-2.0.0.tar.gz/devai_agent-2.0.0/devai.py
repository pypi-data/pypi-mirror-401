import asyncio
import sys
import json
from pathlib import Path

from rich.console import Console, Group
from rich.panel import Panel
from rich.markdown import Markdown
from rich.rule import Rule
from rich.control import Control

from config.loader import load_config
from agent.agent import Agent
from agent.events import AgentEventType
from ui.tui import TUI

# Fix for Windows asyncio
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def run():
    try:
        config = load_config(cwd=Path.cwd())
        # Disable MCP to avoid hangs if needed
        # config.mcp_servers = {} 
    except Exception as e:
        print(f"Config error: {e}")
        return

    # Initialize TUI
    tui = TUI(config)
    console = tui.console

    # Welcome Screen

    # Welcome Screen - restored and updated
    welcome_text = """
# DevAI v2.0 · Agentic Coding Assistant 🚀

I am your advanced coding assistant.
* Type your request to generate code, analyze files, or search the web.
* I can access your filesystem and run tools.

Type `/exit` to quit.
    """
    console.print(Panel(Markdown(welcome_text), title="[bold blue]DevAI[/bold blue]", border_style="blue"))


    async with Agent(config, confirmation_callback=tui.handle_confirmation) as agent:
        # Minimalist Header (Claude Code style) - kept as sub-header
        console.print(Rule(style="dim"))
        console.print(" [bold]DevAI[/bold] v2.0 · Agentic Coding Assistant", justify="center")
        console.print(" Type `/help` for commands or `/exit` to quit.", justify="center", style="dim")
        console.print(Rule(style="dim"))
        # Removed extra newline here

        while True:
            try:
                # Boxed Input Style (Claude Code)
                # 1. We are below the Top Rule (Header or Prev Turn)
                # 2. Reserve space for input
                console.print() 
                # 3. Print Bottom Rule
                console.print(Rule(style="dim"))
                # 4. Cursor is now below Bottom Rule. Move up 3 lines to the blank line.
                console.control(Control.move(0, -3))
                
                # 5. Print Prompt AND wait for input
                console.print("[bold]❯[/bold] ", end="")
                prompt = await asyncio.to_thread(input, "")
                prompt = prompt.strip()
                
                # 6. After Enter, cursor is on the Bottom Rule line. Jump past it.
                console.print() 
                
                if not prompt: 
                    continue
                if prompt.lower() in ["/exit", "/quit"]:
                    console.print("See you later!")
                    break
                    
                console.print()
                
                # 2. Assistant Turn Start
                # We start with the bullet. Text will stream after it.
                console.print("[bold cyan]●[/bold cyan] ", end="")
                
                import time
                start_time = time.time()
                
                with console.status("[dim]Processing...[/dim]", spinner="dots", spinner_style="cyan") as status:
                    async for event in agent.run(prompt):
                        if event.type == AgentEventType.TEXT_DELTA:
                            status.stop()
                            # Stream text directly. 
                            # Note: We already printed the ● prefix.
                            tui.stream_assistant_delta(event.data["content"])
                            
                        elif event.type == AgentEventType.TOOL_CALL_START:
                            status.stop()
                            args_str = event.data.get("arguments", "{}")
                            try:
                                args = json.loads(args_str)
                            except:
                                args = {"raw": args_str}
                                
                            # We might need to print a newline if we were streaming text?
                            # If we were streaming text, we are on the same line?
                            # stream_assistant_delta uses print(end="").
                            # So yes, we usually ARE on the end of a line.
                            # But tool style (Step 70) starts with a newline?
                            # Let's ensure separation.
                            # tui.tool_call_start does console.print(summary).
                            
                            tui.tool_call_start(
                                call_id=event.data.get("call_id", "unknown"),
                                name=event.data.get("name", "unknown"),
                                tool_kind=None, 
                                arguments=args
                            )
                            status.update("[dim]Running tool...[/dim]")
                            status.start()
                            
                        elif event.type == AgentEventType.TOOL_CALL_COMPLETE:
                            status.stop()
                            
                            tui.tool_call_complete(
                                call_id=event.data.get("call_id", "unknown"),
                                name=event.data.get("name", "unknown"),
                                tool_kind=None,
                                success=event.data.get("success", False),
                                output=event.data.get("output", ""),
                                error=event.data.get("error"),
                                metadata=event.data.get("metadata"),
                                diff=event.data.get("diff"),
                                truncated=event.data.get("truncated", False),
                                exit_code=event.data.get("exit_code")
                            )
                            status.update("[dim]Processing...[/dim]")
                            status.start()
                            
                        elif event.type == AgentEventType.AGENT_ERROR:
                            status.stop()
                            console.print(f"\n[bold red]Error[/bold red]: {event.data.get('error')}")
                            
                # End of turn - Footer
                duration = time.time() - start_time
                mins = int(duration // 60)
                secs = int(duration % 60)
                if mins > 0:
                    time_str = f"{mins}m {secs}s"
                else:
                    time_str = f"{secs}s"
                    
                console.print()
                console.print(f"[dim]✻ Churned for {time_str}[/dim]")
                console.print(Rule(style="dim"))
                            
            except KeyboardInterrupt:
                console.print("\n[dim]Interrupted[/dim]")
                break
            except Exception as e:
                console.print(f"\n[bold red]Critical Error[/bold red]: {e}")
                break

if __name__ == "__main__":
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        pass
