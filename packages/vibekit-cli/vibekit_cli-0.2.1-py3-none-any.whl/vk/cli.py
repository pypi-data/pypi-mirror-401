#!/usr/bin/env python3
"""
VibeKit CLI - Configure in SaaS, execute locally.

Getting Started:
    pip install vksdk         # Install
    vk login                  # Authenticate
    vk init                   # Initialize project
    vk pull                   # Sync config from SaaS

Commands:
    vk login                  # Authenticate with vkcli.com
    vk logout                 # Clear authentication
    vk init                   # Initialize project
    vk link <slug>            # Link existing project
    vk pull                   # Pull config from SaaS
    vk push                   # Push status to SaaS
    vk status                 # View sync status
    vk open                   # Open in browser
    vk sprint                 # View current sprint
    vk done <task-id>         # Mark task complete

Documentation: https://vkcli.com/docs
"""

import hashlib
import subprocess
import webbrowser
from pathlib import Path
from typing import Optional

import typer
import yaml
from rich.console import Console
from rich.table import Table

app = typer.Typer(
    help="VibeKit - Configure in SaaS, execute locally | https://vkcli.com",
    add_completion=False,
)

console = Console()

# Project root - current working directory
PROJECT_ROOT = Path.cwd()


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def _get_vk_dir() -> Path:
    """Get .vk directory path."""
    return PROJECT_ROOT / ".vk"


def _get_config() -> Optional[dict]:
    """Load project config from .vk/config.yaml."""
    config_file = _get_vk_dir() / "config.yaml"
    if not config_file.exists():
        return None
    with open(config_file) as f:
        return yaml.safe_load(f)


def _save_config(config: dict) -> None:
    """Save project config to .vk/config.yaml."""
    config_file = _get_vk_dir() / "config.yaml"
    _get_vk_dir().mkdir(exist_ok=True)
    with open(config_file, "w") as f:
        yaml.dump(config, f, default_flow_style=False)


def _install_git_hooks() -> None:
    """Install git hooks for auto-sync on commit."""
    git_dir = PROJECT_ROOT / ".git"
    if not git_dir.exists():
        return

    hooks_dir = git_dir / "hooks"
    hooks_dir.mkdir(exist_ok=True)

    post_commit = hooks_dir / "post-commit"
    hook_content = """#!/bin/bash
# VibeKit Auto-Sync Hook
# Installed by: vk init

# Extract task IDs from commit message
TASKS=$(git log -1 --pretty=%B | grep -oE 'TASK-[0-9A-Za-z-]+' | sort -u)

# Mark each task as done
for task in $TASKS; do
    vk done "$task" --quiet 2>/dev/null
done

# Push changes to SaaS (background)
vk push --quiet 2>/dev/null &

exit 0
"""
    post_commit.write_text(hook_content)
    post_commit.chmod(0o755)


def _detect_project_from_git() -> Optional[str]:
    """Try to detect project from git remote."""
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
        )
        if result.returncode != 0:
            return None

        remote_url = result.stdout.strip()

        from vk.client import VKClient

        client = VKClient()
        if not client.is_authenticated():
            return None

        projects = client.projects.list()
        for project in projects:
            if project.get("git_url") == remote_url:
                return project.get("id")
            repo_name = remote_url.split("/")[-1].replace(".git", "")
            if project.get("name") == repo_name:
                return project.get("id")
        return None
    except Exception:
        return None


def _update_gitignore() -> None:
    """Add .vk/ cache files to .gitignore."""
    gitignore_path = PROJECT_ROOT / ".gitignore"
    ignore_entries = [
        "# VibeKit cache",
        ".vk/cache/",
        ".vk/context-cache.json",
    ]

    existing = ""
    if gitignore_path.exists():
        existing = gitignore_path.read_text()
        if ".vk/cache" in existing:
            return

    with open(gitignore_path, "a") as f:
        if existing and not existing.endswith("\n"):
            f.write("\n")
        f.write("\n".join(ignore_entries) + "\n")


# ============================================================================
# AUTH COMMANDS
# ============================================================================


