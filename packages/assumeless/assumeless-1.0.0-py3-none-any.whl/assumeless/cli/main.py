import os
import click

from typing import List
from assumeless.core.engine import Scanner
from assumeless.core.doctor import CodeDoctor
from assumeless.core.config import Config
from assumeless.cli.render import print_banner, print_doctor_report, print_scan_summary, console, print_json
from assumeless.core.cache import FileHashCache
from assumeless.core.models import Finding
from assumeless.core.doc_checker import DocDriftDetector

def perform_scan(path: str, show_all: bool, output_json: bool) -> List[Finding]:
    """Helper for both scan and doctor."""
    config = Config.load(path)
    scanner = Scanner(config)
    doctor = CodeDoctor()

    if output_json:
        # JSON Logic
        raw_findings = scanner.scan_path(path)
        if show_all:
            return raw_findings
        return doctor.examine(raw_findings)
    
    # CLI Logic
    # We suppress printing here if we are printing later, 
    # but the status spinner needs to be here during execution.
    if not output_json:
        with console.status("[bold blue]Scanning codebase..."):
            raw_findings = scanner.scan_path(path)
            if show_all:
                return raw_findings
            return doctor.examine(raw_findings)
    else:
        # Should not happen as logic flow is handled above
         return []

@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx: click.Context) -> None:
    """AssumeLess: Find risky hidden assumptions."""
    if ctx.invoked_subcommand is None:
        # Default behavior: Show banner and help
        print_banner()
        click.echo(ctx.get_help())

@main.command()
@click.argument('path', default='.', type=click.Path(exists=True))
@click.option('--version', is_flag=True, help="Show version info")
@click.option('--all', 'show_all', is_flag=True, help="Show all findings")
@click.option('--json', 'output_json', is_flag=True, help="Output JSON")
def scan(path: str, version: bool, show_all: bool, output_json: bool) -> None:
    """Scan codebase and show top 2–3 risky assumptions."""
    if version:
        print_banner()
        return

    findings = perform_scan(path, show_all, output_json)
    
    if output_json:
        print_json(findings)
    else:
        # Use minimal summary for scan
        print_scan_summary(findings)

@main.command()
@click.argument('path', default='.', type=click.Path(exists=True))
@click.option('--all', 'show_all', is_flag=True, help="Show all findings")
@click.option('--json', 'output_json', is_flag=True, help="Output JSON")
def doctor(path: str, show_all: bool, output_json: bool) -> None:
    """Alias for scan (Code Doctor)."""
    # Distinct handler calling the same logic
    findings = perform_scan(path, show_all, output_json)
    
    if output_json:
        print_json(findings)
    else:
        # Use detailed report for doctor
        print_doctor_report(findings)

@main.command()
@click.argument('finding_id')
def explain(finding_id: str) -> None:
    """Show details for one finding."""
    scanner = Scanner()
    found_rule = None
    
    # Search registry for rule ID
    for rules_list in scanner.registry.values():
        for rule in rules_list:
            if rule.id == finding_id:
                found_rule = rule
                break
        if found_rule:
            break
    
    if found_rule:
        console.print(f"[bold cyan]Explanation for {finding_id}[/bold cyan]")
        console.print(f"[bold]{found_rule.name}[/bold]")
        console.print("\n[dim](Full documentation coming in v1.3)[/dim]")
    else:
        console.print(f"[red]Unknown Rule ID: {finding_id}[/red]")
        console.print("Run `assumeless rules` to see valid IDs.")

@main.command()
def help() -> None:
    """Show help + ASCII banner."""
    print_banner()
    with click.Context(main) as ctx:
        click.echo(main.get_help(ctx))

@main.command()
def version() -> None:
    """Show version + ASCII banner."""
    print_banner()

@main.command()
@click.argument('path', default='.', type=click.Path(exists=True))
def config(path: str) -> None:
    """Show loaded config summary."""
    conf = Config.load(path)
    console.print(f"[bold]Loaded Configuration from {path}[/bold]")
    console.print(f"Max Findings: {conf.max_findings}")
    console.print(f"Ignore Paths: {conf.ignore_paths}")
    console.print(f"Ignore Rules: {conf.ignore_rules}")
    console.print(f"Cache Enabled: {conf.enable_cache}")

@main.command()
def rules() -> None:
    """List available rule IDs."""
    scanner = Scanner()
    rules = sorted(set([(r.id, r.name) for sublist in scanner.registry.values() for r in sublist]))
    
    console.print("[bold]Active Rules Catalog:[/bold]")
    for rid, rname in rules:
        console.print(f" - [cyan]{rid}[/cyan]: {rname}")

@main.command()
def clear_cache() -> None:
    """Clear incremental scan cache."""
    cache = FileHashCache()
    if os.path.exists(cache.cache_path):
        os.remove(cache.cache_path)
        console.print("[green]✓ Cache cleared.[/green]")
    else:
        console.print("[yellow]No cache found.[/yellow]")



@main.command()
@click.argument('path', default='.', type=click.Path(exists=True))
def docs(path: str) -> None:
    """Scan for documentation drift."""
    console.print("AssumeLess Docs")
    
    detector = DocDriftDetector(path)
    findings = detector.scan()
    
    if not findings:
        console.print("No documentation drift detected")
        return

    console.print(f"[bold red]{len(findings)} documentation mismatches found[/bold red]\n")
    
    for f in findings:
        console.print(f"• [cyan]{f.id}[/cyan] at {f.file_path}:{f.line_number}")
        console.print(f"  {f.description}\n")

if __name__ == '__main__':
    main()
