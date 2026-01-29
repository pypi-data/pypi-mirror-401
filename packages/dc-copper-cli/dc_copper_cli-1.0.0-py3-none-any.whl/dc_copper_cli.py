#!/usr/bin/env python3
"""Copper CRM CLI.

CRUD operations for Copper CRM: leads, people, opportunities, companies, and custom fields.

Usage:
    copper [global flags] <resource> <action> [args] [flags]

Resources: lead, person, opportunity, company, field
"""

from __future__ import annotations

import json
import os
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

import click
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

try:
    import tomli
except ImportError:
    tomli = None

try:
    import tomli_w
except ImportError:
    tomli_w = None

from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.table import Table

# Exit codes per spec
EXIT_SUCCESS = 0
EXIT_ERROR = 1
EXIT_USAGE = 2
EXIT_AUTH = 3
EXIT_NOT_FOUND = 4
EXIT_RATE_LIMITED = 5

# API constants
API_BASE_URL = "https://api.copper.com/developer_api/v1"
RETRY_ATTEMPTS = 3
RETRY_BACKOFF_FACTOR = 2
TIMEOUT = 30

# Config paths
CONFIG_DIR = Path.home() / ".config" / "copper"
CONFIG_FILE = CONFIG_DIR / "config.toml"
PROJECT_CONFIG = Path(".copper.toml")


class CopperConfig:
    """Configuration loader with precedence: flags > env > project config > user config."""

    def __init__(self) -> None:
        """Initialize configuration from files and environment."""
        self.api_key: str | None = None
        self.email: str | None = None
        self.defaults: dict[str, Any] = {"limit": 25, "output": "table"}
        self._load()

    def _load(self) -> None:
        # Load user config
        if CONFIG_FILE.exists() and tomli:
            with open(CONFIG_FILE, "rb") as f:
                data = tomli.load(f)
                self.api_key = data.get("api_key")
                self.email = data.get("email")
                self.defaults.update(data.get("defaults", {}))

        # Load project config (overrides user)
        if PROJECT_CONFIG.exists() and tomli:
            with open(PROJECT_CONFIG, "rb") as f:
                data = tomli.load(f)
                if "api_key" in data:
                    self.api_key = data["api_key"]
                if "email" in data:
                    self.email = data["email"]
                self.defaults.update(data.get("defaults", {}))

        # Env vars override config files
        if os.getenv("COPPER_API_KEY"):
            self.api_key = os.getenv("COPPER_API_KEY")
        if os.getenv("COPPER_EMAIL"):
            self.email = os.getenv("COPPER_EMAIL")

    def save_user_config(self) -> None:
        """Save current config to user config file."""
        if not tomli_w:
            return
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        data = {}
        if self.api_key:
            data["api_key"] = self.api_key
        if self.email:
            data["email"] = self.email
        if self.defaults:
            data["defaults"] = self.defaults
        with open(CONFIG_FILE, "wb") as f:
            tomli_w.dump(data, f)


class Context:
    """Click context object for global state."""

    def __init__(self) -> None:
        """Initialize context with default settings."""
        self.config = CopperConfig()
        self.console = Console()
        self.json_output = False
        self.quiet = False
        self.verbose = False
        self.no_input = False
        self.client: CopperAPIClient | None = None

    def get_client(self) -> CopperAPIClient:
        """Get or create API client instance."""
        if self.client is None:
            if not self.config.api_key:
                self.error("Missing COPPER_API_KEY", EXIT_AUTH)
            if not self.config.email:
                self.error("Missing COPPER_EMAIL", EXIT_AUTH)
            self.client = CopperAPIClient(self.config.api_key, self.config.email, self)
        return self.client

    def output(self, data: Any, table_fn: Callable | None = None) -> None:
        """Output data as JSON or table based on flags."""
        if self.json_output:
            click.echo(json.dumps(data, indent=2, default=str))
        elif table_fn and not self.quiet:
            table_fn(data)
        elif not self.quiet:
            click.echo(json.dumps(data, indent=2, default=str))

    def info(self, msg: str) -> None:
        """Print info message if not quiet."""
        if not self.quiet:
            self.console.print(msg)

    def debug(self, msg: str) -> None:
        """Print debug message if verbose."""
        if self.verbose:
            self.console.print(f"[dim]{msg}[/dim]", err=True)

    def warn(self, msg: str) -> None:
        """Print warning message to stderr."""
        self.console.print(f"[yellow]{msg}[/yellow]", err=True)

    def error(self, msg: str, exit_code: int = EXIT_ERROR) -> None:
        """Print error message and exit."""
        self.console.print(f"[red]Error: {msg}[/red]", err=True)
        sys.exit(exit_code)

    def confirm(self, msg: str, default: bool = False) -> bool:
        """Prompt for confirmation, respecting --no-input."""
        if self.no_input:
            return default
        return Confirm.ask(msg, default=default)

    def prompt(self, msg: str, default: str = "") -> str:
        """Prompt for input, respecting --no-input."""
        if self.no_input:
            if default:
                return default
            self.error("Prompt required but --no-input specified", EXIT_USAGE)
        return Prompt.ask(msg, default=default)


