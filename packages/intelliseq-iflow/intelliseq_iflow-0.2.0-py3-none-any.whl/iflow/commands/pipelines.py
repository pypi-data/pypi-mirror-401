"""Pipeline commands for iFlow CLI."""

import asyncio

import click

from iflow.api import APIError, ComputeAPIClient
from iflow.curl import compute_curl


@click.group()
def pipelines():
    """Manage pipelines."""
    pass


@pipelines.command("list")
@click.option("--curl", is_flag=True, help="Output curl command instead of executing")
def list_pipelines(curl: bool):
    """List available pipelines."""
    if curl:
        print(compute_curl("GET", "/pipelines"))
        return

    async def _list():
        client = ComputeAPIClient()
        try:
            pipelines_list = await client.list_pipelines()

            if not pipelines_list:
                click.echo("No pipelines found.")
                return

            # Print header
            click.echo(f"{'SLUG':<25} {'NAME':<25} {'MODE':<20} {'ACTIVE'}")
            click.echo("-" * 80)

            for p in pipelines_list:
                active = "Yes" if p.is_active else "No"
                click.echo(f"{p.slug:<25} {p.name:<25} {p.execution_mode:<20} {active}")

        except APIError as e:
            click.echo(f"Error: {e}", err=True)
            raise SystemExit(1)

    asyncio.run(_list())


@pipelines.command("info")
@click.argument("slug")
@click.option("--curl", is_flag=True, help="Output curl command instead of executing")
def pipeline_info(slug: str, curl: bool):
    """Get details about a pipeline.

    SLUG is the pipeline identifier (e.g., 'nextflow-minimal').
    """
    if curl:
        print(compute_curl("GET", f"/pipelines/{slug}"))
        return

    async def _info():
        client = ComputeAPIClient()
        try:
            p = await client.get_pipeline(slug)

            click.echo(f"Pipeline: {p.name}")
            click.echo(f"  Slug: {p.slug}")
            click.echo(f"  ID: {p.id}")
            click.echo(f"  Description: {p.description or 'N/A'}")
            click.echo(f"  Source Type: {p.source_type}")
            click.echo(f"  Execution Mode: {p.execution_mode}")
            click.echo(f"  Default Profile: {p.default_profile}")
            click.echo(f"  Active: {'Yes' if p.is_active else 'No'}")

        except APIError as e:
            click.echo(f"Error: {e}", err=True)
            raise SystemExit(1)

    asyncio.run(_info())
