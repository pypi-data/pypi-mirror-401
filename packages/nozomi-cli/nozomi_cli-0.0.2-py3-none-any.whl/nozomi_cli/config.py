import json
import os
import time
from dataclasses import dataclass
from pathlib import Path

import questionary
from questionary import Style
from rich.console import Console

DEFAULT_API_URL = "https://api.nozomi.sh"

# Custom style for questionary prompts
NOZOMI_STYLE = Style(
    [
        ("qmark", "fg:cyan bold"),
        ("question", "bold"),
        ("answer", "fg:cyan"),
        ("pointer", "fg:cyan bold"),
        ("highlighted", "fg:cyan bold"),
        ("selected", "fg:cyan"),
        ("text", ""),
        ("instruction", "fg:gray"),
    ]
)


@dataclass
class UserConfig:
    workspace_id: str | None = None
    default_machine_tier: str = "small"


@dataclass
class FolderConfig:
    workspace_id: str | None = None
    default_machine_tier: str | None = None


@dataclass
class ResolvedConfig:
    api_url: str
    workspace_id: str | None
    default_machine_tier: str
    user_config_path: Path
    folder_config_path: Path | None


def get_config_dir() -> Path:
    config_dir = os.environ.get("NOZOMI_CONFIG_DIR")
    if config_dir:
        return Path(config_dir)
    return Path.home() / ".nozomi"


def get_user_config_path() -> Path:
    return get_config_dir() / "config.json"


def get_credentials_path() -> Path:
    return get_config_dir() / "credentials.json"


def find_folder_config() -> Path | None:
    cwd = Path.cwd()
    for parent in [cwd, *cwd.parents]:
        config_path = parent / ".nozomi" / "config.json"
        if config_path.exists():
            return config_path
    return None


def load_user_config() -> UserConfig:
    config_path = get_user_config_path()
    if not config_path.exists():
        return UserConfig()

    try:
        data = json.loads(config_path.read_text())
        return UserConfig(
            workspace_id=data.get("workspace_id"),
            default_machine_tier=data.get("default_machine_tier", "small"),
        )
    except (json.JSONDecodeError, KeyError):
        return UserConfig()


def load_folder_config(path: Path | None = None) -> FolderConfig:
    if path is None:
        path = find_folder_config()
    if path is None or not path.exists():
        return FolderConfig()

    try:
        data = json.loads(path.read_text())
        return FolderConfig(
            workspace_id=data.get("workspace_id"),
            default_machine_tier=data.get("default_machine_tier"),
        )
    except (json.JSONDecodeError, KeyError):
        return FolderConfig()


def load_config() -> ResolvedConfig:
    user_config = load_user_config()
    folder_config_path = find_folder_config()
    folder_config = load_folder_config(folder_config_path)

    api_url = os.environ.get("NOZOMI_API_URL", DEFAULT_API_URL)

    workspace_id = folder_config.workspace_id or user_config.workspace_id
    default_tier = folder_config.default_machine_tier or user_config.default_machine_tier or "small"

    return ResolvedConfig(
        api_url=api_url,
        workspace_id=workspace_id,
        default_machine_tier=default_tier,
        user_config_path=get_user_config_path(),
        folder_config_path=folder_config_path,
    )


def save_user_config(config: UserConfig) -> None:
    config_path = get_user_config_path()
    config_path.parent.mkdir(parents=True, exist_ok=True)

    data: dict = {"version": 1}
    if config.workspace_id:
        data["workspace_id"] = config.workspace_id
    if config.default_machine_tier:
        data["default_machine_tier"] = config.default_machine_tier

    config_path.write_text(json.dumps(data, indent=2))
    os.chmod(config_path, 0o600)


def save_folder_config(config: FolderConfig, path: Path | None = None) -> Path:
    if path is None:
        folder_path = Path.cwd() / ".nozomi"
        folder_path.mkdir(parents=True, exist_ok=True)
        path = folder_path / "config.json"

    data: dict = {}
    if config.workspace_id:
        data["workspace_id"] = config.workspace_id
    if config.default_machine_tier:
        data["default_machine_tier"] = config.default_machine_tier

    path.write_text(json.dumps(data, indent=2))
    return path


def get_api_url() -> str:
    return load_config().api_url


def get_workspace_id() -> str | None:
    return load_config().workspace_id


def _launch_workspace_setup(workspace_id: str) -> None:
    """Launch workspace setup by connecting via SSH."""
    from nozomi_cli.api import ApiClient
    from nozomi_cli.auth import get_access_token
    from nozomi_cli.terminal import run_ssh_terminal

    token = get_access_token()
    if not token:
        return

    config = load_config()
    api = ApiClient(config.api_url, token)

    try:
        tasks = api.list_tasks(workspace_id)
        running = [t for t in tasks if t.get("state") == "running"]
        if not running:
            return

        task_id = running[0]["id"]
        ssh_info = api.get_ssh_connection(task_id)

        run_ssh_terminal(
            host=ssh_info["host"],
            port=ssh_info["port"],
            user=ssh_info["user"],
            private_key=ssh_info["private_key"],
            attach_harness=False,
        )
    except Exception:
        pass