class CopperAPIClient:
    """Copper CRM API client with retry logic."""

    def __init__(self, api_key: str, email: str, ctx: Context) -> None:
        """Initialize API client with credentials."""
        self.api_key = api_key
        self.email = email
        self.ctx = ctx
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        session = requests.Session()
        retry = Retry(
            total=RETRY_ATTEMPTS,
            backoff_factor=RETRY_BACKOFF_FACTOR,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "DELETE"],
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def _headers(self) -> dict[str, str]:
        return {
            "X-PW-AccessToken": self.api_key,
            "X-PW-Application": "developer_api",
            "X-PW-UserEmail": self.email,
            "Content-Type": "application/json",
        }

    def _handle_response(self, resp: requests.Response) -> Any:
        self.ctx.debug(f"HTTP {resp.status_code} {resp.request.method} {resp.url}")

        if resp.status_code == 401:
            self.ctx.error("Authentication failed", EXIT_AUTH)
        if resp.status_code == 404:
            self.ctx.error("Resource not found", EXIT_NOT_FOUND)
        if resp.status_code == 429:
            retry_after = resp.headers.get("Retry-After", "unknown")
            self.ctx.error(
                f"Rate limited. Retry after {retry_after}s", EXIT_RATE_LIMITED
            )
        if resp.status_code == 422:
            try:
                err = resp.json()
                self.ctx.error(f"Validation error: {err}", EXIT_USAGE)
            except Exception:
                self.ctx.error("Validation error", EXIT_USAGE)

        resp.raise_for_status()

        if resp.status_code == 204:
            return None
        try:
            return resp.json()
        except Exception:
            return None

    def get(self, endpoint: str, params: dict | None = None) -> Any:
        """Make GET request to API endpoint."""
        url = f"{API_BASE_URL}{endpoint}"
        self.ctx.debug(f"GET {url}")
        resp = self.session.get(
            url, headers=self._headers(), params=params, timeout=TIMEOUT
        )
        return self._handle_response(resp)

    def post(self, endpoint: str, data: dict) -> Any:
        """Make POST request to API endpoint."""
        url = f"{API_BASE_URL}{endpoint}"
        self.ctx.debug(f"POST {url}")
        resp = self.session.post(
            url, headers=self._headers(), json=data, timeout=TIMEOUT
        )
        return self._handle_response(resp)

    def put(self, endpoint: str, data: dict) -> Any:
        """Make PUT request to API endpoint."""
        url = f"{API_BASE_URL}{endpoint}"
        self.ctx.debug(f"PUT {url}")
        resp = self.session.put(
            url, headers=self._headers(), json=data, timeout=TIMEOUT
        )
        return self._handle_response(resp)

    def delete(self, endpoint: str) -> Any:
        """Make DELETE request to API endpoint."""
        url = f"{API_BASE_URL}{endpoint}"
        self.ctx.debug(f"DELETE {url}")
        resp = self.session.delete(url, headers=self._headers(), timeout=TIMEOUT)
        return self._handle_response(resp)


pass_context = click.make_pass_decorator(Context, ensure=True)


