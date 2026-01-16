"""
Real-time sync client for VibeKit using Server-Sent Events (SSE).

Connects to vkcli.com SSE endpoint and auto-updates local .vk/ files
when changes occur on the server (task updates, sprint changes, etc.).
"""

import asyncio
import json
import signal
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional

import yaml

try:
    import httpx
except ImportError:
    httpx = None


class RealtimeSyncClient:
    """
    Background SSE listener that auto-updates .vk/ files.

    Usage:
        client = RealtimeSyncClient(project_root)
        await client.connect(project_id, auth_token)

    Or use the sync helper:
        await watch_project(project_root)
    """

    def __init__(
        self,
        project_root: Optional[Path] = None,
        api_url: str = "https://vkcli.com/api",
    ):
        """
        Initialize real-time sync client.

        Args:
            project_root: Root directory of the project (default: cwd)
            api_url: Base URL for the API
        """
        self.project_root = project_root or Path.cwd()
        self.vk_dir = self.project_root / ".vk"
        self.api_url = api_url
        self._running = False
        self._reconnect_delay = 1  # seconds, exponential backoff
        self._max_reconnect_delay = 60
        self._handlers: dict[str, list[Callable]] = {}

    def on(self, event_type: str, handler: Callable) -> None:
        """
        Register event handler.

        Args:
            event_type: Event type to handle (task.updated, sprint.changed, etc.)
            handler: Async function to call with event data
        """
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    async def connect(
        self,
        project_id: str,
        auth_token: str,
        on_connected: Optional[Callable] = None,
        on_error: Optional[Callable] = None,
    ) -> None:
        """
        Connect to SSE endpoint and start listening.

        Args:
            project_id: Project ID to subscribe to
            auth_token: Authentication token
            on_connected: Callback when connected
            on_error: Callback on errors
        """
        if httpx is None:
            raise ImportError("httpx is required for real-time sync. Install with: pip install httpx")

        self._running = True
        url = f"{self.api_url}/projects/{project_id}/events"
        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Accept": "text/event-stream",
        }

        while self._running:
            try:
                async with httpx.AsyncClient(timeout=None) as client:
                    async with client.stream("GET", url, headers=headers) as response:
                        if response.status_code != 200:
                            if on_error:
                                await on_error(f"Connection failed: {response.status_code}")
                            await self._backoff()
                            continue

                        # Reset backoff on successful connection
                        self._reconnect_delay = 1

                        if on_connected:
                            await on_connected()

                        # Process SSE stream
                        await self._process_stream(response)

            except httpx.TimeoutException:
                # Normal timeout, reconnect
                continue
            except httpx.ConnectError as e:
                if on_error:
                    await on_error(f"Connection error: {e}")
                await self._backoff()
            except Exception as e:
                if on_error:
                    await on_error(f"Error: {e}")
                await self._backoff()

    async def _process_stream(self, response) -> None:
        """Process incoming SSE events from stream."""
        event_type = None
        event_data = ""

        async for line in response.aiter_lines():
            if not self._running:
                break

            line = line.strip()

            if not line:
                # Empty line = end of event
                if event_type and event_data:
                    await self._handle_event(event_type, event_data)
                event_type = None
                event_data = ""
                continue

            if line.startswith("event:"):
                event_type = line[6:].strip()
            elif line.startswith("data:"):
                event_data = line[5:].strip()
            elif line.startswith(":"):
                # Comment/keepalive, ignore
                pass

    async def _handle_event(self, event_type: str, event_data: str) -> None:
        """Handle a single SSE event."""
        try:
            data = json.loads(event_data)
        except json.JSONDecodeError:
            data = {"raw": event_data}

        # Call registered handlers
        handlers = self._handlers.get(event_type, [])
        handlers.extend(self._handlers.get("*", []))  # Wildcard handlers

        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(event_type, data)
                else:
                    handler(event_type, data)
            except Exception as e:
                print(f"Handler error for {event_type}: {e}")

        # Built-in handlers for local file updates
        await self._update_local_files(event_type, data)

    async def _update_local_files(self, event_type: str, data: dict) -> None:
        """Update local .vk/ files based on event."""
        if event_type == "task.updated":
            await self._update_task(data)
        elif event_type == "task.created":
            await self._add_task(data)
        elif event_type == "sprint.changed":
            await self._update_sprint(data)
        elif event_type == "content.updated":
            await self._update_content(data)

    async def _update_task(self, data: dict) -> None:
        """Update task status in local sprint file."""
        task_id = data.get("task_id")
        new_status = data.get("status")

        if not task_id or not new_status:
            return

        sprint_file = self.vk_dir / "sprints" / "current.yaml"
        if not sprint_file.exists():
            return

        try:
            with open(sprint_file) as f:
                sprint = yaml.safe_load(f) or {}

            # Find and update task
            for req in sprint.get("requirements", []):
                for task in req.get("tasks", []):
                    if task.get("task_id") == task_id:
                        task["status"] = new_status
                        if "updated_at" in data:
                            task["updated_at"] = data["updated_at"]
                        break

            # Write back
            with open(sprint_file, "w") as f:
                yaml.safe_dump(sprint, f, default_flow_style=False, sort_keys=False)

        except Exception as e:
            print(f"Error updating task: {e}")

    async def _add_task(self, data: dict) -> None:
        """Add new task to local sprint file."""
        # For new tasks, trigger a full pull for consistency
        # This is a simplified approach; could be enhanced to surgically add
        pass

    async def _update_sprint(self, data: dict) -> None:
        """Update sprint info in local files."""
        sprint_file = self.vk_dir / "sprints" / "current.yaml"
        if not sprint_file.exists():
            return

        try:
            with open(sprint_file) as f:
                sprint = yaml.safe_load(f) or {}

            # Update sprint-level fields
            for key in ["name", "goal", "status", "start_date", "end_date"]:
                if key in data:
                    sprint[key] = data[key]

            with open(sprint_file, "w") as f:
                yaml.safe_dump(sprint, f, default_flow_style=False, sort_keys=False)

        except Exception as e:
            print(f"Error updating sprint: {e}")

    async def _update_content(self, data: dict) -> None:
        """Handle content update notification."""
        content_type = data.get("content_type")
        name = data.get("name")

        if content_type and name:
            # Log the update; user can run 'vk pull' to get latest
            print(f"[sync] System content updated: {content_type}/{name}")

    async def _backoff(self) -> None:
        """Wait with exponential backoff before reconnecting."""
        await asyncio.sleep(self._reconnect_delay)
        self._reconnect_delay = min(
            self._reconnect_delay * 2,
            self._max_reconnect_delay,
        )

    def stop(self) -> None:
        """Stop the sync client."""
        self._running = False