@app.command()
def login():
    """
    Authenticate with vkcli.com using device flow.

    Opens browser for authentication and stores credentials locally.
    """
    console.print("\n[bold blue]🔐 VibeKit Login[/bold blue]")
    console.print("[blue]" + "━" * 50 + "[/blue]\n")

    from vk.auth import AuthClient

    auth = AuthClient()

    if auth.is_authenticated():
        token = auth.get_token()
        console.print(f"[green]Already logged in as {token.email}[/green]")
        console.print("[dim]Run 'vk logout' to switch accounts[/dim]")
        return

    success = auth.login()

    if success:
        console.print("\n[green]✅ Login successful![/green]")
        console.print("\n[bold]Next steps:[/bold]")
        console.print("  1. Run [cyan]vk init[/cyan] to initialize a project")
        console.print("  2. Or [cyan]vk link <slug>[/cyan] to link existing project")
    else:
        console.print("\n[red]❌ Login failed[/red]")
        raise typer.Exit(1)


@app.command()
def logout():
    """Log out and clear stored credentials."""
    console.print("\n[bold blue]🔓 VibeKit Logout[/bold blue]")
    console.print("[blue]" + "━" * 50 + "[/blue]\n")

    from vk.auth import AuthClient

    auth = AuthClient()
    auth.logout()
    console.print("[green]✅ Logged out successfully[/green]")


# ============================================================================
# PROJECT COMMANDS
# ============================================================================


@app.command()
def init():
    """
    Initialize project and authenticate with vkcli.com.

    This command:
    1. Opens browser for authentication (if needed)
    2. Registers project in SaaS
    3. Creates local .vk/ folder
    4. Pulls initial configuration

    After init, configure your project at vkcli.com, then run 'vk pull'.
    """
    console.print("\n[bold blue]🚀 VibeKit - Initialize Project[/bold blue]")
    console.print("[blue]" + "━" * 50 + "[/blue]\n")

    from vk.auth import AuthClient
    from vk.client import VKClient

    # Check if already initialized
    config = _get_config()
    if config and config.get("project_id"):
        console.print(f"[yellow]Project already initialized: {config.get('name')}[/yellow]")
        console.print(f"[dim]Project ID: {config.get('project_id')}[/dim]")
        console.print("\n[dim]Run 'vk pull' to sync or 'vk init --force' to reinitialize[/dim]")
        return

    # Ensure authenticated
    auth = AuthClient()
    if not auth.is_authenticated():
        console.print("[bold]Step 1: Authentication[/bold]")
        success = auth.login()
        if not success:
            console.print("[red]Authentication failed[/red]")
            raise typer.Exit(1)
    else:
        token = auth.get_token()
        console.print(f"[green]✓ Authenticated as {token.email}[/green]")

    # Detect project info
    console.print("\n[bold]Step 2: Project Detection[/bold]")

    project_name = PROJECT_ROOT.name
    git_remote = None

    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
        )
        if result.returncode == 0:
            git_remote = result.stdout.strip()
            console.print(f"  Git remote: {git_remote}")
    except Exception:
        pass

    console.print(f"  Project name: {project_name}")
    console.print(f"  Location: {PROJECT_ROOT}")

    # Check for existing project
    client = VKClient()
    existing_project = _detect_project_from_git()

    if existing_project:
        console.print(f"\n[green]Found existing project in SaaS![/green]")
        project_id = existing_project
        project = client.projects.get(project_id)
    else:
        # Create new project
        console.print("\n[bold]Step 3: Register Project[/bold]")

        # Detect languages
        languages = []
        if (PROJECT_ROOT / "pyproject.toml").exists() or (PROJECT_ROOT / "setup.py").exists():
            languages.append("python")
        if (PROJECT_ROOT / "package.json").exists():
            languages.append("javascript")
            if (PROJECT_ROOT / "tsconfig.json").exists():
                languages.append("typescript")
        if (PROJECT_ROOT / "go.mod").exists():
            languages.append("go")
        if (PROJECT_ROOT / "Cargo.toml").exists():
            languages.append("rust")

        console.print(f"  Detected languages: {', '.join(languages) or 'none'}")

        project = client.projects.create(
            name=project_name,
            path=str(PROJECT_ROOT),
            languages=languages or None,
        )
        project_id = project.get("id") or project.get("project_id")
        console.print(f"  [green]✓ Created project: {project_id}[/green]")

        # Update with git remote
        if git_remote:
            client.projects.update(project_id, git_remote_url=git_remote)

    # Save local config
    console.print("\n[bold]Step 4: Local Setup[/bold]")
    _get_vk_dir().mkdir(exist_ok=True)

    _save_config({
        "project_id": project_id,
        "project_slug": project.get("slug", f"project/{project_name}"),
        "name": project.get("name", project_name),
    })
    console.print("  [green]✓ Created .vk/config.yaml[/green]")

    # Update gitignore
    _update_gitignore()
    console.print("  [green]✓ Updated .gitignore[/green]")

    # Install git hooks
    _install_git_hooks()
    console.print("  [green]✓ Installed git hooks[/green]")

    # Pull initial config
    console.print("\n[bold]Step 5: Initial Sync[/bold]")
    from vk.sync import SyncClient

    sync = SyncClient(PROJECT_ROOT)
    result = sync.pull()

    if result.success:
        console.print(f"  [green]✓ Synced {len(result.files_synced)} files[/green]")
    else:
        console.print(f"  [yellow]⚠ Sync had issues: {result.errors}[/yellow]")

    # Success message
    config_url = project.get("config_url", f"https://vkcli.com/p/{project_id}")
    console.print("\n[green]" + "━" * 50 + "[/green]")
    console.print("[bold green]✅ Project initialized![/bold green]")
    console.print("\n[bold]Next steps:[/bold]")
    console.print(f"  1. Configure at: [link={config_url}]{config_url}[/link]")
    console.print("  2. Run [cyan]vk pull[/cyan] to sync changes")
    console.print("  3. Start coding!")