def parse_fields(field_args: tuple[str, ...]) -> dict[str, Any]:
    """Parse --field KEY=VAL arguments into a dict."""
    result = {}
    for f in field_args:
        if "=" not in f:
            continue
        key, val = f.split("=", 1)
        # Try to parse as int/float
        try:
            result[key.strip()] = int(val)
        except ValueError:
            try:
                result[key.strip()] = float(val)
            except ValueError:
                result[key.strip()] = val.strip()
    return result


def make_table(records: list[dict], columns: list[str], title: str = "") -> Table:
    """Create a rich table from records."""
    table = Table(title=title)
    table.add_column("ID", style="cyan")
    for col in columns:
        table.add_column(col.replace("_", " ").title())

    for rec in records:
        row = [str(rec.get("id", ""))]
        for col in columns:
            val = rec.get(col, "")
            if isinstance(val, (dict, list)):
                val = json.dumps(val)[:40]
            row.append(str(val)[:50] if val else "")
        table.add_row(*row)

    return table


# ============================================================================
# CLI Root
# ============================================================================


@click.group()
@click.option(
    "--version",
    is_flag=True,
    is_eager=True,
    expose_value=False,
    callback=lambda ctx, param, val: (
        click.echo("copper 1.0.0") or ctx.exit() if val else None
    ),
    help="Show version",
)
@click.option("--json", "json_output", is_flag=True, help="Output as JSON")
@click.option("-q", "--quiet", is_flag=True, help="Suppress non-essential output")
@click.option("-v", "--verbose", is_flag=True, help="Verbose output")
@click.option("--no-color", is_flag=True, help="Disable colors")
@click.option("--no-input", is_flag=True, help="Fail instead of prompting")
@click.option("--config", "config_path", type=click.Path(), help="Config file path")
@click.pass_context
def cli(click_ctx, json_output, quiet, verbose, no_color, no_input, config_path):
    """Copper CRM CLI - Manage your CRM data from the command line."""
    ctx = Context()
    ctx.json_output = json_output
    ctx.quiet = quiet
    ctx.verbose = verbose
    ctx.no_input = no_input

    if no_color or os.getenv("NO_COLOR"):
        ctx.console = Console(force_terminal=False, no_color=True)

    if config_path:
        # Override config path
        global CONFIG_FILE
        CONFIG_FILE = Path(config_path)
        ctx.config = CopperConfig()

    click_ctx.obj = ctx


# ============================================================================
# Config commands
# ============================================================================


@cli.group()
def config():
    """Manage configuration."""
    pass


@config.command("init")
@pass_context
def config_init(ctx: Context):
    """Interactive configuration setup."""
    ctx.info("[bold]Copper CLI Configuration[/bold]\n")

    api_key = ctx.prompt("API Key", ctx.config.api_key or "")
    email = ctx.prompt("Email", ctx.config.email or "")

    ctx.config.api_key = api_key
    ctx.config.email = email
    ctx.config.save_user_config()

    ctx.info(f"\n[green]Config saved to {CONFIG_FILE}[/green]")


@config.command("show")
@pass_context
def config_show(ctx: Context):
    """Display current configuration."""
    data = {
        "api_key": "***" + ctx.config.api_key[-4:] if ctx.config.api_key else None,
        "email": ctx.config.email,
        "config_file": str(CONFIG_FILE),
        "defaults": ctx.config.defaults,
    }
    ctx.output(data)


@config.command("set")
@click.argument("key")
@click.argument("value")
@pass_context
def config_set(ctx: Context, key: str, value: str):
    """Set a configuration value."""
    if key == "api_key":
        ctx.config.api_key = value
    elif key == "email":
        ctx.config.email = value
    elif key.startswith("defaults."):
        subkey = key.replace("defaults.", "")
        ctx.config.defaults[subkey] = value
    else:
        ctx.error(f"Unknown config key: {key}", EXIT_USAGE)

    ctx.config.save_user_config()
    ctx.info(f"[green]Set {key}[/green]")


# ============================================================================
# Auth commands
# ============================================================================


