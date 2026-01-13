"""
Data loading utilities for various file formats.
"""

import pandas as pd
from pathlib import Path
from typing import Union


def load_data(filepath: Union[str, Path]) -> pd.DataFrame:
    """
    Load data from various file formats.
    
    Args:
        filepath: Path to the data file
        
    Returns:
        pandas DataFrame
        
    Raises:
        ValueError: If file format is not supported
        FileNotFoundError: If file doesn't exist
    """
    filepath = Path(filepath)
    
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    
    suffix = filepath.suffix.lower()
    
    loaders = {
        '.csv': lambda f: pd.read_csv(f),
        '.xlsx': lambda f: pd.read_excel(f),
        '.xls': lambda f: pd.read_excel(f),
        '.json': lambda f: pd.read_json(f),
        '.parquet': lambda f: pd.read_parquet(f),
    }
    
    if suffix not in loaders:
        raise ValueError(
            f"Unsupported file format: {suffix}. "
            f"Supported formats: {', '.join(loaders.keys())}"
        )
    
    try:
        df = loaders[suffix](filepath)
        return df
    except Exception as e:
        raise ValueError(f"Error loading file {filepath}: {str(e)}")
