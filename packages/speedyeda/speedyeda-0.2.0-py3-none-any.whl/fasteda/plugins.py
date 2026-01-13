"""
Plugin system for custom visualizations and analysis functions.
"""

from typing import Callable, Dict, Any, List
import inspect


# Global registry for plugins
_PLUGIN_REGISTRY: Dict[str, Callable] = {}


def register_plugin(name: str):
    """
    Decorator to register a custom plugin function.
    
    Usage:
        @register_plugin("my_analysis")
        def my_custom_analysis(df):
            return {"result": "custom analysis"}
    
    Args:
        name: Unique name for the plugin
    """
    def decorator(func: Callable):
        if name in _PLUGIN_REGISTRY:
            raise ValueError(f"Plugin '{name}' is already registered")
        
        # Validate function signature
        sig = inspect.signature(func)
        if 'df' not in sig.parameters:
            raise ValueError(f"Plugin function must accept 'df' parameter")
        
        _PLUGIN_REGISTRY[name] = func
        return func
    
    return decorator


def get_plugin(name: str) -> Callable:
    """
    Get a registered plugin by name.
    
    Args:
        name: Plugin name
        
    Returns:
        Plugin function
        
    Raises:
        KeyError: If plugin not found
    """
    if name not in _PLUGIN_REGISTRY:
        raise KeyError(f"Plugin '{name}' not found. Available: {list_plugins()}")
    
    return _PLUGIN_REGISTRY[name]


def list_plugins() -> List[str]:
    """Get list of registered plugin names."""
    return list(_PLUGIN_REGISTRY.keys())


def run_plugin(name: str, df, **kwargs) -> Any:
    """
    Run a registered plugin.
    
    Args:
        name: Plugin name
        df: pandas DataFrame
        **kwargs: Additional arguments to pass to plugin
        
    Returns:
        Plugin result
    """
    plugin = get_plugin(name)
    return plugin(df, **kwargs)


def load_plugins_from_file(filepath: str):
    """
    Load plugins from a Python file.
    
    The file should contain functions decorated with @register_plugin.
    
    Args:
        filepath: Path to Python file containing plugin definitions
    """
    import importlib.util
    from pathlib import Path
    
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"Plugin file not found: {filepath}")
    
    # Load module from file
    spec = importlib.util.spec_from_file_location("custom_plugins", filepath)
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    else:
        raise ImportError(f"Failed to load plugins from {filepath}")


# Example built-in plugin
@register_plugin("outlier_detection")
def detect_outliers(df, **kwargs):
    """
    Detect outliers using IQR method.
    
    Args:
        df: pandas DataFrame
        **kwargs: threshold (default: 1.5)
    """
    import numpy as np
    
    threshold = kwargs.get('threshold', 1.5)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    outliers = {}
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        
        outlier_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
        outlier_count = outlier_mask.sum()
        
        if outlier_count > 0:
            outliers[col] = {
                'count': int(outlier_count),
                'percentage': float(outlier_count / len(df) * 100),
                'lower_bound': float(lower_bound),
                'upper_bound': float(upper_bound),
            }
    
    return outliers