@cli.command("auth")
@pass_context
def auth_status(ctx: Context):
    """Check authentication status."""
    try:
        client = ctx.get_client()
        # Try a simple API call
        result = client.get("/account")
        ctx.output(
            {
                "authenticated": True,
                "account": result.get("name") if result else None,
                "email": ctx.config.email,
            }
        )
    except SystemExit:
        raise
    except Exception as e:
        ctx.output({"authenticated": False, "error": str(e)})
        sys.exit(EXIT_AUTH)


# ============================================================================
# Resource command factory
# ============================================================================


def create_resource_group(
    name: str,
    endpoint: str,
    display_columns: list[str],
    create_fields: list[str],
) -> click.Group:
    """Factory to create resource command groups (lead, person, etc.)."""

    @cli.group(name=name)
    def resource_group():
        f"""Manage {name}s."""
        pass

    @resource_group.command("list")
    @click.option("--limit", "-l", default=25, type=int, help="Results per page")
    @click.option("--page", "-p", default=1, type=int, help="Page number")
    @click.option("--all", "fetch_all", is_flag=True, help="Fetch all pages")
    @click.option("--sort", help="Sort by field")
    @click.option("--order", type=click.Choice(["asc", "desc"]), default="desc")
    @click.option("-f", "--filter", "filters", multiple=True, help="Filter KEY=VAL (passed to API search endpoint)")
    @pass_context
    def list_cmd(ctx: Context, limit, page, fetch_all, sort, order, filters):
        f"""List {name}s."""
        client = ctx.get_client()

        # Show initial feedback
        if not ctx.quiet and not ctx.json_output:
            ctx.info(f"[dim]Searching {name}s...[/dim]")

        # Build search body (Copper uses POST for search)
        body: dict[str, Any] = {
            "page_size": min(limit, 200),
            "page_number": page,
        }

        if sort:
            body["sort_by"] = sort
            body["sort_direction"] = order

        # Parse filters
        for f in filters:
            if "=" in f:
                k, v = f.split("=", 1)
                body[k.strip()] = v.strip()

        if fetch_all:
            all_records = []
            page_num = 1
            show_progress = sys.stdout.isatty() and not ctx.quiet and not ctx.json_output
            while True:
                body["page_number"] = page_num
                if show_progress:
                    ctx.console.print(f"[dim]Fetching page {page_num}...[/dim]", file=sys.stderr)
                records = client.post(f"{endpoint}/search", body)
                if not records:
                    break
                all_records.extend(records)
                if len(records) < body["page_size"]:
                    break
                page_num += 1

            records = all_records
            if show_progress:
                ctx.console.print(f"[dim]✓ Fetched {len(records)} records[/dim]", file=sys.stderr)
        else:
            records = client.post(f"{endpoint}/search", body)

        if not records:
            records = []

        def show_table(data):
            table = make_table(data, display_columns, f"{name.title()}s")
            ctx.console.print(table)
            ctx.info(f"\n[cyan]{len(data)} record(s)[/cyan]")

        ctx.output(records, show_table)

    @resource_group.command("get")
    @click.argument("id", type=int)
    @pass_context
    def get_cmd(ctx: Context, id: int):
        f"""Get a {name} by ID."""
        client = ctx.get_client()
        record = client.get(f"{endpoint}/{id}")

        def show_record(data):
            table = Table(title=f"{name.title()} #{id}", show_header=False)
            table.add_column("Field", style="cyan")
            table.add_column("Value")
            for k, v in data.items():
                if isinstance(v, (dict, list)):
                    v = json.dumps(v, indent=2)
                table.add_row(k, str(v) if v is not None else "")
            ctx.console.print(table)

        ctx.output(record, show_record)

    @resource_group.command("create")
    @click.option("--name", "rec_name", help="Name")
    @click.option("--email", help="Email address")
    @click.option("--phone", help="Phone number")
    @click.option("--company", type=int, help="Company ID")
    @click.option("--owner", type=int, help="Owner user ID")
    @click.option("--field", "fields", multiple=True, help="Custom field KEY=VAL")
    @click.option(
        "--from-json",
        "json_file",
        type=click.Path(),
        help="Read from JSON file (use '-' for stdin)",
    )
    @pass_context
    def create_cmd(
        ctx: Context, rec_name, email, phone, company, owner, fields, json_file
    ):
        f"""Create a new {name}."""
        client = ctx.get_client()

        if json_file:
            if json_file == "-":
                data = json.load(sys.stdin)
            else:
                with open(json_file) as f:
                    data = json.load(f)
        else:
            data = {}
            if rec_name:
                data["name"] = rec_name
            if email:
                if name == "person":
                    data["emails"] = [{"email": email, "category": "work"}]
                else:
                    data["email"] = {"email": email, "category": "work"}
            if phone:
                if name == "person":
                    data["phone_numbers"] = [{"number": phone, "category": "work"}]
                else:
                    data["phone"] = phone
            if company:
                data["company_id"] = company
            if owner:
                data["assignee_id"] = owner

        # Add custom fields
        if fields:
            custom = parse_fields(fields)
            if custom:
                data["custom_fields"] = [
                    {"custom_field_definition_id": k, "value": v}
                    for k, v in custom.items()
                ]

        if not data:
            ctx.error("No data provided. Use flags or --from-json", EXIT_USAGE)

        result = client.post(endpoint, data)
        ctx.info(f"[green]Created {name} #{result.get('id')}[/green]")
        ctx.output(result)

    @resource_group.command("update")
    @click.argument("id", type=int)
    @click.option("--name", "rec_name", help="Name")
    @click.option("--email", help="Email address")
    @click.option("--phone", help="Phone number")
    @click.option("--company", type=int, help="Company ID")
    @click.option("--owner", type=int, help="Owner user ID")
    @click.option("--field", "fields", multiple=True, help="Custom field KEY=VAL")
    @click.option(
        "--from-json", "json_file", type=click.Path(), help="Read from JSON file (use '-' for stdin)"
    )
    @pass_context
    def update_cmd(
        ctx: Context, id, rec_name, email, phone, company, owner, fields, json_file
    ):
        f"""Update a {name}."""
        client = ctx.get_client()

        if json_file:
            if json_file == "-":
                data = json.load(sys.stdin)
            else:
                with open(json_file) as f:
                    data = json.load(f)
        else:
            data = {}
            if rec_name:
                data["name"] = rec_name
            if email:
                if name == "person":
                    data["emails"] = [{"email": email, "category": "work"}]
                else:
                    data["email"] = {"email": email, "category": "work"}
            if phone:
                data["phone"] = phone
            if company:
                data["company_id"] = company
            if owner:
                data["assignee_id"] = owner

        if fields:
            custom = parse_fields(fields)
            if custom:
                data["custom_fields"] = [
                    {"custom_field_definition_id": k, "value": v}
                    for k, v in custom.items()
                ]

        if not data:
            ctx.error("No updates provided", EXIT_USAGE)

        result = client.put(f"{endpoint}/{id}", data)
        ctx.info(f"[green]Updated {name} #{id}[/green]")
        ctx.output(result)

    @resource_group.command("delete")
    @click.argument("id", type=int)
    @click.option("--force", is_flag=True, help="Skip confirmation prompt")
    @click.option("--dry-run", is_flag=True, help="Show what would be deleted without deleting")
    @pass_context
    def delete_cmd(ctx: Context, id: int, force: bool, dry_run: bool):
        f"""Delete a {name}."""
        client = ctx.get_client()

        # Fetch first to show what we're deleting
        record = client.get(f"{endpoint}/{id}")

        if dry_run:
            ctx.info(f"[yellow]Would delete {name} #{id}:[/yellow]")
            ctx.output(record)
            return

        if not force:
            ctx.info(f"[red]About to delete {name} #{id}:[/red]")
            ctx.output(record)
            if not ctx.confirm("\nConfirm delete?", default=False):
                ctx.info("[yellow]Cancelled[/yellow]")
                return

        client.delete(f"{endpoint}/{id}")
        ctx.info(f"[green]Deleted {name} #{id}[/green]")

    return resource_group


