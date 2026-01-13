"""CLI entry point for mock data generator."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TaskProgressColumn, TextColumn


console = Console()


@click.group()
def main() -> None:
    """Mock data generator CLI."""


@main.command()
@click.option("--file", "file_path", required=True, type=click.Path(exists=True, dir_okay=False))
@click.option("--output", "output_dir", default="./output", show_default=True)
@click.option("--interactive", is_flag=True, default=False, show_default=True)
@click.option("--locale", default="en_US", show_default=True)
def generate(file_path: str, output_dir: str, interactive: bool, locale: str) -> None:
    """Generate mock data from a model file."""
    try:
        _run_generate(Path(file_path), Path(output_dir), interactive, locale)
    except Exception as exc:  # pragma: no cover - defensive CLI boundary
        console.print(Panel(f"[red]Error:[/red] {exc}", title="mock-generator"))
        sys.exit(1)


def _run_generate(file_path: Path, output_dir: Path, interactive: bool, locale: str) -> None:
    console.print(f"[bold]Scanning[/bold] {file_path}...")

    from mock_generator.scanner import scan_file
    from mock_generator.analyzer import analyze_model
    from mock_generator.relationship_resolver import build_dependency_graph, get_generation_order
    from mock_generator.generator import MockDataGenerator
    from mock_generator.exporters import export_to_json

    scan_result = scan_file(str(file_path))
    framework = scan_result["framework"]
    model_nodes = scan_result["models"]

    if not model_nodes:
        raise ValueError("No models found in the provided file.")

    model_names = ", ".join(model_nodes.keys())
    console.print(f"[green]Found {len(model_nodes)} models[/green]: {model_names}")
    console.print(f"[green]Framework:[/green] {framework}")

    console.print("[bold]Analyzing models...[/bold]")
    models = {name: analyze_model(node, framework) for name, node in model_nodes.items()}

    dependency_graph = build_dependency_graph(models)
    order = get_generation_order(dependency_graph)

    console.print(f"[bold]Generation order:[/bold] {' -> '.join(order)}")

    counts = _collect_counts(order, interactive)

    generator = MockDataGenerator(locale=locale)

    console.print("[bold]Generating mock data...[/bold]")
    with Progress(
        SpinnerColumn(),
        TextColumn("{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
    ) as progress:
        for model_name in order:
            count = counts.get(model_name, 10)
            task = progress.add_task(f"{model_name}: {count}", total=count)
            records = generator.generate_for_model(models[model_name], count)
            generator.generated_data[model_name] = records
            progress.update(task, completed=count)

    export_to_json(generator.generated_data, str(output_dir))
    console.print("[green]Done![/green]")


def _collect_counts(order: list[str], interactive: bool) -> dict:
    counts: dict[str, int] = {}

    for model_name in order:
        if interactive:
            value = click.prompt(f"How many {model_name} records?", default=10, type=int)
        else:
            value = 10
        counts[model_name] = value

    return counts


if __name__ == "__main__":
    main()
