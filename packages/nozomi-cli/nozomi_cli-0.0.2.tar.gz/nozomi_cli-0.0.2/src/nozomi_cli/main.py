import time

import click
import httpx
from packaging.version import Version
from rich.console import Console
from rich.prompt import Confirm
from rich.table import Table

from nozomi_cli import __version__
from nozomi_cli.api import ApiClient
from nozomi_cli.auth import get_access_token, login_flow, whoami_info
from nozomi_cli.auth import logout as auth_logout
from nozomi_cli.config import interactive_config_init, load_config
from nozomi_cli.output import output, print_error, print_info, print_success, print_warning

PYPI_PACKAGE_NAME = "nozomi-cli"

console = Console()


def get_api(json_output: bool = False) -> ApiClient | None:
    """Get an authenticated API client or print error."""
    config = load_config()
    token = get_access_token()
    if not token:
        print_error("Not logged in. Run 'nozomi init' to get started.", json_output)
        return None
    return ApiClient(config.api_url, token)


@click.group()
@click.option("--json", "json_output", is_flag=True, help="Output in JSON format")
@click.pass_context
def cli(ctx: click.Context, json_output: bool) -> None:
    """Nozomi CLI - Remote workspace platform."""
    ctx.ensure_object(dict)
    ctx.obj["json"] = json_output


NOZOMI_ASCII = r"""
[cyan]
       _   ______  _____   ____  __  _______
      / | / / __ \/__  /  / __ \/  |/  /  _/
     /  |/ / / / /  / /  / / / / /|_/ // /
    / /|  / /_/ /  / /__/ /_/ / /  / // /
   /_/ |_/\____/  /____/\____/_/  /_/___/
[/cyan]"""


@cli.command()
def init() -> None:
    """Initialize Nozomi configuration (interactive setup).

    This is the recommended first command for new users.
    It will prompt for login if needed, then guide you through
    creating a workspace and configuring your CLI.
    """
    token = get_access_token()

    if not token:
        console.clear()
        console.print(NOZOMI_ASCII)
        console.print("  [bold]Welcome to Nozomi![/bold]")
        console.print()
        console.print("  Let's get you set up. First, you'll need to log in.")
        console.print()

        if not login_flow():
            return

    api = get_api(json_output=False)
    workspaces = None
    if api:
        try:
            workspaces = api.list_workspaces()
        except Exception as e:
            config = load_config()
            console.print(f"  [yellow]Could not fetch workspaces from {config.api_url}[/yellow]")
            console.print(f"  [dim]{e}[/dim]")
            console.print()

    interactive_config_init(workspaces)


@cli.command()
def login() -> None:
    """Login to Nozomi (opens browser)."""
    login_flow()


@cli.command("logout")
@click.pass_context
def logout_cmd(ctx: click.Context) -> None:
    """Logout from Nozomi."""
    auth_logout()
    if not ctx.obj.get("json"):
        print_success("Logged out successfully")


@cli.command()
@click.pass_context
def whoami(ctx: click.Context) -> None:
    """Show current user info."""
    json_output = ctx.obj.get("json", False)
    info = whoami_info()
    if info:
        output({"email": info["email"], "org_id": info["org_id"]}, json_output)
    else:
        print_warning("Not logged in", json_output)


@cli.group()
def workspace() -> None:
    """Manage workspaces."""
    pass


@workspace.command("list")
@click.pass_context
def workspace_list(ctx: click.Context) -> None:
    """List all workspaces."""
    json_output = ctx.obj.get("json", False)
    api = get_api(json_output)
    if not api:
        return

    try:
        ws_list = api.list_workspaces()
        if not ws_list:
            if json_output:
                output([], json_output)
            else:
                print_info("No workspaces found. Create one with 'nozomi workspace create <name>'")
            return

        if json_output:
            output(ws_list, json_output)
            return

        config = load_config()
        table = Table(show_header=True, header_style="bold")
        table.add_column("ID", style="cyan")
        table.add_column("Name")
        table.add_column("Status")
        table.add_column("Default", justify="center")

        for ws in ws_list:
            status = "Ready" if ws.get("setup_completed_at") else "Setup pending"
            status_styled = (
                f"[green]{status}[/green]"
                if ws.get("setup_completed_at")
                else f"[yellow]{status}[/yellow]"
            )
            is_default = ws["id"] == config.workspace_id
            default_marker = "[cyan]*[/cyan]" if is_default else ""
            table.add_row(ws["id"], ws["name"], status_styled, default_marker)

        console.print(table)

        if config.workspace_id:
            console.print("\n[dim]* = default workspace from config[/dim]")

    except Exception as e:
        print_error(str(e), json_output)