@app.command()
def link(
    identifier: str = typer.Argument(
        ...,
        help="Project slug (owner/name) or project ID",
    ),
):
    """
    Link an existing SaaS project to the current directory.

    Use this when you have a project configured in vkcli.com
    and want to connect it to a local directory.

    Examples:
        vk link myuser/myproject
        vk link 507f1f77bcf86cd799439011
    """
    console.print("\n[bold blue]🔗 VibeKit - Link Project[/bold blue]")
    console.print("[blue]" + "━" * 50 + "[/blue]\n")

    from vk.auth import AuthClient
    from vk.client import VKClient

    # Ensure authenticated
    auth = AuthClient()
    if not auth.is_authenticated():
        console.print("[red]Not authenticated. Run 'vk login' first.[/red]")
        raise typer.Exit(1)

    client = VKClient()

    # Fetch project
    console.print(f"Looking up project: {identifier}")

    try:
        if "/" in identifier:
            project = client.projects.get_by_slug(identifier)
        else:
            project = client.projects.get(identifier)
    except Exception as e:
        console.print(f"[red]Project not found: {e}[/red]")
        raise typer.Exit(1)

    project_id = project.get("id") or project.get("project_id")
    project_name = project.get("name", "Unknown")

    console.print(f"[green]✓ Found: {project_name}[/green]")

    # Save config
    _get_vk_dir().mkdir(exist_ok=True)
    _save_config({
        "project_id": project_id,
        "project_slug": project.get("slug", identifier),
        "name": project_name,
    })

    # Update gitignore and hooks
    _update_gitignore()
    _install_git_hooks()

    # Pull config
    console.print("\nPulling configuration...")
    from vk.sync import SyncClient

    sync = SyncClient(PROJECT_ROOT)
    result = sync.pull()

    if result.success:
        console.print(f"[green]✓ Synced {len(result.files_synced)} files[/green]")
    else:
        console.print(f"[yellow]⚠ {result.errors}[/yellow]")

    console.print("\n[green]✅ Project linked![/green]")
    console.print(f"[dim]Run 'vk pull' to sync updates[/dim]")


# ============================================================================
# SYNC COMMANDS
# ============================================================================