# ============================================================================
# Create resource groups
# ============================================================================

create_resource_group(
    "lead", "/leads", ["name", "email", "status"], ["name", "email", "phone"]
)
create_resource_group(
    "person", "/people", ["name", "emails", "company_id"], ["name", "email", "phone"]
)
create_resource_group(
    "company", "/companies", ["name", "email", "phone"], ["name", "email", "phone"]
)
create_resource_group(
    "opportunity",
    "/opportunities",
    ["name", "status", "monetary_value"],
    ["name", "status", "value"],
)


# ============================================================================
# Custom Fields
# ============================================================================


@cli.group("field")
def field_group():
    """Manage custom field definitions."""
    pass


@field_group.command("list")
@pass_context
def field_list(ctx: Context):
    """List custom field definitions."""
    client = ctx.get_client()
    result = client.get("/custom_field_definitions")

    def show_table(data):
        table = Table(title="Custom Fields")
        table.add_column("ID", style="cyan")
        table.add_column("Name")
        table.add_column("Type")
        table.add_column("Entity")
        for field in data:
            table.add_row(
                str(field.get("id", "")),
                field.get("name", ""),
                field.get("data_type", ""),
                ", ".join(field.get("available_on", [])),
            )
        ctx.console.print(table)

    ctx.output(result, show_table)


