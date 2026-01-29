from typing import Any

import httpx


class ApiClient:
    def __init__(self, base_url: str, token: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.client = httpx.Client(timeout=30.0)

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.token}"}

    def _get(self, path: str) -> Any:
        resp = self.client.get(f"{self.base_url}{path}", headers=self._headers())
        resp.raise_for_status()
        return resp.json()

    def _post(self, path: str, data: dict | None = None) -> Any:
        resp = self.client.post(f"{self.base_url}{path}", headers=self._headers(), json=data or {})
        resp.raise_for_status()
        return resp.json()

    def get_me(self) -> dict:
        return self._get("/auth/me")

    def list_workspaces(self) -> list[dict]:
        me = self.get_me()
        org_id = me.get("org_id")
        return self._get(f"/orgs/{org_id}/workspaces")

    def create_workspace(self, name: str) -> dict:
        me = self.get_me()
        org_id = me.get("org_id")
        return self._post(f"/orgs/{org_id}/workspaces", {"name": name})

    def start_setup(self, workspace_id: str, machine_tier: str = "small") -> dict:
        return self._post(f"/workspaces/{workspace_id}/setup/start", {"machine_tier": machine_tier})

    def list_tasks(self, workspace_id: str) -> list[dict]:
        return self._get(f"/workspaces/{workspace_id}/tasks")

    def create_task(
        self, workspace_id: str, prompt: str | None = None, machine_tier: str = "small"
    ) -> dict:
        data: dict[str, Any] = {"machine_tier": machine_tier}
        if prompt:
            data["prompt"] = prompt
        resp = self._post(f"/workspaces/{workspace_id}/tasks", data)
        return resp.get("task", resp)

    def get_task(self, task_id: str) -> dict:
        return self._get(f"/tasks/{task_id}")

    def stop_task(self, task_id: str) -> dict:
        return self._post(f"/tasks/{task_id}/stop")

    def exec_in_task(
        self,
        task_id: str,
        cmd: list[str],
        cwd: str | None = None,
        env: dict[str, str] | None = None,
    ) -> dict:
        data: dict[str, Any] = {"cmd": cmd}
        if cwd:
            data["cwd"] = cwd
        if env:
            data["env"] = env
        return self._post(f"/tasks/{task_id}/exec", data)

    def create_terminal_session(self, task_id: str, tab_id: str = "cli") -> dict:
        return self._post(f"/tasks/{task_id}/terminal/sessions", {"tab_id": tab_id})

    def get_ssh_connection(self, task_id: str) -> dict:
        return self._post(f"/tasks/{task_id}/ssh")

    def sleep_task(self, task_id: str) -> dict:
        return self._post(f"/tasks/{task_id}/sleep")

    def wake_task(self, task_id: str, intent: str = "unknown") -> dict:
        return self._post(f"/tasks/{task_id}/wake?intent={intent}")
