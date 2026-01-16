"""
DNS-AID Command Line Interface.

Usage:
    dns-aid publish     Publish an agent to DNS
    dns-aid discover    Discover agents at a domain
    dns-aid verify      Verify agent DNS records
    dns-aid list        List DNS-AID records
    dns-aid zones       List available DNS zones
"""

from __future__ import annotations

import asyncio
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(
    name="dns-aid",
    help="DNS-based Agent Identification and Discovery",
    no_args_is_help=True,
)

console = Console()
error_console = Console(stderr=True)


def run_async(coro):
    """Run async function in sync context."""
    return asyncio.run(coro)


# ============================================================================
# PUBLISH COMMAND
# ============================================================================


@app.command()
def publish(
    name: Annotated[str, typer.Option("--name", "-n", help="Agent name (e.g., 'chat', 'network')")],
    domain: Annotated[str, typer.Option("--domain", "-d", help="Domain to publish under")],
    protocol: Annotated[str, typer.Option("--protocol", "-p", help="Protocol: mcp or a2a")] = "mcp",
    endpoint: Annotated[
        str | None, typer.Option("--endpoint", "-e", help="Agent endpoint hostname")
    ] = None,
    port: Annotated[int, typer.Option("--port", help="Port number")] = 443,
    capability: Annotated[
        list[str] | None,
        typer.Option("--capability", "-c", help="Agent capability (repeatable)"),
    ] = None,
    version: Annotated[str, typer.Option("--version", "-v", help="Agent version")] = "1.0.0",
    ttl: Annotated[int, typer.Option("--ttl", help="DNS TTL in seconds")] = 3600,
    backend: Annotated[
        str, typer.Option("--backend", "-b", help="DNS backend: route53, mock")
    ] = "route53",
):
    """
    Publish an agent to DNS using DNS-AID protocol.

    Creates SVCB and TXT records that allow other agents to discover this agent.

    Example:
        dns-aid publish -n network-specialist -d example.com -p mcp -e mcp.example.com -c ipam -c dns
    """
    from dns_aid.core.publisher import publish as do_publish

    # Default endpoint to {protocol}.{domain}
    if endpoint is None:
        endpoint = f"{protocol}.{domain}"

    # Get backend
    dns_backend = _get_backend(backend)

    console.print("\n[bold]Publishing agent to DNS...[/bold]\n")

    result = run_async(
        do_publish(
            name=name,
            domain=domain,
            protocol=protocol,
            endpoint=endpoint,
            port=port,
            capabilities=capability or [],
            version=version,
            ttl=ttl,
            backend=dns_backend,
        )
    )

    if result.success:
        console.print("[green]✓ Agent published successfully![/green]\n")
        console.print(f"  [bold]FQDN:[/bold] {result.agent.fqdn}")
        console.print(f"  [bold]Endpoint:[/bold] {result.agent.endpoint_url}")
        console.print("\n  [bold]Records created:[/bold]")
        for record in result.records_created:
            console.print(f"    • {record}")

        console.print("\n[dim]Verify with:[/dim]")
        console.print(f"  dig {result.agent.fqdn} SVCB")
        console.print(f"  dig {result.agent.fqdn} TXT")
    else:
        error_console.print(f"[red]✗ Failed to publish: {result.message}[/red]")
        raise typer.Exit(1)


# ============================================================================
# DISCOVER COMMAND
# ============================================================================