@workspace.command("create")
@click.argument("name")
@click.option("--connect", "-c", is_flag=True, help="Connect to workspace after creation")
@click.pass_context
def workspace_create(ctx: click.Context, name: str, connect: bool) -> None:
    """Create a new workspace and start the sandbox."""
    json_output = ctx.obj.get("json", False)
    api = get_api(json_output)
    if not api:
        return

    try:
        ws = api.create_workspace(name)

        if json_output and not connect:
            output(ws, json_output)
            return

        print_success(f"Created workspace: {ws['id']}")
        print_info(f"Name: {ws['name']}")

        with console.status("[cyan]Starting sandbox (this may take a minute)...[/cyan]"):
            result = api.start_setup(ws["id"])
            task = result.get("task", result)
            task_id = task["id"]

            for _ in range(90):
                task = api.get_task(task_id)
                state = task.get("state")

                if state == "running":
                    break
                if state == "error":
                    print_error(f"Sandbox failed: {task.get('error_message', 'Unknown error')}")
                    return

                time.sleep(2)
            else:
                print_warning(f"Sandbox still starting (state: {state}). Run setup later.")
                return

        print_success("Sandbox ready!")

        if connect:
            _connect_to_task(api, task_id, json_output)
        else:
            print_info(f"Run setup: nozomi workspace setup {ws['id']}")

    except Exception as e:
        print_error(str(e), json_output)


@workspace.command("setup")
@click.argument("workspace_id", required=False)
@click.pass_context
def workspace_setup(ctx: click.Context, workspace_id: str | None) -> None:
    """Start or resume workspace setup (opens interactive terminal via SSH)."""
    json_output = ctx.obj.get("json", False)
    config = load_config()
    api = get_api(json_output)
    if not api:
        return

    if not workspace_id:
        workspace_id = config.workspace_id
        if not workspace_id:
            print_error(
                "No workspace ID provided. Pass it as argument or run 'nozomi config init'",
                json_output,
            )
            return
        print_info(f"Using workspace from config: {workspace_id}")

    task_id = None

    try:
        result = api.start_setup(workspace_id)
        task = result.get("task", result)
        task_id = task["id"]

        if task.get("state") != "running":
            with console.status("[cyan]Waiting for sandbox...[/cyan]"):
                for _ in range(60):
                    task = api.get_task(task_id)
                    state = task.get("state")

                    if state == "running":
                        break
                    if state == "error":
                        print_error(f"Sandbox failed: {task.get('error_message')}")
                        return

                    time.sleep(2)
                else:
                    print_error(f"Timeout waiting for sandbox (state: {state})")
                    return

        _connect_to_task(api, task_id, json_output, attach_harness=False)

    except KeyboardInterrupt:
        print_warning("\nDetached. Task still running.")
        if task_id:
            print_info(f"Reconnect: nozomi task connect {task_id}")
    except Exception as e:
        print_error(str(e), json_output)


@workspace.command("connect")
@click.argument("workspace_id", required=False)
@click.pass_context
def workspace_connect(ctx: click.Context, workspace_id: str | None) -> None:
    """Connect to a workspace's running task."""
    json_output = ctx.obj.get("json", False)
    config = load_config()
    api = get_api(json_output)
    if not api:
        return

    if not workspace_id:
        workspace_id = config.workspace_id
        if not workspace_id:
            print_error(
                "No workspace ID provided. Pass it as argument or run 'nozomi config init'",
                json_output,
            )
            return

    try:
        tasks = api.list_tasks(workspace_id)
        running_tasks = [t for t in tasks if t.get("state") == "running"]

        if not running_tasks:
            print_error("No running tasks in this workspace")
            return

        task_id = running_tasks[0]["id"]
        _connect_to_task(api, task_id, json_output)

    except KeyboardInterrupt:
        print_warning("\nDetached. Task still running.")
    except Exception as e:
        print_error(str(e), json_output)


