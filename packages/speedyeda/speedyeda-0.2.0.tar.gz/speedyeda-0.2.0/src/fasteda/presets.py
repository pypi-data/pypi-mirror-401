"""
Preset configurations for common analysis scenarios.
"""

from typing import Dict, Any, List


PRESETS: Dict[str, Dict[str, Any]] = {
    'ecommerce': {
        'description': 'E-commerce product and sales analysis',
        'focus_columns': ['price', 'quantity', 'revenue', 'category', 'product'],
        'key_metrics': ['price', 'quantity', 'revenue'],
        'categorical_focus': ['category', 'product', 'region'],
        'recommended_plots': ['distribution', 'correlation', 'categorical'],
    },
    
    'survey': {
        'description': 'Survey response and sentiment analysis',
        'focus_columns': ['rating', 'score', 'response', 'category', 'sentiment'],
        'key_metrics': ['rating', 'score'],
        'categorical_focus': ['response', 'category', 'sentiment'],
        'recommended_plots': ['categorical', 'distribution'],
    },
    
    'finance': {
        'description': 'Financial and time series analysis',
        'focus_columns': ['price', 'volume', 'return', 'date', 'ticker'],
        'key_metrics': ['price', 'volume', 'return'],
        'categorical_focus': ['ticker', 'sector'],
        'recommended_plots': ['distribution', 'correlation', 'boxplot'],
    },
    
    'general': {
        'description': 'General-purpose data exploration',
        'focus_columns': [],
        'key_metrics': [],
        'categorical_focus': [],
        'recommended_plots': ['distribution', 'correlation', 'categorical', 'boxplot'],
    }
}


def get_preset(name: str) -> Dict[str, Any]:
    """
    Get a preset configuration by name.
    
    Args:
        name: Preset name (ecommerce, survey, finance, general)
        
    Returns:
        Preset configuration dictionary
        
    Raises:
        ValueError: If preset name is not found
    """
    preset = PRESETS.get(name.lower())
    if not preset:
        available = ', '.join(PRESETS.keys())
        raise ValueError(f"Unknown preset: {name}. Available: {available}")
    
    return preset


def list_presets() -> List[str]:
    """Get list of available presets."""
    return list(PRESETS.keys())


def apply_preset(df, preset_name: str) -> Dict[str, Any]:
    """
    Apply preset configuration to filter and focus analysis.
    
    Args:
        df: pandas DataFrame
        preset_name: Name of the preset
        
    Returns:
        Dictionary with filtered columns and analysis hints
    """
    preset = get_preset(preset_name)
    
    # Find matching columns (case-insensitive)
    df_cols_lower = {col.lower(): col for col in df.columns}
    
    focus_cols = []
    for col_pattern in preset['focus_columns']:
        for df_col_lower, df_col in df_cols_lower.items():
            if col_pattern.lower() in df_col_lower:
                focus_cols.append(df_col)
    
    return {
        'preset_name': preset_name,
        'description': preset['description'],
        'focus_columns': focus_cols if focus_cols else None,  # None = use all
        'recommended_plots': preset['recommended_plots'],
    }
