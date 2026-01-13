import click
from assumeless.core.engine import Scanner
from assumeless.core.doctor import CodeDoctor
from assumeless.utils.formatting import print_finding, print_summary, console

@click.group()
def cli():
    """AssumeLess: Assumptions-first diagnostic tool."""
    pass

@cli.command()
@click.argument('path', default='.', type=click.Path(exists=True))
@click.option('--all', is_flag=True, help="Show all findings (Disable Doctor filtering).")
def scan(path, all):
    """
    Scan a directory for dangerous assumptions.
    """
    scanner = Scanner()
    doctor = CodeDoctor()

    with console.status("[bold green]Diagnosing codebase assumptions..."):
        findings = scanner.scan_directory(path)
        
    if not all:
        # The Doctor Logic: Only show the "Poisonous" ones
        selected_findings = doctor.examine(findings)
    else:
        selected_findings = findings

    if not selected_findings and findings:
        console.print("[yellow]Assumptions detected, but none met the 'Active Poison' threshold for immediate review.[/yellow]")
        console.print("[dim]Use --all to see them.[/dim]")
        return

    for f in selected_findings:
        print_finding(f)

    print_summary(len(findings), len(selected_findings))

@cli.command()
@click.argument('finding_id')
def explain(finding_id):
    """
    Explain the reasoning behind a specific Finding ID.
    (Placeholder for v1.0)
    """
    # In a real tool this would look up the Rule docstring or a docs DB.
    console.print(f"[bold]Explanation for {finding_id}[/bold]")
    console.print("This finding ID represents a specific pattern of assumption...")

if __name__ == '__main__':
    cli()