@app.command()
def pull():
    """
    Pull configuration from SaaS to local .vk/ folder.

    Downloads:
    - config.yaml: Project settings
    - sprints/current.yaml: Current sprint and tasks
    - rules/*.md: Coding rules and patterns
    - agents/*.yaml: Agent configurations
    - tools/*.yaml: Tool configurations

    Also generates CLAUDE.md for Claude Code integration.
    """
    console.print("\n[bold blue]📥 VibeKit - Pull from SaaS[/bold blue]")
    console.print("[blue]" + "━" * 50 + "[/blue]\n")

    from vk.sync import SyncClient

    sync = SyncClient(PROJECT_ROOT)

    if not sync.is_initialized():
        console.print("[red]Project not initialized. Run 'vk init' first.[/red]")
        raise typer.Exit(1)

    console.print("[bold]Syncing from SaaS...[/bold]")
    result = sync.pull()

    if result.success:
        console.print()
        console.print("[bold]Synced files:[/bold]")
        for f in result.files_synced:
            console.print(f"  [green]✓[/green] {f}")

        console.print("\n[green]✅ Pull complete![/green]")
        console.print("\n[dim]CLAUDE.md generated - Claude Code follows your rules.[/dim]")
    else:
        console.print(f"\n[red]❌ Pull failed:[/red]")
        for error in result.errors:
            console.print(f"  [red]• {error}[/red]")
        raise typer.Exit(1)


@app.command()
def push(
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Minimal output"),
):
    """
    Push local changes to SaaS.

    Syncs task status and progress back to vkcli.com dashboard.
    """
    if not quiet:
        console.print("\n[bold blue]📤 VibeKit - Push to SaaS[/bold blue]")
        console.print("[blue]" + "━" * 50 + "[/blue]\n")

    from vk.sync import SyncClient

    sync = SyncClient(PROJECT_ROOT)

    if not sync.is_initialized():
        if not quiet:
            console.print("[red]Project not initialized. Run 'vk init' first.[/red]")
        raise typer.Exit(1)

    result = sync.push()

    if result.success:
        if not quiet:
            console.print("[green]✅ Push complete![/green]")
            if result.files_synced:
                for f in result.files_synced:
                    console.print(f"  [green]✓[/green] {f}")
    else:
        if not quiet:
            console.print(f"[red]❌ Push failed: {result.errors}[/red]")
        raise typer.Exit(1)


@app.command()
def update():
    """
    Update local config and regenerate CLAUDE.md.

    Convenience command that runs pull and regenerates Claude integration.
    """
    console.print("\n[bold blue]🔄 VibeKit - Update[/bold blue]")
    console.print("[blue]" + "━" * 50 + "[/blue]\n")

    from vk.sync import SyncClient

    sync = SyncClient(PROJECT_ROOT)

    if not sync.is_initialized():
        console.print("[red]Project not initialized. Run 'vk init' first.[/red]")
        raise typer.Exit(1)

    # Pull latest
    console.print("[bold]Pulling latest config...[/bold]")
    result = sync.pull()

    if result.success:
        console.print(f"[green]✓ Synced {len(result.files_synced)} files[/green]")
    else:
        console.print(f"[yellow]⚠ {result.errors}[/yellow]")

    # Regenerate CLAUDE.md
    console.print("\n[bold]Regenerating CLAUDE.md...[/bold]")
    from vk.generator import ClaudeMdGenerator

    generator = ClaudeMdGenerator(PROJECT_ROOT)
    output_path = generator.generate()
    console.print(f"[green]✓ {output_path.name}[/green]")

    console.print("\n[green]✅ Update complete![/green]")


# ============================================================================
# STATUS COMMANDS
# ============================================================================


@app.command()
def status():
    """Show project and authentication status."""
    console.print("\n[bold blue]📊 VibeKit Status[/bold blue]")
    console.print("[blue]" + "━" * 50 + "[/blue]\n")

    from vk.auth import AuthClient

    # Auth status
    auth = AuthClient()
    console.print("[bold]Authentication:[/bold]")
    if auth.is_authenticated():
        token = auth.get_token()
        console.print(f"  [green]✓[/green] Logged in as {token.email}")
    else:
        console.print("  [red]✗[/red] Not authenticated")
        console.print("  [dim]Run 'vk login' to authenticate[/dim]")

    # Project status
    console.print("\n[bold]Project:[/bold]")
    config = _get_config()
    if config:
        console.print(f"  Name: {config.get('name', 'Unknown')}")
        console.print(f"  ID: {config.get('project_id', 'Unknown')}")
        console.print(f"  Slug: {config.get('project_slug', 'Unknown')}")
    else:
        console.print("  [yellow]Not initialized[/yellow]")
        console.print("  [dim]Run 'vk init' to initialize[/dim]")

    # Files status
    console.print("\n[bold]Local Files:[/bold]")
    vk_dir = _get_vk_dir()
    if vk_dir.exists():
        files = list(vk_dir.rglob("*"))
        file_count = len([f for f in files if f.is_file()])
        console.print(f"  [green]✓[/green] .vk/ exists ({file_count} files)")

        claude_md = PROJECT_ROOT / "CLAUDE.md"
        if claude_md.exists():
            console.print(f"  [green]✓[/green] CLAUDE.md exists")
        else:
            console.print(f"  [yellow]✗[/yellow] CLAUDE.md missing (run 'vk pull')")
    else:
        console.print("  [yellow]✗[/yellow] .vk/ not found")


