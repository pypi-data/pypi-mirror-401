"""File management commands."""

import asyncio
import mimetypes
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from iseq_flow.api import APIError, ComputeAPIClient, FlowAPIClient, MinerAPIClient
from iseq_flow.config import require_project
from iseq_flow.curl import files_curl

console = Console()


def format_size(size: int | None) -> str:
    """Format file size for display."""
    if size is None:
        return "-"

    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.1f} {unit}" if unit != "B" else f"{size} {unit}"
        size /= 1024
    return f"{size:.1f} PB"


@click.group()
def files():
    """File operations (ls, download, upload)."""
    pass


@files.command("ls")
@click.option("--project", "-p", help="Project ID (uses default if not specified)")
@click.argument("path", default="")
@click.option("--curl", is_flag=True, help="Output curl command instead of executing")
def list_files(project: str | None, path: str, curl: bool):
    """List files and folders in a project.

    PATH is relative to the project's bucket (default: root).
    """
    project_id = require_project(project)

    if curl:
        params = {"path": path} if path else None
        print(files_curl("GET", "/files", project_id, params=params))
        return

    async def _list():
        client = FlowAPIClient()
        return await client.list_files(project_id, path)

    try:
        result = asyncio.run(_list())

        # Display bucket info
        console.print(f"[dim]Bucket:[/dim] {result.bucket_name}")
        if result.path:
            console.print(f"[dim]Path:[/dim] {result.path}")
        console.print()

        if not result.folders and not result.files:
            console.print("[yellow]No files or folders found.[/yellow]")
            return

        # Create table
        table = Table(show_header=True, header_style="bold")
        table.add_column("Type", width=6)
        table.add_column("Name")
        table.add_column("Size", justify="right")
        table.add_column("Modified")

        # Add folders first
        for folder in result.folders:
            table.add_row(
                "[blue]DIR[/blue]",
                f"[blue]{folder.display_name}/[/blue]",
                "-",
                "-",
            )

        # Add files
        for file in result.files:
            table.add_row(
                "[green]FILE[/green]",
                file.display_name,
                format_size(file.size),
                file.last_modified[:19] if file.last_modified else "-",
            )

        console.print(table)
        console.print()
        console.print(f"[dim]{len(result.folders)} folders, {len(result.files)} files[/dim]")

    except APIError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise SystemExit(1)


@files.command()
@click.option("--project", "-p", help="Project ID (uses default if not specified)")
@click.argument("path", required=False)
@click.option("--output", "-o", help="Local output path (default: filename from path)")
@click.option("--order-name", help="Order name to look up (use with --output-name)")
@click.option("--output-name", help="Semantic output name from meta.json (e.g., vcf, report)")
@click.option("--curl", is_flag=True, help="Output curl command instead of executing")
def download(
    project: str | None,
    path: str | None,
    output: str | None,
    order_name: str | None,
    output_name: str | None,
    curl: bool,
):
    """Download a file from the project.

    Two modes of operation:

    \b
    1. By path: flow files download PATH
       PATH is relative to the project's bucket.

    \b
    2. By semantic output: flow files download --order-name "Patient 001" --output-name vcf
       Looks up the order, finds the latest successful run, and downloads
       the output file matching the semantic name from meta.json.

    \b
    Examples:
      flow files download nf-results/run-123/output.vcf.gz
      flow files download --order-name "Case 001" --output-name vcf
      flow files download --order-name "Case 001" --output-name report -o report.html
    """
    project_id = require_project(project)

    # Validate arguments
    if order_name and output_name:
        # Semantic output download mode
        if path:
            console.print("[red]Error:[/red] Cannot specify PATH with --order-name/--output-name")
            raise SystemExit(1)
        _download_by_output(project_id, order_name, output_name, output, curl)
    elif path:
        # Direct path download mode
        if order_name or output_name:
            console.print("[red]Error:[/red] --order-name requires --output-name (and vice versa)")
            raise SystemExit(1)
        _download_by_path(project_id, path, output, curl)
    else:
        console.print("[red]Error:[/red] Must specify PATH or --order-name with --output-name")
        raise SystemExit(1)


def _download_by_path(project_id: str, path: str, output: str | None, curl: bool):
    """Download file by direct GCS path."""
    if curl:
        print(files_curl("GET", f"/files/download?path={path}", project_id))
        return

    async def _download():
        client = FlowAPIClient()

        # Get signed URL
        console.print("[dim]Getting download URL...[/dim]")
        url = await client.get_download_url(project_id, path)

        # Determine output path
        output_path = output or Path(path).name

        # Download file
        console.print(f"[dim]Downloading to {output_path}...[/dim]")
        await client.download_file(url, output_path)

        return output_path

    try:
        output_path = asyncio.run(_download())
        console.print(f"[green]Downloaded:[/green] {output_path}")

    except APIError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise SystemExit(1)