@cli.group()
def task() -> None:
    """Manage tasks."""
    pass


@task.command("list")
@click.option("--workspace", "-w", help="Filter by workspace ID (uses config default if set)")
@click.option(
    "--state",
    "-s",
    type=click.Choice(["running", "sleeping", "stopped", "error", "all"]),
    default="all",
    help="Filter by state",
)
@click.option("--all", "-a", "show_all", is_flag=True, help="Show tasks from all workspaces")
@click.pass_context
def task_list(ctx: click.Context, workspace: str | None, state: str, show_all: bool) -> None:
    """List tasks."""
    json_output = ctx.obj.get("json", False)
    config = load_config()
    api = get_api(json_output)
    if not api:
        return

    try:
        if show_all:
            ws_list = api.list_workspaces()
            task_list_data = []
            for ws in ws_list:
                task_list_data.extend(api.list_tasks(ws["id"]))
        elif workspace:
            task_list_data = api.list_tasks(workspace)
        elif config.workspace_id:
            if not json_output:
                print_info(f"Showing tasks for workspace: {config.workspace_id}")
                print_info("Use --all to see all workspaces")
            task_list_data = api.list_tasks(config.workspace_id)
        else:
            ws_list = api.list_workspaces()
            task_list_data = []
            for ws in ws_list:
                task_list_data.extend(api.list_tasks(ws["id"]))

        if state != "all":
            task_list_data = [t for t in task_list_data if t.get("state") == state]

        if not task_list_data:
            if json_output:
                output([], json_output)
            else:
                print_info("No tasks found.")
            return

        if json_output:
            output(task_list_data, json_output)
            return

        table = Table(show_header=True, header_style="bold")
        table.add_column("ID", style="cyan")
        table.add_column("State")
        table.add_column("Prompt")

        for t in task_list_data:
            task_state = t["state"]
            state_color = {
                "running": "green",
                "sleeping": "yellow",
                "stopped": "dim",
                "error": "red",
                "starting": "cyan",
            }.get(task_state, "white")
            state_styled = f"[{state_color}]{task_state}[/{state_color}]"
            prompt = (t.get("prompt") or "-")[:50]
            if len(t.get("prompt") or "") > 50:
                prompt += "..."
            table.add_row(t["id"], state_styled, prompt)

        console.print(table)

        running = [t for t in task_list_data if t.get("state") == "running"]
        sleeping = [t for t in task_list_data if t.get("state") == "sleeping"]

        if running:
            console.print("\n[dim]Connect to a task: nozomi task connect <id>[/dim]")
        if sleeping:
            console.print("[dim]Wake a sleeping task: nozomi task connect <id> (auto-wakes)[/dim]")

    except Exception as e:
        print_error(str(e), json_output)


@task.command("connect")
@click.argument("task_id")
@click.option("--shell", "-s", is_flag=True, help="Open shell instead of attaching to harness")
@click.pass_context
def task_connect(ctx: click.Context, task_id: str, shell: bool) -> None:
    """Connect terminal to a task.

    Automatically wakes sleeping tasks. By default, attaches to the
    harness tmux session. Use --shell to get a plain shell instead.
    """
    json_output = ctx.obj.get("json", False)
    api = get_api(json_output)
    if not api:
        return

    try:
        task = api.get_task(task_id)
        state = task.get("state")

        if state == "sleeping":
            with console.status("[cyan]Task sandbox went to sleep, waking...[/cyan]"):
                task = api.wake_task(task_id, intent="attach")

                for _ in range(60):
                    task = api.get_task(task_id)
                    if task.get("state") == "running":
                        break
                    time.sleep(1)

            if task.get("state") != "running":
                print_error(f"Failed to wake task (state: {task.get('state')})")
                return

            if not json_output:
                print_success("Task is now running")

        elif state != "running":
            print_error(f"Task is not running (state: {state})")
            return

        _connect_to_task(api, task_id, json_output, attach_harness=not shell)

    except KeyboardInterrupt:
        print_warning("\nDetached from terminal. Task is still running.")
    except Exception as e:
        print_error(str(e), json_output)