@app.command(name="open")
def open_browser():
    """Open project in browser at vkcli.com."""
    config = _get_config()

    if not config or not config.get("project_id"):
        console.print("[red]Project not initialized. Run 'vk init' first.[/red]")
        raise typer.Exit(1)

    project_id = config["project_id"]
    url = f"https://vkcli.com/p/{project_id}"

    console.print(f"Opening: {url}")
    webbrowser.open(url)


# ============================================================================
# TASK COMMANDS
# ============================================================================


@app.command()
def sprint():
    """View current sprint status."""
    console.print("\n[bold blue]🏃 Current Sprint[/bold blue]")
    console.print("[blue]" + "━" * 50 + "[/blue]\n")

    sprint_file = _get_vk_dir() / "sprints" / "current.yaml"

    if not sprint_file.exists():
        console.print("[yellow]No active sprint.[/yellow]")
        console.print("[dim]Configure a sprint at vkcli.com, then run 'vk pull'[/dim]")
        return

    with open(sprint_file) as f:
        sprint_data = yaml.safe_load(f)

    if not sprint_data:
        console.print("[yellow]Sprint file is empty.[/yellow]")
        return

    # Sprint info
    console.print(f"[bold]{sprint_data.get('name', 'Unnamed Sprint')}[/bold]")
    if sprint_data.get("goal"):
        console.print(f"[dim]{sprint_data['goal']}[/dim]")

    # Tasks table
    tasks = sprint_data.get("tasks", [])
    if tasks:
        console.print()
        table = Table(show_header=True)
        table.add_column("ID", style="cyan")
        table.add_column("Title")
        table.add_column("Status", style="bold")
        table.add_column("Priority")

        for task in tasks:
            status = task.get("status", "pending")
            status_style = {
                "done": "[green]✓ done[/green]",
                "in_progress": "[yellow]▶ active[/yellow]",
                "pending": "[dim]○ pending[/dim]",
                "blocked": "[red]✗ blocked[/red]",
            }.get(status, status)

            table.add_row(
                task.get("id", "?"),
                task.get("title", "Untitled")[:50],
                status_style,
                task.get("priority", "-"),
            )

        console.print(table)

        # Summary
        done = len([t for t in tasks if t.get("status") == "done"])
        console.print(f"\n[bold]Progress:[/bold] {done}/{len(tasks)} tasks complete")
    else:
        console.print("\n[dim]No tasks in sprint.[/dim]")


@app.command()
def done(
    task_id: str = typer.Argument(..., help="Task ID to mark as complete"),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Minimal output"),
):
    """
    Mark a task as complete.

    Updates local sprint file and syncs to SaaS.
    """
    sprint_file = _get_vk_dir() / "sprints" / "current.yaml"

    if not sprint_file.exists():
        if not quiet:
            console.print("[red]No active sprint.[/red]")
        raise typer.Exit(1)

    with open(sprint_file) as f:
        sprint_data = yaml.safe_load(f) or {}

    tasks = sprint_data.get("tasks", [])
    task_found = False

    for task in tasks:
        if task.get("id") == task_id:
            task["status"] = "done"
            task_found = True
            break

    if not task_found:
        if not quiet:
            console.print(f"[red]Task not found: {task_id}[/red]")
        raise typer.Exit(1)

    # Save
    with open(sprint_file, "w") as f:
        yaml.dump(sprint_data, f, default_flow_style=False)

    if not quiet:
        console.print(f"[green]✓ Marked {task_id} as done[/green]")

    # Push to SaaS
    from vk.sync import SyncClient

    sync = SyncClient(PROJECT_ROOT)
    sync.push()

    if not quiet:
        console.print("[dim]Synced to SaaS[/dim]")


# ============================================================================
# MAIN
# ============================================================================


def main():
    """CLI entry point."""
    app()


if __name__ == "__main__":
    main()
