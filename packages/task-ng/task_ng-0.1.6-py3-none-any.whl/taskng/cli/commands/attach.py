"""Attachment CLI commands."""

import platform
import shutil
import subprocess
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from taskng.cli.display import format_size
from taskng.cli.output import is_json_mode, output_json
from taskng.config.settings import get_config, get_data_dir
from taskng.core.attachments import AttachmentService
from taskng.core.models import Attachment
from taskng.storage.database import Database
from taskng.storage.repository import TaskRepository

console = Console()


def attach_files(task_id: int, files: list[Path]) -> None:
    """Attach files to a task.

    Args:
        task_id: Task ID.
        files: List of file paths to attach.
    """
    db = Database()
    if not db.exists:
        console.print("[red]Database not initialized. Run 'task-ng init' first.[/red]")
        raise typer.Exit(1)

    repo = TaskRepository(db)
    task = repo.get_by_id(task_id)

    if not task:
        console.print(
            f"[red]Task {task_id} not found.[/red]\n"
            f"[dim]Use 'task-ng list' to see available tasks.[/dim]"
        )
        raise typer.Exit(1)

    service = AttachmentService(get_data_dir())
    attached: list[Attachment] = []

    # Get existing filenames for duplicate checking
    existing_names = {a.filename for a in task.attachments}

    for file_path in files:
        if not file_path.exists():
            console.print(
                f"[red]File not found: {file_path}[/red]\n"
                f"[dim]Check the path and try again.[/dim]"
            )
            continue

        if file_path.is_dir():
            console.print(
                f"[red]Cannot attach directory: {file_path}[/red]\n"
                f"[dim]Please attach individual files instead.[/dim]"
            )
            continue

        # Check for duplicate filename
        if file_path.name in existing_names:
            console.print(
                f"[yellow]Warning: Task already has attachment '{file_path.name}'[/yellow]"
            )
            if not typer.confirm("Continue? (both files will be kept)", default=False):
                continue

        # Check file size
        config = get_config()
        max_size = config.get("attachment.max_size", 104857600)  # Default 100MB
        file_size_check = file_path.stat().st_size

        if file_size_check > max_size:
            max_size_mb = max_size / (1024 * 1024)
            actual_size_mb = file_size_check / (1024 * 1024)
            console.print(f"[red]File too large: {file_path.name}[/red]")
            console.print(
                f"  Size: {actual_size_mb:.1f} MB (limit: {max_size_mb:.1f} MB)"
            )
            console.print(
                "[dim]Adjust with: task-ng config set attachment.max_size <bytes>[/dim]"
            )
            continue

        try:
            file_hash, file_size, mime_type = service.store_file(file_path)

            attachment = Attachment(
                task_uuid=task.uuid,
                filename=file_path.name,
                hash=file_hash,
                size=file_size,
                mime_type=mime_type,
            )
            saved = repo.add_attachment(attachment)
            attached.append(saved)

            console.print(
                f"Attached '[cyan]{file_path.name}[/cyan]' "
                f"({format_size(file_size)}) to task {task_id}"
            )
        except (
            FileNotFoundError,
            IsADirectoryError,
            ValueError,
            PermissionError,
            OSError,
        ) as e:
            console.print(
                f"[red]Failed to attach {file_path.name}: {e}[/red]\n"
                f"[dim]Ensure the file is readable and not locked.[/dim]"
            )
        except Exception as e:
            # Truly unexpected errors - re-raise for debugging
            console.print(
                f"[red]Unexpected error attaching {file_path.name}: {e}[/red]"
            )
            raise

    if is_json_mode():
        output_json([a.model_dump() for a in attached])


def list_attachments(task_id: int) -> None:
    """List attachments for a task.

    Args:
        task_id: Task ID.
    """
    db = Database()
    if not db.exists:
        console.print(f"[red]Task {task_id} not found[/red]")
        raise typer.Exit(1)

    repo = TaskRepository(db)
    task = repo.get_by_id(task_id)

    if not task:
        console.print(f"[red]Task {task_id} not found[/red]")
        raise typer.Exit(1)

    if is_json_mode():
        output_json([a.model_dump() for a in task.attachments])
        return

    if not task.attachments:
        console.print(f"No attachments for task {task_id}")
        return

    console.print(
        f'\nAttachments for task {task_id}: "[cyan]{task.description}[/cyan]"\n'
    )

    table = Table(show_header=True)
    table.add_column("#", style="dim", width=4)
    table.add_column("Filename")
    table.add_column("Size", justify="right")
    table.add_column("Added")

    for i, att in enumerate(task.attachments, 1):
        table.add_row(
            str(i),
            att.filename,
            format_size(att.size),
            att.entry.strftime("%Y-%m-%d"),
        )

    console.print(table)