@field_group.command("get")
@click.argument("id", type=int)
@pass_context
def field_get(ctx: Context, id: int):
    """Get a custom field definition by ID."""
    client = ctx.get_client()
    # Copper doesn't have a single-field endpoint, so we filter from list
    result = client.get("/custom_field_definitions")
    field = next((f for f in result if f.get("id") == id), None)
    if not field:
        ctx.error(f"Field {id} not found", EXIT_NOT_FOUND)
    ctx.output(field)


@field_group.command("types")
@pass_context
def field_types(ctx: Context):
    """Show available custom field types."""
    types = [
        {"type": "String", "description": "Single-line text"},
        {"type": "Text", "description": "Multi-line text"},
        {"type": "Dropdown", "description": "Single select from options"},
        {"type": "MultiSelect", "description": "Multiple select from options"},
        {"type": "Date", "description": "Date (YYYY-MM-DD)"},
        {"type": "Checkbox", "description": "Boolean true/false"},
        {"type": "Number", "description": "Numeric value"},
        {"type": "Currency", "description": "Monetary value"},
        {"type": "Percentage", "description": "Percentage value"},
        {"type": "URL", "description": "Web URL"},
        {"type": "Connect", "description": "Link to another record"},
    ]

    def show_table(data):
        table = Table(title="Custom Field Types")
        table.add_column("Type", style="cyan")
        table.add_column("Description")
        for t in data:
            table.add_row(t["type"], t["description"])
        ctx.console.print(table)

    ctx.output(types, show_table)


# ============================================================================
# Shell completion
# ============================================================================


@cli.command("completion")
@click.argument("shell", type=click.Choice(["bash", "zsh", "fish"]))
def completion(shell: str):
    """Generate shell completion script.
    
    To install:
      bash:  eval "$(copper completion bash)"
      zsh:   eval "$(copper completion zsh)"
      fish:  copper completion fish | source
    """
    if shell == "bash":
        click.echo('eval "$(_COPPER_COMPLETE=bash_source copper)"')
    elif shell == "zsh":
        click.echo('eval "$(_COPPER_COMPLETE=zsh_source copper)"')
    elif shell == "fish":
        click.echo("_COPPER_COMPLETE=fish_source copper | source")


# ============================================================================
# Entry point
# ============================================================================


def main() -> None:
    """Entry point for the Copper CLI."""
    try:
        cli(standalone_mode=False)
    except click.ClickException as e:
        e.show()
        sys.exit(EXIT_USAGE)
    except SystemExit:
        raise
    except KeyboardInterrupt:
        click.echo("\nInterrupted", err=True)
        sys.exit(130)
    except Exception as e:
        # Check if we're in verbose mode by looking at sys.argv
        verbose = "-v" in sys.argv or "--verbose" in sys.argv
        
        if verbose:
            # Show full traceback in verbose mode
            import traceback
            click.echo(f"Error: {e}", err=True)
            click.echo("\nTraceback:", err=True)
            traceback.print_exc()
        else:
            # User-friendly error with hint
            click.echo(f"Error: {e}", err=True)
            click.echo("Hint: Use --verbose for detailed error information", err=True)
        
        sys.exit(EXIT_ERROR)


if __name__ == "__main__":
    main()
