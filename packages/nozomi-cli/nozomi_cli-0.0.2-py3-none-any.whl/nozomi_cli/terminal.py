import subprocess
import tempfile
from pathlib import Path

from nozomi_cli.banner import show_banner


def run_ssh_terminal(
    host: str,
    port: int,
    user: str,
    private_key: str,
    attach_harness: bool = False,
    show_welcome: bool = True,
) -> int:
    """Connect to a sandbox via SSH using native ssh command.

    Args:
        host: SSH host
        port: SSH port
        user: SSH user
        private_key: SSH private key content
        attach_harness: If True, attach to tmux harness session (nozomi:harness)
        show_welcome: Show welcome banner
    """
    if show_welcome:
        show_banner()

    with tempfile.TemporaryDirectory() as tmpdir:
        key_path = Path(tmpdir) / "key"
        key_path.write_text(private_key)
        key_path.chmod(0o600)

        if attach_harness:
            remote_cmd = (
                "TERM=xterm-256color tmux attach -t nozomi:harness 2>/dev/null || exec bash -l"
            )
        else:
            remote_cmd = "TERM=xterm-256color exec bash -l"

        ssh_args = [
            "ssh",
            "-i",
            str(key_path),
            "-p",
            str(port),
            "-o",
            "StrictHostKeyChecking=no",
            "-o",
            "UserKnownHostsFile=/dev/null",
            "-o",
            "LogLevel=ERROR",
            "-t",
            f"{user}@{host}",
            remote_cmd,
        ]

        return subprocess.call(ssh_args)
