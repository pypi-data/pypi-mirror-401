"""Run commands for iFlow CLI."""

import asyncio
import time

import click

from iflow.api import APIError, ComputeAPIClient
from iflow.config import require_project, resolve_gcs_path
from iflow.curl import compute_curl


@click.group()
def runs():
    """Manage pipeline runs."""
    pass


@runs.command("list")
@click.option("-p", "--project", help="Project ID (uses default if not specified)")
@click.option("-o", "--order-id", help="Filter by order ID")
@click.option("--limit", default=20, help="Maximum runs to display")
@click.option("--curl", is_flag=True, help="Output curl command instead of executing")
def list_runs(project: str | None, order_id: str | None, limit: int, curl: bool):
    """List runs for a project.

    \b
    Examples:
      iflow runs list
      iflow runs list --order-id ORDER_ID
    """
    project_id = require_project(project)

    if curl:
        params = {"project_id": project_id, "limit": str(limit)}
        if order_id:
            params["order_id"] = order_id
        print(compute_curl("GET", "/runs", params=params))
        return

    async def _list():
        client = ComputeAPIClient()
        try:
            if order_id:
                runs_list = await client.list_runs_by_order(order_id)
            else:
                runs_list = await client.list_runs(project_id, limit=limit)

            if not runs_list:
                click.echo("No runs found.")
                return

            # Print header
            click.echo(f"{'ID':<40} {'NAME':<35} {'STATUS':<12}")
            click.echo("-" * 90)

            for r in runs_list:
                click.echo(f"{r.id:<40} {r.name:<35} {r.status:<12}")

        except APIError as e:
            click.echo(f"Error: {e}", err=True)
            raise SystemExit(1)

    asyncio.run(_list())


@runs.command("submit")
@click.option("-p", "--project", help="Project ID (uses default if not specified)")
@click.option("--pipeline", required=True, help="Pipeline slug (e.g., nextflow-minimal)")
@click.option("--order-id", "-o", help="Order ID to associate with this run (from miner-service)")
@click.option("--param", "-P", multiple=True, help="Parameter in KEY=VALUE format")
@click.option("--tag", "-t", multiple=True, help="Tag for the run")
@click.option("--profile", help="Override Nextflow profile")
@click.option("--callback-url", help="URL to receive callback when run completes/fails (LIS integration)")
@click.option("--watch", is_flag=True, help="Watch run status after submission")
@click.option("--curl", is_flag=True, help="Output curl command instead of executing")
def submit_run(
    project: str | None,
    pipeline: str,
    order_id: str | None,
    param: tuple[str, ...],
    tag: tuple[str, ...],
    profile: str | None,
    callback_url: str | None,
    watch: bool,
    curl: bool,
):
    """Submit a new pipeline run.

    \b
    Examples:
      iflow runs submit --pipeline hereditary-mock \\
        -P case_id=patient-001 \\
        -P child_fastq=data/R1.fastq.gz \\
        -P child_fastq=data/R2.fastq.gz

      iflow runs submit --pipeline hereditary-mock \\
        --order-id ORDER_ID -P case_id=patient-001 --watch

      iflow runs submit --pipeline nextflow-minimal \\
        -P analysis_name=test --watch

      # With callback URL for LIS integration
      iflow runs submit --pipeline hereditary-mock \\
        -P case_id=patient-001 \\
        --callback-url https://lis.example.com/api/results
    """
    project_id = require_project(project)

    # Parse parameters - handle multiple values for same key
    # File paths are auto-resolved: relative paths get bucket prefix
    params = {}
    for p in param:
        if "=" not in p:
            click.echo(f"Invalid parameter format: {p} (use KEY=VALUE)", err=True)
            raise SystemExit(1)
        key, value = p.split("=", 1)

        # Resolve file paths (looks like a path if contains / or common extensions)
        file_exts = (".gz", ".fastq", ".fq", ".vcf", ".bam", ".cram", ".bed")
        if "/" in value or value.endswith(file_exts):
            value = resolve_gcs_path(value)

        if key in params:
            # Multiple values for same key - convert to list
            if isinstance(params[key], list):
                params[key].append(value)
            else:
                params[key] = [params[key], value]
        else:
            params[key] = value

    if curl:
        # For curl output, we need pipeline_id but we don't have it yet
        # Show with pipeline slug and note that it needs to be resolved
        data = {
            "project_id": project_id,
            "pipeline_slug": pipeline,
            "params": params,
        }
        if order_id:
            data["order_id"] = order_id
        if tag:
            data["tags"] = list(tag)
        if profile:
            data["profile"] = profile
        if callback_url:
            data["callback_url"] = callback_url
        print("# Note: pipeline_slug needs to be resolved to pipeline_id first")
        print(f"# GET {compute_curl('GET', f'/pipelines/{pipeline}')}")
        print()
        print(compute_curl("POST", "/runs", data=data))
        return

    async def _submit():
        client = ComputeAPIClient()
        try:
            # Get pipeline ID from slug
            pipeline_obj = await client.get_pipeline(pipeline)
            pipeline_id = pipeline_obj.id

            # Submit run
            run = await client.submit_run(
                project_id=project_id,
                pipeline_id=pipeline_id,
                order_id=order_id,
                params=params,
                tags=list(tag),
                profile=profile,
                callback_url=callback_url,
            )

            click.echo("Run submitted successfully!")
            click.echo(f"  ID: {run.id}")
            click.echo(f"  Name: {run.name}")
            click.echo(f"  Status: {run.status}")

            if watch:
                click.echo("\nWatching run status (Ctrl+C to stop)...")
                await _watch_run(client, run.id)

        except APIError as e:
            click.echo(f"Error: {e}", err=True)
            raise SystemExit(1)

    asyncio.run(_submit())