def _create_workspace_flow(console: Console) -> tuple[str | None, bool]:
    """Create a new workspace interactively. Returns (workspace_id, should_run_setup)."""

    from nozomi_cli.api import ApiClient
    from nozomi_cli.auth import get_access_token

    console.print()
    console.print("  [bold]Create a New Workspace[/bold]")
    console.print()
    console.print("  A workspace is your development environment with code, dependencies,")
    console.print("  and configuration. Tasks are isolated forks of your workspace.")
    console.print()

    name = questionary.text(
        "Workspace name:",
        style=NOZOMI_STYLE,
    ).ask()

    if not name or not name.strip():
        console.print("  [yellow]No name provided, skipping workspace creation.[/yellow]")
        return None, False

    token = get_access_token()
    if not token:
        console.print("  [red]Not logged in. Run 'nozomi login' first.[/red]")
        return None, False

    config = load_config()

    try:
        api = ApiClient(config.api_url, token)
        console.print()

        with console.status("[cyan]Creating workspace and starting sandbox...[/cyan]"):
            ws = api.create_workspace(name.strip())
            result = api.start_setup(ws["id"])
            task = result.get("task", result)
            task_id = task["id"]

            for _ in range(90):
                task = api.get_task(task_id)
                state = task.get("state")
                if state == "running":
                    break
                if state == "error":
                    console.print(f"  [red]Sandbox failed: {task.get('error_message')}[/red]")
                    return ws["id"], False
                time.sleep(2)

        console.print(f"  [green]Created workspace: {ws['name']}[/green]")
        console.print(f"  [dim]ID: {ws['id']}[/dim]")
        console.print()

        if task.get("state") == "running":
            console.print("  [green]Sandbox is ready![/green]")
            console.print()
            console.print("  Your workspace needs setup before you can run tasks.")
            console.print("  Setup involves cloning repos, installing dependencies, and")
            console.print("  configuring your AI harness.")
            console.print()

            start_setup = questionary.confirm(
                "Start setup now?",
                default=True,
                style=NOZOMI_STYLE,
            ).ask()

            if start_setup:
                return ws["id"], True

        return ws["id"], False
    except Exception as e:
        console.print(f"  [red]Failed to create workspace: {e}[/red]")
        return None, False


NOZOMI_ASCII = r"""
[cyan]
       _   ______  _____   ____  __  _______
      / | / / __ \/__  /  / __ \/  |/  /  _/
     /  |/ / / / /  / /  / / / / /|_/ // /
    / /|  / /_/ /  / /__/ /_/ / /  / // /
   /_/ |_/\____/  /____/\____/_/  /_/___/
[/cyan]"""


def _draw_header(console: Console, title: str | None = None) -> None:
    """Draw the config wizard header."""
    console.clear()
    console.print(NOZOMI_ASCII)
    if title:
        console.print(f"  [bold]{title}[/bold]")
        console.print()


