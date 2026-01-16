"""Authentication commands."""

import asyncio

import click
from rich.console import Console

from iflow.auth import (
    AuthError,
    TokenInfo,
    clear_token,
    device_flow_login,
    get_stored_token,
    is_token_expired,
    password_login,
    store_token,
)

console = Console()


@click.command()
@click.option("--email", "-e", envvar="FLOW_EMAIL", help="Email for password auth (or set FLOW_EMAIL)")
@click.option("--password", "-p", envvar="FLOW_PASSWORD", help="Password for auth (or set FLOW_PASSWORD)")
@click.option("--token", "-t", envvar="FLOW_TOKEN", help="Personal Access Token for headless auth (or set FLOW_TOKEN)")
@click.option("--curl", is_flag=True, help="Output curl command instead of executing")
def login(email: str | None, password: str | None, token: str | None, curl: bool):
    """
    Login to Flow.

    \b
    By default uses OAuth Device Flow (opens browser).
    For headless/CI environments, use --token option with a PAT.

    \b
    Examples:
      iflow login                           # Interactive Device Flow
      iflow login --token YOUR_PAT          # PAT auth (recommended for CI)
      FLOW_TOKEN=YOUR_PAT iflow login       # Via env var
      iflow login -e user@example.com -p x  # Password auth (if ROPC enabled)
    """
    from iflow.config import get_settings

    settings = get_settings()

    if curl:
        if token:
            console.print("[yellow]Note:[/yellow] PAT login doesn't make an API call.")
            console.print("The token is stored locally for subsequent requests.")
            return

        if email and password:
            # Show ROPC token request
            console.print("# Password login (ROPC grant)")
            console.print(f"curl -s -X POST \\")
            console.print(f"  '{settings.zitadel_issuer}/oauth/v2/token' \\")
            console.print(f"  -d 'grant_type=password' \\")
            console.print(f"  -d 'client_id={settings.zitadel_client_id}' \\")
            console.print(f"  -d 'username={email}' \\")
            console.print(f"  -d 'password=YOUR_PASSWORD' \\")
            console.print(f"  -d 'scope=openid profile email offline_access urn:zitadel:iam:org:projects:roles'")
        else:
            # Show Device Flow step 1
            console.print("# Device Flow - Step 1: Get device code")
            console.print(f"curl -s -X POST \\")
            console.print(f"  '{settings.zitadel_issuer}/oauth/v2/device_authorization' \\")
            console.print(f"  -d 'client_id={settings.zitadel_client_id}' \\")
            console.print(f"  -d 'scope=openid profile email offline_access urn:zitadel:iam:org:projects:roles'")
            console.print()
            console.print("# Then visit verification_uri with user_code")
            console.print("# Device Flow - Step 2: Poll for token")
            console.print(f"curl -s -X POST \\")
            console.print(f"  '{settings.zitadel_issuer}/oauth/v2/token' \\")
            console.print(f"  -d 'grant_type=urn:ietf:params:oauth:grant-type:device_code' \\")
            console.print(f"  -d 'client_id={settings.zitadel_client_id}' \\")
            console.print(f"  -d 'device_code=DEVICE_CODE_FROM_STEP_1'")
        return

    import time

    try:
        if token:
            # Use Personal Access Token directly
            console.print("[dim]Using Personal Access Token...[/dim]")
            token_info = TokenInfo(
                access_token=token,
                refresh_token=None,
                expires_at=time.time() + 86400 * 365,  # Assume 1 year validity
                token_type="Bearer",
            )
            store_token(token_info)
            console.print()
            console.print("[green]Successfully logged in with PAT![/green]")
            return

        if email and password:
            # Use password-based authentication (ROPC)
            console.print(f"[dim]Logging in as {email}...[/dim]")
            token_info = asyncio.run(password_login(email, password))
        else:
            # Use Device Flow (interactive)
            token_info = asyncio.run(device_flow_login())

        store_token(token_info)
        console.print()
        console.print("[green]Successfully logged in![/green]")
    except AuthError as e:
        console.print(f"[red]Login failed:[/red] {e}")
        raise SystemExit(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Login cancelled.[/yellow]")
        raise SystemExit(1)


@click.command()
def logout():
    """Logout and clear stored credentials."""
    clear_token()
    console.print("[green]Logged out successfully.[/green]")


@click.command()
def status():
    """Show current authentication status."""
    token = get_stored_token()

    if not token:
        console.print("[yellow]Not logged in.[/yellow]")
        console.print("Run [bold]iflow login[/bold] to authenticate.")
        return

    if is_token_expired(token):
        console.print("[yellow]Token expired.[/yellow]")
        console.print("Run [bold]iflow login[/bold] to re-authenticate.")
        return

    console.print("[green]Logged in.[/green]")

    # Try to decode token to show user info
    try:
        import base64
        import json

        # Decode JWT payload (middle part)
        payload_b64 = token.access_token.split(".")[1]
        # Add padding if needed
        payload_b64 += "=" * (4 - len(payload_b64) % 4)
        payload = json.loads(base64.urlsafe_b64decode(payload_b64))

        if "email" in payload:
            console.print(f"User: [cyan]{payload['email']}[/cyan]")
        elif "sub" in payload:
            console.print(f"Subject: [cyan]{payload['sub']}[/cyan]")

    except Exception:
        pass  # Don't fail if we can't decode token
