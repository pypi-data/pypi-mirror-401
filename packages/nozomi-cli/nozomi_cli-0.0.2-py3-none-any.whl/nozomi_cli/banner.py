from rich.console import Console

NOZOMI_BANNER = r"""
[cyan]
       _   ______  _____   ____  __  _______
      / | / / __ \/__  /  / __ \/  |/  /  _/
     /  |/ / / / /  / /  / / / / /|_/ // /
    / /|  / /_/ /  / /__/ /_/ / /  / // /
   /_/ |_/\____/  /____/\____/_/  /_/___/
[/cyan]
[dim]Remote Workspace Platform[/dim]

[yellow]In-Sandbox Commands:[/yellow]
  nozomid status              Current sandbox status
  nozomid services            List managed services
  nozomid service logs <name> View service logs
  nozomid expose <svc> <port> Expose a port publicly

[yellow]From Your Machine:[/yellow]
  nozomi task list            List your tasks
  nozomi task sleep <id>      Save state and free resources
  nozomi task connect <id>    Reconnect to a task

[dim]Press Ctrl+D or type 'exit' to detach (task keeps running)[/dim]
"""


def show_banner() -> None:
    console = Console()
    console.print(NOZOMI_BANNER)
