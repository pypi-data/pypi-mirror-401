"""
Report generation and export utilities.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
import pandas as pd


def save_report(results: Dict[str, Any], filepath: str):
    """
    Save analysis results to a file.
    
    Args:
        results: Analysis results dictionary
        filepath: Output file path (supports .json, .txt)
    """
    filepath = Path(filepath)
    suffix = filepath.suffix.lower()
    
    if suffix == '.json':
        _save_json_report(results, filepath)
    elif suffix == '.txt':
        _save_text_report(results, filepath)
    else:
        raise ValueError(f"Unsupported format: {suffix}. Use .json or .txt")


def _save_json_report(results: Dict[str, Any], filepath: Path):
    """Save results as JSON."""
    # Convert DataFrames to dicts for JSON serialization
    serializable = {}
    
    for key, value in results.items():
        if isinstance(value, pd.DataFrame):
            serializable[key] = value.to_dict()
        elif isinstance(value, dict):
            serializable[key] = _make_serializable(value)
        else:
            serializable[key] = value
    
    with open(filepath, 'w') as f:
        json.dump(serializable, f, indent=2, default=str)


def _make_serializable(obj):
    """Convert objects to JSON-serializable format."""
    import numpy as np
    
    if isinstance(obj, pd.DataFrame):
        return obj.to_dict(orient='records')
    elif isinstance(obj, (pd.Series, np.ndarray)):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {str(k): _make_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_make_serializable(item) for item in obj]
    elif isinstance(obj, (np.integer, np.floating)):
        return float(obj)
    elif hasattr(obj, 'item'):  # numpy scalar
        return obj.item()
    elif pd.api.types.is_numeric_dtype(type(obj)):
        return float(obj)
    else:
        return str(obj) if not isinstance(obj, (str, int, float, bool, type(None))) else obj


def _save_text_report(results: Dict[str, Any], filepath: Path):
    """Save results as plain text."""
    with open(filepath, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("FASTEDA ANALYSIS REPORT\n")
        f.write("=" * 80 + "\n\n")
        
        # Basic info
        info = results['basic_info']
        f.write("DATASET OVERVIEW\n")
        f.write("-" * 40 + "\n")
        f.write(f"Shape: {info['rows']:,} rows × {info['columns']} columns\n")
        f.write(f"Memory: {info['memory_usage'] / 1024 / 1024:.2f} MB\n\n")
        
        # Data types
        types = results['data_types']
        f.write("DATA TYPES\n")
        f.write("-" * 40 + "\n")
        f.write(f"Numeric: {types['numeric_count']}\n")
        f.write(f"Categorical: {types['categorical_count']}\n")
        f.write(f"Datetime: {types['datetime_count']}\n\n")
        
        # Statistics
        if not results['statistics'].empty:
            f.write("STATISTICS\n")
            f.write("-" * 40 + "\n")
            f.write(results['statistics'].to_string())
            f.write("\n\n")
        
        # Missing values
        if not results['missing_values'].empty:
            f.write("MISSING VALUES\n")
            f.write("-" * 40 + "\n")
            f.write(results['missing_values'].to_string(index=False))
            f.write("\n\n")
        
        # High correlations
        if results['correlations']['high_correlations']:
            f.write("HIGH CORRELATIONS\n")
            f.write("-" * 40 + "\n")
            for item in results['correlations']['high_correlations'][:10]:
                f.write(f"{item['column1']} <-> {item['column2']}: {item['correlation']:.3f}\n")
            f.write("\n")