def interactive_config_init(workspaces: list[dict] | None = None) -> None:
    """Interactive TUI for configuring nozomi."""
    console = Console()

    # Welcome screen
    _draw_header(console)
    console.print("  This wizard will configure your Nozomi CLI defaults.")
    console.print()
    console.print("  You can set a default workspace so you don't have to specify it")
    console.print(
        "  every time you run commands like [cyan]nozomi task list[/cyan] or [cyan]nozomi run[/cyan]."
    )
    console.print()

    if not questionary.confirm("Continue?", default=True, style=NOZOMI_STYLE).ask():
        return

    # Step 1: Choose scope
    _draw_header(console, "Step 1: Configuration Scope")

    console.print("  Choose where to save your configuration:")
    console.print()

    local_path = Path.cwd() / ".nozomi" / "config.json"
    global_path = get_user_config_path()

    scope_choices = [
        questionary.Choice(
            title=f"Local - {local_path}",
            value="local",
        ),
        questionary.Choice(
            title=f"Global - {global_path}",
            value="global",
        ),
    ]

    scope = questionary.select(
        "Select scope:",
        choices=scope_choices,
        style=NOZOMI_STYLE,
        instruction="(use arrow keys)",
    ).ask()

    if scope is None:
        return

    is_global = scope == "global"

    # Step 2: Choose workspace
    _draw_header(console, "Step 2: Default Workspace")

    workspace_id = None
    should_run_setup = False
    needs_setup = False

    if workspaces and len(workspaces) > 0:
        console.print("  Select a workspace to use as the default for this config.")
        console.print("  This workspace will be used when you run commands without specifying one.")
        console.print()

        ws_choices = []
        for ws in workspaces:
            status = "Ready" if ws.get("setup_completed_at") else "Setup pending"
            ws_choices.append(
                questionary.Choice(
                    title=f"{ws['name']} ({status})",
                    value=ws["id"],
                )
            )

        ws_choices.append(questionary.Choice(title="Create a new workspace", value="__create__"))
        ws_choices.append(questionary.Choice(title="Skip (no default)", value="__skip__"))

        selected = questionary.select(
            "Available workspaces:",
            choices=ws_choices,
            style=NOZOMI_STYLE,
            instruction="(use arrow keys)",
        ).ask()

        if selected is None:
            return
        elif selected == "__create__":
            workspace_id, should_run_setup = _create_workspace_flow(console)
        elif selected != "__skip__":
            workspace_id = selected
            selected_ws = next((ws for ws in workspaces if ws["id"] == selected), None)
            ws_name = selected_ws["name"] if selected_ws else selected
            needs_setup = selected_ws and not selected_ws.get("setup_completed_at")
            console.print()
            console.print(f"  Selected: [cyan]{ws_name}[/cyan]")
    else:
        console.print("  No workspaces found yet.")
        console.print()

        action_choices = [
            questionary.Choice(title="Create a new workspace", value="create"),
            questionary.Choice(title="Enter workspace ID manually", value="manual"),
            questionary.Choice(title="Skip (no default)", value="skip"),
        ]

        action = questionary.select(
            "What would you like to do?",
            choices=action_choices,
            style=NOZOMI_STYLE,
            instruction="(use arrow keys)",
        ).ask()

        if action is None:
            return
        elif action == "create":
            workspace_id, should_run_setup = _create_workspace_flow(console)
        elif action == "manual":
            console.print()
            manual_id = questionary.text(
                "Workspace ID:",
                style=NOZOMI_STYLE,
            ).ask()
            if manual_id and manual_id.strip():
                workspace_id = manual_id.strip()

    # Step 3: Choose tier
    _draw_header(console, "Step 3: Default Machine Tier")

    console.print("  Select the default machine size for new tasks.")
    console.print("  You can always override this with [cyan]--tier[/cyan] when running a task.")
    console.print()

    tier_choices = [
        questionary.Choice(title="small  - 1 CPU, 512 MB RAM", value="small"),
        questionary.Choice(title="medium - 2 CPU, 2 GB RAM", value="medium"),
        questionary.Choice(title="large  - 4 CPU, 8 GB RAM", value="large"),
    ]

    tier = questionary.select(
        "Machine tier:",
        choices=tier_choices,
        style=NOZOMI_STYLE,
        instruction="(use arrow keys)",
    ).ask()

    if tier is None:
        return

    # Summary and save
    _draw_header(console, "Configuration Summary")

    if is_global:
        save_path = get_user_config_path()
        console.print("  [bold]Scope:[/bold] Global")
    else:
        save_path = Path.cwd() / ".nozomi" / "config.json"
        console.print("  [bold]Scope:[/bold] Local (this directory)")

    console.print(f"  [bold]File:[/bold] {save_path}")
    console.print()
    console.print(f"  [bold]Default workspace:[/bold] {workspace_id or '[dim]None[/dim]'}")
    console.print(f"  [bold]Default tier:[/bold] {tier}")
    console.print()

    if needs_setup and workspace_id:
        console.print("  [yellow]This workspace needs setup before you can run tasks.[/yellow]")
        console.print()

        setup_choices = [
            questionary.Choice(title="Save and start setup now", value="setup_now"),
            questionary.Choice(title="Save and setup later", value="setup_later"),
            questionary.Choice(title="Cancel", value="cancel"),
        ]

        setup_action = questionary.select(
            "What would you like to do?",
            choices=setup_choices,
            style=NOZOMI_STYLE,
            instruction="(use arrow keys)",
        ).ask()

        if setup_action is None or setup_action == "cancel":
            console.print("\n  [yellow]Configuration cancelled.[/yellow]\n")
            return

        should_run_setup = setup_action == "setup_now"
    else:
        if not questionary.confirm(
            "Save this configuration?", default=True, style=NOZOMI_STYLE
        ).ask():
            console.print("\n  [yellow]Configuration cancelled.[/yellow]\n")
            return

    # Save
    if is_global:
        config = UserConfig(workspace_id=workspace_id, default_machine_tier=tier)
        save_user_config(config)
    else:
        config = FolderConfig(workspace_id=workspace_id, default_machine_tier=tier)
        save_folder_config(config)

    console.print()
    console.print(f"  [green]Configuration saved to {save_path}[/green]")
    console.print()

    if should_run_setup and workspace_id:
        console.print("  [cyan]Launching workspace setup...[/cyan]")
        console.print()
        _launch_workspace_setup(workspace_id)
    elif needs_setup and workspace_id:
        console.print("  [dim]To setup your workspace later, run:[/dim]")
        console.print("    [cyan]nozomi workspace setup[/cyan]")
        console.print()
    else:
        console.print("  [dim]You can now run commands without specifying workspace:[/dim]")
        console.print("    [cyan]nozomi task list[/cyan]")
        console.print('    [cyan]nozomi run "Fix the bug"[/cyan]')
        console.print()
