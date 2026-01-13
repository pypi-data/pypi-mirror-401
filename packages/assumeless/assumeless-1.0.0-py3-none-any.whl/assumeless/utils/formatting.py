from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from assumeless.core.models import Finding, BlastRadius

console = Console()

def print_finding(finding: Finding) -> None:
    """
    Render a finding in the specific 'Assumeless' style.
    Style: Review comment, not error report.
    """
    # Color coding based on 'Poison' intuition (visual only)
    color = "yellow" 
    if finding.blast_radius in (BlastRadius.SYSTEM, BlastRadius.DATA):
        color = "red"
    
    title = Text(f"Observation {finding.id}: {finding.description}", style=f"bold {color}")
    
    body = (
        f"[dim]{finding.location_str}[/dim]\n\n"
        f"[bold]Diagnosis:[/bold]\n"
        f" • Invisibility: {finding.invisibility.value}\n"
        f" • Impact Risk:  {finding.blast_radius.value}\n"
        f" • Mode:         {finding.failure_mode.value}\n\n"
        f"[italic]\"This assumption creates a {finding.blast_radius.value.lower()} risk that is {finding.invisibility.value.lower()} from view.\"[/italic]"
    )
    
    console.print(Panel(body, title=title, border_style=color, expand=False))

def print_summary(n_findings: int, n_shown: int) -> None:
    """
    Print the calm summary footer.
    """
    if n_findings == 0:
        console.print("\n[green]No critical assumptions observed.[/green] Codebase appears clean of defined patterns.\n")
    else:
        hidden = n_findings - n_shown
        msg = f"\n[dim]Diagnosed {n_findings} potential assumptions.[/dim]"
        if hidden > 0:
             msg += f" [dim]Surfaced the top {n_shown} most significant issues. ({hidden} hidden)[/dim]"
        console.print(msg + "\n")