async def watch_project(
    project_root: Optional[Path] = None,
    verbose: bool = True,
) -> None:
    """
    Watch a project for real-time updates.

    Convenience function that:
    1. Loads project config from .vk/config.yaml
    2. Gets auth token from keyring
    3. Connects to SSE and prints updates

    Args:
        project_root: Project root directory
        verbose: Print events to console
    """
    project_root = project_root or Path.cwd()
    vk_dir = project_root / ".vk"
    config_file = vk_dir / "config.yaml"

    if not config_file.exists():
        raise FileNotFoundError(
            "Project not initialized. Run 'vk init' first."
        )

    # Load project ID
    with open(config_file) as f:
        config = yaml.safe_load(f)
    project_id = config.get("project_id")

    if not project_id:
        raise ValueError("No project_id in config")

    # Get auth token
    try:
        from vk.auth import AuthClient
        auth = AuthClient()
        token = auth.get_token()
    except ImportError:
        raise ImportError("Auth module required for real-time sync")

    if not token:
        raise ValueError("Not authenticated. Run 'vk login' first.")

    # Create client
    client = RealtimeSyncClient(project_root)

    # Setup handlers if verbose
    if verbose:
        async def log_event(event_type: str, data: dict):
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] {event_type}: {json.dumps(data, indent=2)}")

        client.on("*", log_event)

    # Handle graceful shutdown
    loop = asyncio.get_event_loop()

    def shutdown():
        print("\n[sync] Stopping...")
        client.stop()

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, shutdown)

    # Connect and run
    async def on_connected():
        print(f"[sync] Connected to project {project_id}")
        print("[sync] Watching for updates... (Ctrl+C to stop)")

    async def on_error(msg: str):
        print(f"[sync] {msg}")

    await client.connect(
        project_id=project_id,
        auth_token=token,
        on_connected=on_connected,
        on_error=on_error,
    )