@app.command()
def discover(
    domain: Annotated[str, typer.Argument(help="Domain to search for agents")],
    protocol: Annotated[
        str | None, typer.Option("--protocol", "-p", help="Filter by protocol")
    ] = None,
    name: Annotated[str | None, typer.Option("--name", "-n", help="Filter by agent name")] = None,
    json_output: Annotated[bool, typer.Option("--json", "-j", help="Output as JSON")] = False,
):
    """
    Discover agents at a domain using DNS-AID protocol.

    Queries DNS for SVCB records and returns agent endpoints.

    Example:
        dns-aid discover example.com
        dns-aid discover example.com --protocol mcp
        dns-aid discover example.com --name chat
    """
    from dns_aid.core.discoverer import discover as do_discover

    console.print(f"\n[bold]Discovering agents at {domain}...[/bold]\n")

    result = run_async(
        do_discover(
            domain=domain,
            protocol=protocol,
            name=name,
        )
    )

    if json_output:
        import json

        output = {
            "domain": result.domain,
            "query": result.query,
            "agents": [
                {
                    "name": a.name,
                    "protocol": a.protocol.value,
                    "endpoint": a.endpoint_url,
                    "capabilities": a.capabilities,
                }
                for a in result.agents
            ],
            "count": result.count,
            "query_time_ms": result.query_time_ms,
        }
        console.print_json(json.dumps(output))
        return

    if result.count == 0:
        console.print(f"[yellow]No agents found at {domain}[/yellow]")
        console.print(f"\n[dim]Query: {result.query}[/dim]")
        console.print(f"[dim]Time: {result.query_time_ms:.2f}ms[/dim]")
        return

    console.print(f"[green]Found {result.count} agent(s) at {domain}:[/green]\n")

    table = Table(show_header=True, header_style="bold")
    table.add_column("Name")
    table.add_column("Protocol")
    table.add_column("Endpoint")
    table.add_column("Capabilities")

    for agent in result.agents:
        table.add_row(
            agent.name,
            agent.protocol.value,
            agent.endpoint_url,
            ", ".join(agent.capabilities) if agent.capabilities else "-",
        )

    console.print(table)
    console.print(f"\n[dim]Query: {result.query}[/dim]")
    console.print(f"[dim]Time: {result.query_time_ms:.2f}ms[/dim]")


# ============================================================================
# VERIFY COMMAND
# ============================================================================


@app.command()
def verify(
    fqdn: Annotated[
        str, typer.Argument(help="FQDN to verify (e.g., _chat._a2a._agents.example.com)")
    ],
):
    """
    Verify DNS-AID records for an agent.

    Checks DNS record existence, DNSSEC validation, and endpoint health.

    Example:
        dns-aid verify _chat._a2a._agents.example.com
    """
    from dns_aid.core.validator import verify as do_verify

    console.print(f"\n[bold]Verifying {fqdn}...[/bold]\n")

    result = run_async(do_verify(fqdn))

    # Display results
    def status(ok: bool | None) -> str:
        if ok is None:
            return "[yellow]○[/yellow]"
        return "[green]✓[/green]" if ok else "[red]✗[/red]"

    console.print(f"  {status(result.record_exists)} DNS record exists")
    console.print(f"  {status(result.svcb_valid)} SVCB record valid")
    console.print(f"  {status(result.dnssec_valid)} DNSSEC validated")
    console.print(f"  {status(result.dane_valid)} DANE/TLSA configured")
    console.print(f"  {status(result.endpoint_reachable)} Endpoint reachable")

    if result.endpoint_latency_ms:
        console.print(f"    [dim]Latency: {result.endpoint_latency_ms:.0f}ms[/dim]")

    console.print(
        f"\n[bold]Security Score:[/bold] {result.security_score}/100 ({result.security_rating})"
    )


# ============================================================================
# LIST COMMAND
# ============================================================================


@app.command("list")
def list_records(
    domain: Annotated[str, typer.Argument(help="Domain to list records from")],
    backend: Annotated[str, typer.Option("--backend", "-b", help="DNS backend")] = "route53",
):
    """
    List DNS-AID records in a domain.

    Shows all _agents.* records in the specified zone.

    Example:
        dns-aid list example.com
    """
    dns_backend = _get_backend(backend)

    console.print(f"\n[bold]DNS-AID records in {domain}:[/bold]\n")

    async def list_all():
        records = []
        async for record in dns_backend.list_records(domain, name_pattern="_agents"):
            records.append(record)
        return records

    records = run_async(list_all())

    if not records:
        console.print(f"[yellow]No DNS-AID records found in {domain}[/yellow]")
        return

    table = Table(show_header=True, header_style="bold")
    table.add_column("Name")
    table.add_column("Type")
    table.add_column("TTL")
    table.add_column("Value")

    for record in records:
        value = record.get("values", [])
        if isinstance(value, list):
            value = value[0] if value else "-"
        if len(str(value)) > 50:
            value = str(value)[:47] + "..."

        table.add_row(
            record["fqdn"],
            record["type"],
            str(record["ttl"]),
            str(value),
        )

    console.print(table)
    console.print(f"\n[dim]Total: {len(records)} record(s)[/dim]")