@task.command("stop")
@click.argument("task_id")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation")
@click.pass_context
def task_stop(ctx: click.Context, task_id: str, yes: bool) -> None:
    """Stop a running task."""
    json_output = ctx.obj.get("json", False)
    api = get_api(json_output)
    if not api:
        return

    if not yes and not json_output:
        if not Confirm.ask(f"Stop task {task_id}?"):
            return

    try:
        task = api.stop_task(task_id)
        if json_output:
            output(task, json_output)
        else:
            print_success(f"Stopped task: {task['id']}")
    except Exception as e:
        print_error(str(e), json_output)


@task.command("sleep")
@click.argument("task_id")
@click.pass_context
def task_sleep(ctx: click.Context, task_id: str) -> None:
    """Put a task to sleep (saves state, frees resources)."""
    json_output = ctx.obj.get("json", False)
    api = get_api(json_output)
    if not api:
        return

    try:
        task = api.sleep_task(task_id)
        if json_output:
            output(task, json_output)
        else:
            print_success(f"Task {task_id} is now sleeping")
            print_info("Wake it with: nozomi task connect " + task_id)
    except Exception as e:
        print_error(str(e), json_output)


@task.command("wake")
@click.argument("task_id")
@click.pass_context
def task_wake(ctx: click.Context, task_id: str) -> None:
    """Wake a sleeping task."""
    json_output = ctx.obj.get("json", False)
    api = get_api(json_output)
    if not api:
        return

    try:
        with console.status("[cyan]Waking task...[/cyan]"):
            task = api.wake_task(task_id)

        if json_output:
            output(task, json_output)
        else:
            print_success(f"Task {task_id} is now running")
    except Exception as e:
        print_error(str(e), json_output)


@cli.command()
@click.argument("prompt")
@click.option("--workspace", "-w", help="Workspace ID (uses config default)")
@click.option("--tier", "-t", type=click.Choice(["small", "medium", "large"]), help="Machine tier")
@click.option("--connect", "-c", is_flag=True, help="Connect to task after launch")
@click.pass_context
def run(
    ctx: click.Context, prompt: str, workspace: str | None, tier: str | None, connect: bool
) -> None:
    """Launch a task with a prompt.

    Example: nozomi run "Fix the auth bug in login.py"
    """
    json_output = ctx.obj.get("json", False)
    config = load_config()
    api = get_api(json_output)
    if not api:
        return

    try:
        if not workspace:
            workspace = config.workspace_id

        if not workspace:
            ws_list = api.list_workspaces()
            ready_ws = [w for w in ws_list if w.get("setup_completed_at")]
            if not ready_ws:
                print_error("No ready workspaces found. Create and setup one first.")
                return
            workspace = ready_ws[0]["id"]
            if not json_output:
                print_info(f"Using workspace: {workspace}")

        machine_tier = tier or config.default_machine_tier
        task = api.create_task(workspace, prompt=prompt, machine_tier=machine_tier)

        if json_output and not connect:
            output(task, json_output)
            return

        print_success(f"Launched task: {task['id']}")
        print_info(f"Prompt: {prompt}")

        if connect:
            with console.status("[cyan]Waiting for task to start...[/cyan]"):
                for _ in range(30):
                    task = api.get_task(task["id"])
                    if task.get("state") == "running":
                        break
                    time.sleep(1)

            if task.get("state") == "running":
                _connect_to_task(api, task["id"], json_output)
            else:
                print_warning(f"Task not running yet (state: {task.get('state')})")
                print_info(f"Connect later: nozomi task connect {task['id']}")
        else:
            print_info(f"Connect with: nozomi task connect {task['id']}")
    except Exception as e:
        print_error(str(e), json_output)


@cli.group()
def config() -> None:
    """Manage configuration."""
    pass


@config.command("show")
@click.pass_context
def config_show(ctx: click.Context) -> None:
    """Show current configuration."""
    json_output = ctx.obj.get("json", False)
    resolved = load_config()

    data = {
        "api_url": resolved.api_url,
        "workspace_id": resolved.workspace_id,
        "default_machine_tier": resolved.default_machine_tier,
        "user_config": str(resolved.user_config_path),
        "folder_config": str(resolved.folder_config_path) if resolved.folder_config_path else None,
    }
    output(data, json_output)


@config.command("init")
@click.pass_context
def config_init(ctx: click.Context) -> None:
    """Interactive configuration setup."""
    json_output = ctx.obj.get("json", False)

    if json_output:
        print_error("Interactive config not available in JSON mode", json_output)
        return

    api = get_api(json_output)
    workspaces = None
    if api:
        try:
            workspaces = api.list_workspaces()
        except Exception:
            pass

    interactive_config_init(workspaces)


