"""
Visualization generation for exploratory data analysis.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Dict, Any, List, Optional
import warnings

warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['figure.dpi'] = 100


def generate_plots(
    df: pd.DataFrame,
    output_dir: Optional[Path] = None,
    show_plots: bool = False
) -> Dict[str, Any]:
    """
    Generate comprehensive visualizations for the dataset.
    
    Args:
        df: pandas DataFrame
        output_dir: Directory to save plots (None = don't save)
        show_plots: Whether to display plots (default: False for CLI)
        
    Returns:
        Dictionary with plot paths and metadata
    """
    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    
    plots = {}
    
    # Numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    # 1. Distribution plots for numeric columns
    if numeric_cols:
        plots['distributions'] = _plot_distributions(df, numeric_cols, output_dir)
    
    # 2. Correlation heatmap
    if len(numeric_cols) >= 2:
        plots['correlation_heatmap'] = _plot_correlation_heatmap(df, numeric_cols, output_dir)
    
    # 3. Box plots for numeric columns
    if numeric_cols:
        plots['boxplots'] = _plot_boxplots(df, numeric_cols, output_dir)
    
    # 4. Categorical value counts
    if categorical_cols:
        plots['categorical'] = _plot_categorical(df, categorical_cols[:5], output_dir)  # Limit to 5
    
    # 5. Missing value heatmap
    if df.isnull().any().any():
        plots['missing_values'] = _plot_missing_values(df, output_dir)
    
    return plots


def _plot_distributions(df: pd.DataFrame, columns: List[str], output_dir: Optional[Path]) -> Optional[str]:
    """Plot histograms for numeric columns."""
    n_cols = len(columns)
    if n_cols == 0:
        return None
    
    # Limit to first 6 columns for readability
    columns = columns[:6]
    n_cols = len(columns)
    
    n_rows = (n_cols + 2) // 3
    n_plot_cols = min(3, n_cols)
    
    fig, axes = plt.subplots(n_rows, n_plot_cols, figsize=(15, 5 * n_rows))
    if n_cols == 1:
        axes = np.array([axes])
    axes = axes.flatten() if n_cols > 1 else axes
    
    for idx, col in enumerate(columns):
        ax = axes[idx] if n_cols > 1 else axes[0]
        df[col].hist(bins=30, ax=ax, edgecolor='black', alpha=0.7)
        ax.set_title(f'Distribution of {col}')
        ax.set_xlabel(col)
        ax.set_ylabel('Frequency')
    
    # Hide unused subplots
    for idx in range(n_cols, len(axes)):
        axes[idx].set_visible(False)
    
    plt.tight_layout()
    
    if output_dir:
        path = output_dir / 'distributions.png'
        plt.savefig(path, bbox_inches='tight', dpi=150)
        plt.close()
        return str(path)
    
    plt.close()
    return None


def _plot_correlation_heatmap(df: pd.DataFrame, columns: List[str], output_dir: Optional[Path]) -> Optional[str]:
    """Plot correlation heatmap."""
    corr = df[columns].corr()
    
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0,
                square=True, linewidths=1, cbar_kws={"shrink": 0.8}, ax=ax)
    ax.set_title('Correlation Matrix', fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    
    if output_dir:
        path = output_dir / 'correlation_heatmap.png'
        plt.savefig(path, bbox_inches='tight', dpi=150)
        plt.close()
        return str(path)
    
    plt.close()
    return None


def _plot_boxplots(df: pd.DataFrame, columns: List[str], output_dir: Optional[Path]) -> Optional[str]:
    """Plot box plots for numeric columns."""
    # Limit to first 6 columns
    columns = columns[:6]
    n_cols = len(columns)
    
    if n_cols == 0:
        return None
    
    n_rows = (n_cols + 2) // 3
    n_plot_cols = min(3, n_cols)
    
    fig, axes = plt.subplots(n_rows, n_plot_cols, figsize=(15, 5 * n_rows))
    if n_cols == 1:
        axes = np.array([axes])
    axes = axes.flatten() if n_cols > 1 else axes
    
    for idx, col in enumerate(columns):
        ax = axes[idx] if n_cols > 1 else axes[0]
        df.boxplot(column=col, ax=ax)
        ax.set_title(f'Box Plot: {col}')
        ax.set_ylabel(col)
    
    # Hide unused subplots
    for idx in range(n_cols, len(axes)):
        axes[idx].set_visible(False)
    
    plt.tight_layout()
    
    if output_dir:
        path = output_dir / 'boxplots.png'
        plt.savefig(path, bbox_inches='tight', dpi=150)
        plt.close()
        return str(path)
    
    plt.close()
    return None


def _plot_categorical(df: pd.DataFrame, columns: List[str], output_dir: Optional[Path]) -> Optional[str]:
    """Plot value counts for categorical columns."""
    if not columns:
        return None
    
    n_cols = len(columns)
    n_rows = (n_cols + 1) // 2
    n_plot_cols = min(2, n_cols)
    
    fig, axes = plt.subplots(n_rows, n_plot_cols, figsize=(15, 5 * n_rows))
    if n_cols == 1:
        axes = np.array([axes])
    axes = axes.flatten() if n_cols > 1 else axes
    
    for idx, col in enumerate(columns):
        ax = axes[idx] if n_cols > 1 else axes[0]
        value_counts = df[col].value_counts().head(10)
        value_counts.plot(kind='barh', ax=ax, color='steelblue')
        ax.set_title(f'Top Values: {col}')
        ax.set_xlabel('Count')
    
    # Hide unused subplots
    for idx in range(n_cols, len(axes)):
        axes[idx].set_visible(False)
    
    plt.tight_layout()
    
    if output_dir:
        path = output_dir / 'categorical.png'
        plt.savefig(path, bbox_inches='tight', dpi=150)
        plt.close()
        return str(path)
    
    plt.close()
    return None


def _plot_missing_values(df: pd.DataFrame, output_dir: Optional[Path]) -> Optional[str]:
    """Plot missing value heatmap."""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create binary matrix for missing values
    missing = df.isnull()
    
    sns.heatmap(missing, yticklabels=False, cbar=True, cmap='viridis', ax=ax)
    ax.set_title('Missing Values Heatmap', fontsize=16, fontweight='bold')
    ax.set_xlabel('Columns')
    ax.set_ylabel('Rows')
    
    plt.tight_layout()
    
    if output_dir:
        path = output_dir / 'missing_values.png'
        plt.savefig(path, bbox_inches='tight', dpi=150)
        plt.close()
        return str(path)
    
    plt.close()
    return None
