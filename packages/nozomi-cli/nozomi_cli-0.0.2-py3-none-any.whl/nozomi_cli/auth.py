import json
import os
import time
import webbrowser
from dataclasses import dataclass
from datetime import datetime

import httpx
from rich.console import Console

from nozomi_cli.config import get_credentials_path, load_config


@dataclass
class UserInfo:
    id: str
    email: str
    org_id: str


@dataclass
class Credentials:
    access_token: str
    refresh_token: str | None = None
    expires_at: datetime | None = None
    user: UserInfo | None = None


def _load_credentials_file() -> dict:
    path = get_credentials_path()
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except (json.JSONDecodeError, KeyError):
        return {}


def _save_credentials_file(data: dict) -> None:
    path = get_credentials_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2))
    os.chmod(path, 0o600)


def get_credentials() -> Credentials | None:
    if token := os.getenv("NOZOMI_ACCESS_TOKEN"):
        return Credentials(access_token=token)

    data = _load_credentials_file()
    if not data.get("access_token"):
        return None

    user = None
    if user_data := data.get("user"):
        user = UserInfo(
            id=user_data.get("id", ""),
            email=user_data.get("email", ""),
            org_id=user_data.get("org_id", ""),
        )

    expires_at = None
    if exp_str := data.get("expires_at"):
        try:
            expires_at = datetime.fromisoformat(exp_str.replace("Z", "+00:00"))
        except ValueError:
            pass

    return Credentials(
        access_token=data.get("access_token", ""),
        refresh_token=data.get("refresh_token"),
        expires_at=expires_at,
        user=user,
    )


def save_credentials(creds: Credentials) -> None:
    data: dict = {
        "access_token": creds.access_token,
    }
    if creds.refresh_token:
        data["refresh_token"] = creds.refresh_token
    if creds.expires_at:
        data["expires_at"] = creds.expires_at.isoformat()
    if creds.user:
        data["user"] = {
            "id": creds.user.id,
            "email": creds.user.email,
            "org_id": creds.user.org_id,
        }

    _save_credentials_file(data)


def clear_credentials() -> None:
    path = get_credentials_path()
    if path.exists():
        path.unlink()


def get_access_token() -> str | None:
    creds = get_credentials()
    if creds:
        return creds.access_token
    return None


def whoami_info() -> dict | None:
    creds = get_credentials()
    if not creds:
        return None

    if creds.user:
        return {
            "id": creds.user.id,
            "email": creds.user.email,
            "org_id": creds.user.org_id,
        }

    config = load_config()
    try:
        resp = httpx.get(
            f"{config.api_url}/auth/me",
            headers={"Authorization": f"Bearer {creds.access_token}"},
            timeout=10.0,
        )
        if resp.status_code == 200:
            return resp.json()
    except Exception:
        pass
    return None


def login_flow() -> Credentials | None:
    console = Console()
    config = load_config()
    api_url = config.api_url

    console.print("[cyan]Opening browser for login...[/cyan]")

    try:
        resp = httpx.post(f"{api_url}/auth/device/start", timeout=10.0)
        resp.raise_for_status()
        data = resp.json()

        device_code = data.get("device_code")
        user_code = data.get("user_code")
        verification_uri = data.get("verification_uri")
        expires_in = data.get("expires_in", 300)

        console.print(f"\n[bold]Enter this code in the browser:[/bold] {user_code}\n")
        webbrowser.open(verification_uri)

        poll_interval = 5
        max_attempts = expires_in // poll_interval

        with console.status("[dim]Waiting for authorization...[/dim]"):
            for _ in range(max_attempts):
                poll_resp = httpx.post(
                    f"{api_url}/auth/device/poll",
                    json={"device_code": device_code},
                    timeout=10.0,
                )

                if poll_resp.status_code == 200:
                    tokens = poll_resp.json()
                    creds = Credentials(
                        access_token=tokens.get("access_token"),
                        refresh_token=tokens.get("refresh_token"),
                    )

                    user_resp = httpx.get(
                        f"{api_url}/auth/me",
                        headers={"Authorization": f"Bearer {creds.access_token}"},
                        timeout=10.0,
                    )
                    if user_resp.status_code == 200:
                        user_data = user_resp.json()
                        creds.user = UserInfo(
                            id=user_data.get("id", ""),
                            email=user_data.get("email", ""),
                            org_id=user_data.get("org_id", ""),
                        )

                    save_credentials(creds)
                    console.print("\n[green]Login successful![/green]")
                    return creds

                if poll_resp.status_code == 428:
                    time.sleep(poll_interval)
                    continue

                console.print(f"\n[red]Login failed: {poll_resp.text}[/red]")
                return None

        console.print("\n[red]Login timed out. Please try again.[/red]")
        return None

    except httpx.HTTPStatusError as e:
        console.print(f"[red]Auth error: {e.response.text}[/red]")
        return None
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        return None


def logout() -> None:
    clear_credentials()