@cli.command()
@click.argument("task_id")
@click.argument("command", nargs=-1)
@click.option("--cwd", "-c", help="Working directory for the command")
@click.pass_context
def exec(ctx: click.Context, task_id: str, command: tuple[str, ...], cwd: str | None) -> None:
    """Execute a command in a task's sandbox.

    If no command is provided, opens an interactive shell.

    Examples:
        nozomi exec task_123 -- ls -la
        nozomi exec task_123 -- python script.py
        nozomi exec task_123 --cwd /workspace -- npm test
    """
    json_output = ctx.obj.get("json", False)
    api = get_api(json_output)
    if not api:
        return

    if not command:
        _connect_to_task(api, task_id, json_output, attach_harness=False)
        return

    cmd_list = list(command)

    try:
        task = api.get_task(task_id)
        if task.get("state") != "running":
            print_error(f"Task is not running (state: {task.get('state')})")
            return

        if not json_output:
            print_info(f"Executing: {' '.join(cmd_list)}")

        result = api.exec_in_task(task_id, cmd_list, cwd=cwd)

        if json_output:
            output(result, json_output)
        else:
            if result.get("stdout"):
                console.print(result["stdout"], end="")
            if result.get("stderr"):
                console.print(f"[red]{result['stderr']}[/red]", end="")

            exit_code = result.get("exit_code", 0)
            if exit_code != 0:
                print_warning(f"Exit code: {exit_code}")
    except Exception as e:
        print_error(str(e), json_output)


def _connect_to_task(
    api: ApiClient, task_id: str, json_output: bool = False, attach_harness: bool = True
) -> None:
    """Helper to establish SSH connection to a task."""
    from nozomi_cli.terminal import run_ssh_terminal

    if not json_output:
        print_info("Connecting...")

    ssh_info = api.get_ssh_connection(task_id)

    if json_output:
        output(
            {
                "host": ssh_info["host"],
                "port": ssh_info["port"],
                "user": ssh_info["user"],
            },
            json_output,
        )
        return

    run_ssh_terminal(
        host=ssh_info["host"],
        port=ssh_info["port"],
        user=ssh_info["user"],
        private_key=ssh_info["private_key"],
        attach_harness=attach_harness,
    )


def check_for_updates() -> dict[str, str | bool] | None:
    """Check PyPI for the latest version of nozomi-cli."""
    try:
        response = httpx.get(
            f"https://pypi.org/pypi/{PYPI_PACKAGE_NAME}/json",
            timeout=5.0,
        )
        if response.status_code != 200:
            return None

        data = response.json()
        latest_version = data["info"]["version"]
        current = Version(__version__)
        latest = Version(latest_version)

        return {
            "current_version": __version__,
            "latest_version": latest_version,
            "update_available": latest > current,
        }
    except Exception:
        return None


@cli.command()
@click.option("--check", "-c", is_flag=True, help="Check for updates from PyPI")
@click.pass_context
def version(ctx: click.Context, check: bool) -> None:
    """Show version information and check for updates."""
    json_output = ctx.obj.get("json", False)

    version_info: dict[str, str | bool | None] = {
        "version": __version__,
        "update_available": None,
        "latest_version": None,
    }

    if check:
        if not json_output:
            with console.status("[cyan]Checking for updates...[/cyan]"):
                update_info = check_for_updates()
        else:
            update_info = check_for_updates()

        if update_info:
            version_info["latest_version"] = update_info["latest_version"]
            version_info["update_available"] = update_info["update_available"]

    if json_output:
        output(version_info, json_output)
        return

    console.print(f"nozomi-cli [cyan]{__version__}[/cyan]")

    if check:
        if version_info["latest_version"] is None:
            print_warning("Could not check for updates (package may not be published yet)")
        elif version_info["update_available"]:
            print_warning(f"Update available: {version_info['latest_version']}")
            console.print("\n[dim]To update, run:[/dim]")
            console.print("  uv tool upgrade nozomi-cli")
            console.print("  [dim]# or: pip install --upgrade nozomi-cli[/dim]")
        else:
            print_success("You're running the latest version")


if __name__ == "__main__":
    cli()
