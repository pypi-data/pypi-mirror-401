"""
rs-dssp CLI - Modern command-line interface with typer and rich.

Usage:
    rs-dssp protein.pdb
    rs-dssp *.pdb --output results/
    rs-dssp protein.pdb --format table
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from . import assign, assign_batch, to_dataframe, __version__

app = typer.Typer(
    name="rs-dssp",
    help="High-performance DSSP secondary structure assignment",
    add_completion=False,
)
console = Console()


def version_callback(value: bool):
    if value:
        console.print(f"rs-dssp [bold green]{__version__}[/]")
        raise typer.Exit()


@app.command()
def main(
    files: Annotated[
        list[Path],
        typer.Argument(help="PDB/mmCIF files to process"),
    ],
    output: Annotated[
        Optional[Path],
        typer.Option("-o", "--output", help="Output file or directory"),
    ] = None,
    format: Annotated[
        str,
        typer.Option("-f", "--format", help="Output format"),
    ] = "simple",
    threads: Annotated[
        int,
        typer.Option("-j", "--threads", help="Number of threads (0=auto)"),
    ] = 0,
    no_sasa: Annotated[
        bool,
        typer.Option("--no-sasa", help="Skip SASA calculation"),
    ] = False,
    version: Annotated[
        Optional[bool],
        typer.Option("--version", callback=version_callback, is_eager=True),
    ] = None,
):
    """Process PDB/mmCIF files and assign secondary structure."""
    calculate_sasa = not no_sasa

    if len(files) == 1:
        _process_single(files[0], output, format, calculate_sasa)
    else:
        _process_batch(files, output, format, threads, calculate_sasa)


def _process_single(file: Path, output: Path | None, fmt: str, sasa: bool):
    """Process a single file."""
    try:
        result = assign(file, calculate_sasa=sasa)
    except Exception as e:
        console.print(f"[red]Error:[/] {e}")
        raise typer.Exit(1)

    _output_result(result, file.stem, output, fmt)


def _process_batch(
    files: list[Path], output: Path | None, fmt: str, threads: int, sasa: bool
):
    """Process multiple files with progress bar."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        progress.add_task(f"Processing {len(files)} files...", total=None)
        results = assign_batch(files, n_threads=threads, calculate_sasa=sasa)

    success = sum(1 for r in results if r is not None)
    console.print(f"[green]Processed {success}/{len(files)} files[/]")

    for file, result in zip(files, results):
        if result:
            _output_result(result, file.stem, output, fmt)


def _output_result(result, name: str, output: Path | None, fmt: str):
    """Output result in specified format."""
    if fmt == "table":
        _print_table(result)
    elif fmt == "simple":
        console.print(f"{result.sequence_c3}\t{name}")
    elif fmt == "json":
        import json
        data = {
            "id": name,
            "sequence": result.sequence,
            "sequence_c3": result.sequence_c3,
            "aa_sequence": result.aa_sequence,
        }
        console.print_json(json.dumps(data))


def _print_table(result):
    """Print result as rich table."""
    table = Table(title=f"DSSP Result ({result.residue_count} residues)")
    table.add_column("Idx", style="dim")
    table.add_column("Chain")
    table.add_column("Seq")
    table.add_column("AA")
    table.add_column("SS", style="bold")
    table.add_column("C3", style="bold cyan")
    table.add_column("Phi")
    table.add_column("Psi")

    for r in result.residues[:20]:  # Show first 20
        phi = f"{r.phi:.1f}" if r.phi else "-"
        psi = f"{r.psi:.1f}" if r.psi else "-"
        table.add_row(
            str(r.index), r.chain_id, str(r.seq_id),
            r.amino_acid, r.structure, r.structure_c3,
            phi, psi
        )

    if result.residue_count > 20:
        table.add_row("...", "...", "...", "...", "...", "...", "...", "...")

    console.print(table)


if __name__ == "__main__":
    app()
