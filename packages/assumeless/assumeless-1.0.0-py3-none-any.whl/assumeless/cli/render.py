from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from typing import List
import json
from dataclasses import asdict
from itertools import groupby
from assumeless.core.models import Finding, BlastRadius, FailureMode

console = Console()

BANNER = r"""
    _____                                           .__                           
  /  _  \    ______  ______ __ __   _____    ____  |  |    ____    ______  ______
 /  /_\  \  /  ___/ /  ___/|  |  \ /     \ _/ __ \ |  |  _/ __ \  /  ___/ /  ___/
/    |    \ \___ \  \___ \ |  |  /|  Y Y  \\  ___/ |  |__\  ___/  \___ \  \___ \ 
\____|__  //____  >/____  >|____/ |__|_|  / \___  >|____/ \___  >/____  >/____  >
        \/      \/      \/              \/      \/            \/      \/      \/ 
"""

def print_banner() -> None:
    console.print(Text(BANNER, style="bold blue"))
    console.print("  [dim]Assumptions-first diagnostic tool v1.0.0[/dim]\n")

def get_human_impact(blast: BlastRadius) -> str:
    mapping = {
        BlastRadius.LOCAL: "This issue is confined to a single function scope.",
        BlastRadius.MODULE: "This creates risks for the entire module's stability.",
        BlastRadius.SYSTEM: "This assumption puts the whole application process at risk.",
        BlastRadius.DATA: "This endangers persistent data integrity.",
        BlastRadius.EXTERNAL: "This affects external systems or users."
    }
    return mapping.get(blast, "Impact is unknown.")

def get_human_consequence(mode: FailureMode) -> str:
    mapping = {
        FailureMode.CRASH: "The application might crash unexpectedly.",
        FailureMode.HANG: "The process could freeze or hang indefinitely.",
        FailureMode.SILENT: "Errors will occur silently, hiding the root cause.",
        FailureMode.BYPASS: "Critical logic or security controls might be bypassed.",
        FailureMode.CORRUPTION: "Data could be corrupted without any warning."
    }
    return mapping.get(mode, "Unpredictable behavior.")

def print_grouped_panel(rule_id: str, findings: List[Finding], index: int) -> None:
    # Consolidate findings
    title_finding = findings[0]
    description = title_finding.description
    
    color = "white"
    if title_finding.blast_radius == BlastRadius.SYSTEM:
        color = "yellow"
    if title_finding.failure_mode in (FailureMode.CORRUPTION, FailureMode.SILENT):
        color = "red"
    
    title = f"{index}) {description} ({rule_id})"
    
    occurrences_text = []
    for f in findings:
        occurrences_text.append(
            f"[bold]• {f.location_str}[/bold]\n"
            f"   [dim]>> {f.content.strip()}[/dim]"
        )
    
    occurrences_block = "\n\n".join(occurrences_text)
    
    why_matters = get_human_impact(title_finding.blast_radius)
    what_breaks = get_human_consequence(title_finding.failure_mode)
    
    content = (
        f"\nThis pattern appears in {len(findings)} locations:\n\n"
        f"{occurrences_block}\n\n"
        f"[bold {color}]Why this matters:[/bold {color}]\n"
        f"{why_matters}\n\n"
        f"[bold {color}]What could break:[/bold {color}]\n"
        f"{what_breaks}\n"
    )
    
    console.print(Panel(content, title=f"[{color}]{title}[/{color}]", border_style=color, expand=False, padding=(0,2)))

def print_doctor_report(findings: List[Finding]) -> None:
    if not findings:
        console.print("[green]✓ No risky assumptions detected.[/green]")
        return
    
    console.print("AssumeLess Doctor")
    console.print(f"[bold]{len(findings)} risky assumptions found[/bold]\n")
    
    sorted_findings = sorted(findings, key=lambda x: x.id)
    grouped = []
    
    for key, group in groupby(sorted_findings, key=lambda x: x.id):
        grouped.append((key, list(group)))
        
    for i, (rule_id, group_findings) in enumerate(grouped, 1):
        print_grouped_panel(rule_id, group_findings, i)
        
    console.print("\n[dim]Run `assumeless explain <id>` for detailed guidance.[/dim]")

def print_scan_summary(findings: List[Finding]) -> None:
    """Minimal, CI-friendly scan output."""
    if not findings:
        console.print("[green]AssumeLess found no risky assumptions.[/green]")
        return
        
    console.print(f"[bold]AssumeLess found {len(findings)} risky assumptions[/bold]\n")
    
    for f in findings:
        # Format: • {ID} at {path}:{line} – {description}
        line = f"• [cyan]{f.id}[/cyan] at {f.location_str} – {f.description}"
        console.print(line)
        
    # No footer, clean exit.

def print_json(findings: List[Finding]) -> None:
    """Output machine-readable JSON."""
    data = []
    for f in findings:
        item = asdict(f)
        item['invisibility'] = f.invisibility.value
        item['blast_radius'] = f.blast_radius.value
        item['failure_mode'] = f.failure_mode.value
        if isinstance(item.get('tags'), set):
             item['tags'] = list(item['tags'])
        data.append(item)
    print(json.dumps(data, indent=2))
