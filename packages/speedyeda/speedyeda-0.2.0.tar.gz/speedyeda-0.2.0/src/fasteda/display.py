"""
Rich terminal display for beautiful, colorful output.
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
from rich.progress import Progress
import pandas as pd
from typing import Dict, Any, List


console = Console()


def display_results(results: Dict[str, Any], fun_mode: bool = False):
    """
    Display analysis results in a beautiful, colorful format.
    
    Args:
        results: Analysis results dictionary
        fun_mode: Enable emojis and extra flair
    """
    if fun_mode:
        console.print("\n🚀 [bold cyan]Dataset ready for launch![/bold cyan] Summary inside 🌟\n")
    else:
        console.print("\n[bold cyan]FastEDA Analysis Report[/bold cyan]\n")
    
    # Basic info
    _display_basic_info(results['basic_info'], fun_mode)
    
    # Data types
    _display_data_types(results['data_types'], fun_mode)
    
    # Statistics
    if not results['statistics'].empty:
        _display_statistics(results['statistics'], fun_mode)
    
    # Missing values
    if not results['missing_values'].empty:
        _display_missing_values(results['missing_values'], fun_mode)
    
    # Correlations
    if results['correlations']['high_correlations']:
        _display_correlations(results['correlations'], fun_mode)
    
    # Categorical insights
    if results['categorical_insights']:
        _display_categorical_insights(results['categorical_insights'], fun_mode)


def _display_basic_info(info: Dict[str, Any], fun_mode: bool):
    """Display basic dataset information."""
    emoji = "📊 " if fun_mode else ""
    
    table = Table(title=f"{emoji}Dataset Overview", box=box.ROUNDED, show_header=False)
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Shape", f"{info['rows']:,} rows × {info['columns']} columns")
    table.add_row("Memory Usage", f"{info['memory_usage'] / 1024 / 1024:.2f} MB")
    
    console.print(table)
    console.print()


def _display_data_types(types: Dict[str, Any], fun_mode: bool):
    """Display data type summary."""
    emoji = "🔤 " if fun_mode else ""
    
    table = Table(title=f"{emoji}Data Types", box=box.ROUNDED)
    table.add_column("Type", style="cyan")
    table.add_column("Count", style="green", justify="right")
    
    table.add_row("Numeric Columns", str(types['numeric_count']))
    table.add_row("Categorical Columns", str(types['categorical_count']))
    table.add_row("Datetime Columns", str(types['datetime_count']))
    
    console.print(table)
    console.print()


def _display_statistics(stats: pd.DataFrame, fun_mode: bool):
    """Display statistical summary."""
    emoji = "📈 " if fun_mode else ""
    
    # Convert to rich table
    table = Table(title=f"{emoji}Statistical Summary", box=box.ROUNDED)
    table.add_column("Statistic", style="cyan")
    
    for col in stats.columns:
        table.add_column(str(col), style="green", justify="right")
    
    for idx in stats.index:
        row_data = [str(idx)]
        for col in stats.columns:
            val = stats.loc[idx, col]
            if isinstance(val, (int, float)):
                row_data.append(f"{val:.2f}")
            else:
                row_data.append(str(val))
        table.add_row(*row_data)
    
    console.print(table)
    console.print()


def _display_missing_values(missing: pd.DataFrame, fun_mode: bool):
    """Display missing value analysis."""
    emoji = "⚠️  " if fun_mode else ""
    
    table = Table(title=f"{emoji}Missing Values", box=box.ROUNDED)
    table.add_column("Column", style="cyan")
    table.add_column("Missing Count", style="yellow", justify="right")
    table.add_column("Missing %", style="red", justify="right")
    
    for _, row in missing.iterrows():
        table.add_row(
            row['column'],
            f"{int(row['missing_count']):,}",
            f"{row['missing_percent']:.2f}%"
        )
    
    console.print(table)
    console.print()


def _display_correlations(corr: Dict[str, Any], fun_mode: bool):
    """Display high correlations."""
    emoji = "🔗 " if fun_mode else ""
    high_corr = corr['high_correlations']
    
    if not high_corr:
        return
    
    table = Table(title=f"{emoji}High Correlations (|r| > 0.7)", box=box.ROUNDED)
    table.add_column("Column 1", style="cyan")
    table.add_column("Column 2", style="cyan")
    table.add_column("Correlation", style="magenta", justify="right")
    
    for item in high_corr[:10]:  # Limit to top 10
        table.add_row(
            item['column1'],
            item['column2'],
            f"{item['correlation']:.3f}"
        )
    
    console.print(table)
    console.print()


def _display_categorical_insights(insights: Dict[str, Any], fun_mode: bool):
    """Display categorical column insights."""
    emoji = "🏷️  " if fun_mode else ""
    
    for col, data in list(insights.items())[:5]:  # Limit to 5 columns
        table = Table(title=f"{emoji}Categorical: {col}", box=box.ROUNDED)
        table.add_column("Value", style="cyan")
        table.add_column("Count", style="green", justify="right")
        
        table.add_row("Unique Values", str(data['unique_count']))
        
        if data['top_values']:
            table.add_row("", "")  # Separator
            for value, count in list(data['top_values'].items())[:5]:
                table.add_row(str(value), f"{count:,}")
        
        console.print(table)
        console.print()


def print_success(message: str, fun_mode: bool = False):
    """Print success message."""
    emoji = "✅ " if fun_mode else ""
    console.print(f"{emoji}[bold green]{message}[/bold green]")


def print_error(message: str):
    """Print error message."""
    console.print(f"❌ [bold red]{message}[/bold red]")


def print_info(message: str, fun_mode: bool = False):
    """Print info message."""
    emoji = "ℹ️  " if fun_mode else ""
    console.print(f"{emoji}[bold blue]{message}[/bold blue]")