# ============================================================================
# ZONES COMMAND
# ============================================================================


@app.command()
def zones(
    backend: Annotated[str, typer.Option("--backend", "-b", help="DNS backend")] = "route53",
):
    """
    List available DNS zones.

    Shows all zones accessible with current credentials.

    Example:
        dns-aid zones
    """
    dns_backend = _get_backend(backend)

    console.print(f"\n[bold]Available DNS zones ({backend}):[/bold]\n")

    if backend != "route53":
        error_console.print("[red]Zone listing only supported for route53 backend[/red]")
        raise typer.Exit(1)

    from dns_aid.backends.route53 import Route53Backend

    if not isinstance(dns_backend, Route53Backend):
        raise typer.Exit(1)

    zone_list = run_async(dns_backend.list_zones())

    table = Table(show_header=True, header_style="bold")
    table.add_column("Domain")
    table.add_column("Zone ID")
    table.add_column("Records")
    table.add_column("Type")

    for zone in zone_list:
        table.add_row(
            zone["name"],
            zone["id"],
            str(zone["record_count"]),
            "Private" if zone["private"] else "Public",
        )

    console.print(table)


# ============================================================================
# DELETE COMMAND
# ============================================================================


@app.command()
def delete(
    name: Annotated[str, typer.Option("--name", "-n", help="Agent name")],
    domain: Annotated[str, typer.Option("--domain", "-d", help="Domain")],
    protocol: Annotated[str, typer.Option("--protocol", "-p", help="Protocol")] = "mcp",
    backend: Annotated[str, typer.Option("--backend", "-b", help="DNS backend")] = "route53",
    force: Annotated[bool, typer.Option("--force", "-f", help="Skip confirmation")] = False,
):
    """
    Delete an agent from DNS.

    Removes SVCB and TXT records for the specified agent.

    Example:
        dns-aid delete -n chat -d example.com -p a2a
    """
    from dns_aid.core.publisher import unpublish

    fqdn = f"_{name}._{protocol}._agents.{domain}"

    if not force:
        confirm = typer.confirm(f"Delete {fqdn}?")
        if not confirm:
            raise typer.Abort()

    dns_backend = _get_backend(backend)

    console.print(f"\n[bold]Deleting {fqdn}...[/bold]\n")

    result = run_async(
        unpublish(
            name=name,
            domain=domain,
            protocol=protocol,
            backend=dns_backend,
        )
    )

    if result:
        console.print("[green]✓ Agent deleted successfully[/green]")
    else:
        console.print("[yellow]No records found to delete[/yellow]")


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def _get_backend(backend_name: str):
    """Get DNS backend by name."""
    if backend_name == "route53":
        from dns_aid.backends.route53 import Route53Backend

        return Route53Backend()
    elif backend_name == "mock":
        from dns_aid.backends.mock import MockBackend

        return MockBackend()
    else:
        error_console.print(f"[red]Unknown backend: {backend_name}[/red]")
        error_console.print("Available backends: route53, mock")
        raise typer.Exit(1)


# ============================================================================
# VERSION
# ============================================================================


def version_callback(value: bool):
    if value:
        from dns_aid import __version__

        console.print(f"dns-aid version {__version__}")
        raise typer.Exit()


def quiet_callback(value: bool):
    if value:
        from dns_aid.utils.logging import silence_logging

        silence_logging()


@app.callback()
def main(
    version: Annotated[
        bool | None,
        typer.Option("--version", callback=version_callback, is_eager=True, help="Show version"),
    ] = None,
    quiet: Annotated[
        bool | None,
        typer.Option("--quiet", "-q", callback=quiet_callback, is_eager=True, help="Suppress logs"),
    ] = None,
):
    """
    DNS-AID: DNS-based Agent Identification and Discovery

    Publish and discover AI agents using DNS infrastructure.
    """
    pass


if __name__ == "__main__":
    app()