@runs.command("status")
@click.argument("run_id")
@click.option("--curl", is_flag=True, help="Output curl command instead of executing")
def run_status(run_id: str, curl: bool):
    """Get status of a run.

    RUN_ID is the run identifier.
    """
    if curl:
        print(compute_curl("GET", f"/runs/{run_id}"))
        return

    async def _status():
        client = ComputeAPIClient()
        try:
            run = await client.get_run(run_id)

            click.echo(f"Run: {run.name}")
            click.echo(f"  ID: {run.id}")
            click.echo(f"  Status: {run.status}")
            click.echo(f"  Pipeline ID: {run.pipeline_id}")
            if run.order_id:
                click.echo(f"  Order ID: {run.order_id}")
            click.echo(f"  Profile: {run.profile or 'default'}")

            if run.created_at:
                click.echo(f"  Created: {run.created_at}")
            if run.started_at:
                click.echo(f"  Started: {run.started_at}")
            if run.finished_at:
                click.echo(f"  Finished: {run.finished_at}")

            if run.output_path:
                click.echo(f"  Output: {run.output_path}")
            if run.error_message:
                click.echo(f"  Error: {run.error_message}")

            if run.params:
                click.echo("  Parameters:")
                for k, v in run.params.items():
                    click.echo(f"    {k}: {v}")

            if run.tags:
                click.echo(f"  Tags: {', '.join(run.tags)}")

        except APIError as e:
            click.echo(f"Error: {e}", err=True)
            raise SystemExit(1)

    asyncio.run(_status())


@runs.command("cancel")
@click.argument("run_id")
@click.option("--curl", is_flag=True, help="Output curl command instead of executing")
@click.confirmation_option(prompt="Are you sure you want to cancel this run?")
def cancel_run(run_id: str, curl: bool):
    """Cancel a running or queued run.

    RUN_ID is the run identifier.
    """
    if curl:
        print(compute_curl("POST", f"/runs/{run_id}/cancel"))
        return

    async def _cancel():
        client = ComputeAPIClient()
        try:
            await client.cancel_run(run_id)
            click.echo(f"Run {run_id} cancelled.")
        except APIError as e:
            click.echo(f"Error: {e}", err=True)
            raise SystemExit(1)

    asyncio.run(_cancel())


@runs.command("outputs")
@click.argument("run_id")
@click.option("--curl", is_flag=True, help="Output curl command instead of executing")
def run_outputs(run_id: str, curl: bool):
    """List semantic outputs of a run.

    Shows outputs mapped from meta.json definitions.
    Only available for WDL runs that have completed.

    \b
    Examples:
      iflow runs outputs RUN_ID
    """
    if curl:
        print(compute_curl("GET", f"/runs/{run_id}/outputs"))
        return

    async def _outputs():
        client = ComputeAPIClient()
        try:
            outputs = await client.get_run_outputs(run_id)

            if not outputs:
                click.echo("No outputs found (run may not have completed or is not a WDL run).")
                return

            # Print header
            click.echo(f"{'NAME':<20} {'TYPE':<10} {'PATH'}")
            click.echo("-" * 80)

            for output in outputs:
                path = output.path or "-"
                click.echo(f"{output.name:<20} {output.type:<10} {path}")

        except APIError as e:
            click.echo(f"Error: {e}", err=True)
            raise SystemExit(1)

    asyncio.run(_outputs())


@runs.command("watch")
@click.argument("run_id")
@click.option("--interval", default=10, help="Polling interval in seconds")
@click.option("--curl", is_flag=True, help="Output curl command instead of executing")
def watch_run(run_id: str, interval: int, curl: bool):
    """Watch run status until completion.

    RUN_ID is the run identifier.
    """
    if curl:
        print(f"# This command polls the following endpoint every {interval} seconds:")
        print(compute_curl("GET", f"/runs/{run_id}"))
        return

    async def _watch():
        client = ComputeAPIClient()
        try:
            await _watch_run(client, run_id, interval)
        except APIError as e:
            click.echo(f"Error: {e}", err=True)
            raise SystemExit(1)

    asyncio.run(_watch())


async def _watch_run(client: ComputeAPIClient, run_id: str, interval: int = 10):
    """Watch run status until terminal state."""
    terminal_statuses = {"succeeded", "failed", "cancelled"}
    last_status = None

    try:
        while True:
            run = await client.get_run(run_id)

            if run.status != last_status:
                timestamp = time.strftime("%H:%M:%S")
                click.echo(f"[{timestamp}] Status: {run.status}")
                last_status = run.status

                if run.status == "running" and run.started_at:
                    click.echo(f"           Started: {run.started_at}")

            if run.status in terminal_statuses:
                click.echo()
                if run.status == "succeeded":
                    click.echo("Run completed successfully!")
                    if run.output_path:
                        click.echo(f"Output: {run.output_path}")
                elif run.status == "failed":
                    click.echo(f"Run failed: {run.error_message or 'Unknown error'}")
                else:
                    click.echo("Run was cancelled.")
                break

            await asyncio.sleep(interval)

    except KeyboardInterrupt:
        click.echo("\nStopped watching (run continues in background).")