def detach_file(task_id: int, target: str | None, all_: bool) -> None:
    """Remove attachment from a task.

    Args:
        task_id: Task ID.
        target: Attachment index (1-based) or filename.
        all_: Remove all attachments.
    """
    if not target and not all_:
        console.print("[red]Specify attachment index/filename or use --all[/red]")
        raise typer.Exit(1)

    db = Database()
    if not db.exists:
        console.print(f"[red]Task {task_id} not found[/red]")
        raise typer.Exit(1)

    repo = TaskRepository(db)
    task = repo.get_by_id(task_id)

    if not task:
        console.print(f"[red]Task {task_id} not found[/red]")
        raise typer.Exit(1)

    if all_:
        count = repo.delete_attachments_by_task(task.uuid)
        console.print(f"Removed {count} attachment(s) from task {task_id}")
        return

    # Find attachment by index or filename
    attachment = None
    if target and target.isdigit():
        index = int(target) - 1  # Convert to 0-based
        if 0 <= index < len(task.attachments):
            attachment = task.attachments[index]
    else:
        for att in task.attachments:
            if att.filename == target:
                attachment = att
                break

    if not attachment or attachment.id is None:
        console.print(f"[red]Attachment '{target}' not found[/red]")
        raise typer.Exit(1)

    repo.delete_attachment(attachment.id)
    console.print(f"Removed '[cyan]{attachment.filename}[/cyan]' from task {task_id}")


def open_attachment(task_id: int, target: str) -> None:
    """Open attachment with system default application.

    Args:
        task_id: Task ID.
        target: Attachment index (1-based) or filename.
    """
    db = Database()
    if not db.exists:
        console.print(f"[red]Task {task_id} not found[/red]")
        raise typer.Exit(1)

    repo = TaskRepository(db)
    task = repo.get_by_id(task_id)

    if not task:
        console.print(f"[red]Task {task_id} not found[/red]")
        raise typer.Exit(1)

    # Find attachment
    attachment = None
    if target.isdigit():
        index = int(target) - 1
        if 0 <= index < len(task.attachments):
            attachment = task.attachments[index]
    else:
        for att in task.attachments:
            if att.filename == target:
                attachment = att
                break

    if not attachment:
        console.print(f"[red]Attachment '{target}' not found[/red]")
        raise typer.Exit(1)

    service = AttachmentService(get_data_dir())
    file_path = service.get_path(attachment.hash)

    if not file_path.exists():
        console.print(f"[red]File missing from storage: {attachment.filename}[/red]")
        raise typer.Exit(1)

    console.print(f"Opening '[cyan]{attachment.filename}[/cyan]'...")
    _open_file(file_path)


def export_attachment_file(
    task_id: int, target: str, destination: Path | None, force: bool = False
) -> None:
    """Export attachment to filesystem.

    Args:
        task_id: Task ID.
        target: Attachment index (1-based) or filename.
        destination: Destination path (file or directory).
        force: Skip overwrite confirmation.
    """
    db = Database()
    if not db.exists:
        console.print(f"[red]Task {task_id} not found[/red]")
        raise typer.Exit(1)

    repo = TaskRepository(db)
    task = repo.get_by_id(task_id)

    if not task:
        console.print(f"[red]Task {task_id} not found[/red]")
        raise typer.Exit(1)

    # Find attachment
    attachment = None
    if target.isdigit():
        index = int(target) - 1
        if 0 <= index < len(task.attachments):
            attachment = task.attachments[index]
    else:
        for att in task.attachments:
            if att.filename == target:
                attachment = att
                break

    if not attachment:
        console.print(f"[red]Attachment '{target}' not found[/red]")
        raise typer.Exit(1)

    service = AttachmentService(get_data_dir())
    source_path = service.get_path(attachment.hash)

    if not source_path.exists():
        console.print(f"[red]File missing from storage: {attachment.filename}[/red]")
        raise typer.Exit(1)

    # Determine destination
    # Sanitize filename to prevent directory traversal attacks
    safe_filename = Path(attachment.filename).name
    if destination is None:
        dest_path = Path.cwd() / safe_filename
    elif destination.is_dir():
        dest_path = destination / safe_filename
    else:
        dest_path = destination

    # Check if destination exists and prompt for confirmation
    if dest_path.exists() and not force:
        existing_size = dest_path.stat().st_size
        new_size = attachment.size
        console.print(f"[yellow]Warning: File already exists: {dest_path}[/yellow]")
        console.print(
            f"  Existing: {format_size(existing_size)}, New: {format_size(new_size)}"
        )
        if not typer.confirm("Overwrite?", default=False):
            console.print("Export cancelled.")
            raise typer.Exit(0)

    shutil.copy2(source_path, dest_path)
    console.print(
        f"Exported '[cyan]{attachment.filename}[/cyan]' to {dest_path.absolute()}"
    )


def _open_file(path: Path) -> None:
    """Open file with system default application.

    Args:
        path: Path to file.
    """
    system = platform.system()
    try:
        if system == "Darwin":
            result = subprocess.run(["open", str(path)], capture_output=True, text=True)
        elif system == "Windows":
            result = subprocess.run(
                ["start", "", str(path)],
                shell=True,
                capture_output=True,
                text=True,
            )
        else:
            result = subprocess.run(
                ["xdg-open", str(path)], capture_output=True, text=True
            )

        if result.returncode != 0:
            console.print(
                f"[yellow]Warning: Could not open file (exit code {result.returncode})[/yellow]"
            )
            if result.stderr:
                console.print(f"[dim]{result.stderr.strip()}[/dim]")
    except FileNotFoundError:
        console.print("[red]Error: System file opener not found[/red]")
        console.print(f"[dim]File location: {path}[/dim]")
