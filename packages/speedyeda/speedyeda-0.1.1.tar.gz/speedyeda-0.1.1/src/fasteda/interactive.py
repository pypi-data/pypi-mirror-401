"""
Interactive CLI prompts for guided analysis.
"""

from rich.prompt import Prompt, Confirm
from rich.console import Console
from typing import List, Optional
import pandas as pd


console = Console()


def interactive_column_selection(df: pd.DataFrame) -> List[str]:
    """
    Prompt user to select columns interactively.
    
    Args:
        df: pandas DataFrame
        
    Returns:
        List of selected column names
    """
    console.print("\n[bold cyan]Available Columns:[/bold cyan]")
    for idx, col in enumerate(df.columns, 1):
        dtype = df[col].dtype
        console.print(f"  {idx}. {col} ({dtype})")
    
    console.print("\n[dim]Enter column numbers separated by commas (e.g., 1,3,5)[/dim]")
    console.print("[dim]Or press Enter to analyze all columns[/dim]")
    
    selection = Prompt.ask("Select columns", default="all")
    
    if selection.lower() in ['all', '']:
        return list(df.columns)
    
    try:
        indices = [int(x.strip()) - 1 for x in selection.split(',')]
        selected_cols = [df.columns[i] for i in indices if 0 <= i < len(df.columns)]
        return selected_cols if selected_cols else list(df.columns)
    except (ValueError, IndexError):
        console.print("[yellow]⚠️  Invalid selection, using all columns[/yellow]")
        return list(df.columns)


def interactive_plot_selection() -> List[str]:
    """
    Prompt user to select plot types.
    
    Returns:
        List of selected plot types
    """
    console.print("\n[bold cyan]Available Plot Types:[/bold cyan]")
    plot_types = [
        ("distributions", "Histograms for numeric columns"),
        ("correlation", "Correlation heatmap"),
        ("boxplots", "Box plots for outlier detection"),
        ("categorical", "Bar charts for categorical data"),
        ("missing", "Missing value heatmap"),
    ]
    
    for idx, (name, desc) in enumerate(plot_types, 1):
        console.print(f"  {idx}. {name} - {desc}")
    
    console.print("\n[dim]Enter plot numbers separated by commas (e.g., 1,2,3)[/dim]")
    console.print("[dim]Or press Enter to generate all plots[/dim]")
    
    selection = Prompt.ask("Select plots", default="all")
    
    if selection.lower() in ['all', '']:
        return [name for name, _ in plot_types]
    
    try:
        indices = [int(x.strip()) - 1 for x in selection.split(',')]
        selected = [plot_types[i][0] for i in indices if 0 <= i < len(plot_types)]
        return selected if selected else [name for name, _ in plot_types]
    except (ValueError, IndexError):
        console.print("[yellow]⚠️  Invalid selection, generating all plots[/yellow]")
        return [name for name, _ in plot_types]


def interactive_preset_selection() -> Optional[str]:
    """
    Prompt user to select a preset.
    
    Returns:
        Selected preset name or None
    """
    from fasteda.presets import list_presets, PRESETS
    
    console.print("\n[bold cyan]Available Presets:[/bold cyan]")
    presets = list_presets()
    
    for idx, preset_name in enumerate(presets, 1):
        desc = PRESETS[preset_name]['description']
        console.print(f"  {idx}. {preset_name} - {desc}")
    
    console.print("\n[dim]Enter preset number or press Enter to skip[/dim]")
    
    selection = Prompt.ask("Select preset", default="none")
    
    if selection.lower() in ['none', '']:
        return None
    
    try:
        idx = int(selection) - 1
        if 0 <= idx < len(presets):
            return presets[idx]
    except ValueError:
        pass
    
    console.print("[yellow]⚠️  Invalid selection, skipping preset[/yellow]")
    return None


def interactive_export_options() -> Optional[str]:
    """
    Prompt user for export options.
    
    Returns:
        Export filepath or None
    """
    if Confirm.ask("\n💾 Save report to file?", default=False):
        filepath = Prompt.ask("Enter filename (e.g., report.json or report.txt)")
        return filepath
    
    return None