def _download_by_output(
    project_id: str, order_name: str, output_name: str, output: str | None, curl: bool
):
    """Download file by semantic output name from an order's run."""
    if curl:
        console.print("[yellow]Note:[/yellow] --curl not supported for semantic output download")
        console.print("This operation requires multiple API calls to resolve the output path.")
        return

    async def _download():
        miner_client = MinerAPIClient()
        compute_client = ComputeAPIClient()
        file_client = FlowAPIClient()

        # 1. Look up order by name
        console.print(f"[dim]Looking up order '{order_name}'...[/dim]")
        order = await miner_client.get_order_by_name(project_id, order_name)
        if not order:
            raise APIError(f"Order not found: {order_name}")
        console.print(f"[dim]Found order: {order.id}[/dim]")

        # 2. Get runs for this order
        console.print("[dim]Getting runs for order...[/dim]")
        runs = await compute_client.list_runs_by_order(order.id)
        if not runs:
            raise APIError(f"No runs found for order: {order_name}")

        # 3. Find the latest successful run
        successful_runs = [r for r in runs if r.status == "succeeded"]
        if not successful_runs:
            statuses = ", ".join(set(r.status for r in runs))
            raise APIError(f"No successful runs found for order (statuses: {statuses})")

        # Sort by created_at descending (most recent first)
        latest_run = sorted(successful_runs, key=lambda r: r.created_at or "", reverse=True)[0]
        console.print(f"[dim]Using run: {latest_run.name} ({latest_run.id})[/dim]")

        # 4. Get outputs for this run
        console.print("[dim]Getting run outputs...[/dim]")
        outputs = await compute_client.get_run_outputs(latest_run.id)
        if not outputs:
            raise APIError("No outputs found for run (may not be a WDL run)")

        # 5. Find matching output
        matching = [o for o in outputs if o.name == output_name]
        if not matching:
            available = ", ".join(o.name for o in outputs)
            raise APIError(f"Output '{output_name}' not found. Available: {available}")

        output_info = matching[0]
        if not output_info.path:
            raise APIError(f"Output '{output_name}' has no path")

        console.print(f"[dim]Found output: {output_info.display_name}[/dim]")
        console.print(f"[dim]Path: {output_info.path}[/dim]")

        # 6. Convert GCS path to relative path for download
        # output_info.path is like gs://bucket/prefix/path/to/file.vcf.gz
        gcs_path = output_info.path
        if not gcs_path.startswith("gs://"):
            raise APIError(f"Invalid output path format: {gcs_path}")

        # Parse bucket and path
        path_parts = gcs_path[5:].split("/", 1)  # Remove gs://
        if len(path_parts) < 2:
            raise APIError(f"Invalid GCS path: {gcs_path}")

        relative_path = path_parts[1]  # Path within bucket

        # 7. Get signed URL and download
        console.print("[dim]Getting download URL...[/dim]")
        url = await file_client.get_download_url(project_id, relative_path)

        # Determine output filename
        output_path = output or Path(relative_path).name

        console.print(f"[dim]Downloading to {output_path}...[/dim]")
        await file_client.download_file(url, output_path)

        return output_path

    try:
        output_path = asyncio.run(_download())
        console.print(f"[green]Downloaded:[/green] {output_path}")

    except APIError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise SystemExit(1)


@files.command()
@click.option("--project", "-p", help="Project ID (uses default if not specified)")
@click.argument("file", type=click.Path(exists=True))
@click.argument("remote_path")
@click.option("--curl", is_flag=True, help="Output curl command instead of executing")
def upload(project: str | None, file: str, remote_path: str, curl: bool):
    """Upload a file to the project.

    FILE is the local file to upload.
    REMOTE_PATH is the destination path relative to the project's bucket.
    """
    project_id = require_project(project)

    # Detect content type
    content_type, _ = mimetypes.guess_type(file)
    content_type = content_type or "application/octet-stream"

    if curl:
        print(files_curl(
            "POST",
            "/files/upload",
            project_id,
            data={"path": remote_path, "content_type": content_type},
        ))
        print("\n# Then upload to the returned signed URL:")
        print(f"# curl -X PUT -H 'Content-Type: {content_type}' \\")
        print(f"#   --data-binary @{file} '<signed_url>'")
        return

    async def _upload():
        client = FlowAPIClient()

        # Get signed URL
        console.print("[dim]Getting upload URL...[/dim]")
        url = await client.get_upload_url(project_id, remote_path, content_type)

        # Upload file
        file_size = Path(file).stat().st_size
        console.print(f"[dim]Uploading {format_size(file_size)}...[/dim]")
        await client.upload_file(url, file, content_type)

    try:
        asyncio.run(_upload())
        console.print(f"[green]Uploaded:[/green] {file} -> {remote_path}")

    except APIError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise SystemExit(1)
    except FileNotFoundError:
        console.print(f"[red]Error:[/red] File not found: {file}")
        raise SystemExit(1)
