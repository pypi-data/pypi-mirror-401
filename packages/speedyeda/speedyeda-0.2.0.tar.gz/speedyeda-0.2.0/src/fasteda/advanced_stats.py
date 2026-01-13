"""
Advanced statistical analysis functions.
"""

import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, Any, List, Tuple, Optional


def calculate_correlations(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate multiple types of correlations.
    
    Args:
        df: pandas DataFrame
        
    Returns:
        Dictionary with Pearson, Spearman, and Kendall correlations
    """
    numeric_df = df.select_dtypes(include=[np.number])
    
    if numeric_df.shape[1] < 2:
        return {
            'pearson': pd.DataFrame(),
            'spearman': pd.DataFrame(),
            'kendall': pd.DataFrame(),
            'high_correlations': []
        }
    
    # Pearson (linear)
    pearson = numeric_df.corr(method='pearson')
    
    # Spearman (monotonic, rank-based)
    spearman = numeric_df.corr(method='spearman')
    
    # Kendall (ordinal association)
    kendall = numeric_df.corr(method='kendall')
    
    # Find high correlations across all methods
    high_corr = _find_high_correlations(pearson, spearman, kendall)
    
    return {
        'pearson': pearson,
        'spearman': spearman,
        'kendall': kendall,
        'high_correlations': high_corr
    }


def _find_high_correlations(
    pearson: pd.DataFrame,
    spearman: pd.DataFrame,
    kendall: pd.DataFrame,
    threshold: float = 0.7
) -> List[Dict[str, Any]]:
    """Find high correlations across all methods."""
    high_corr = []
    
    for i in range(len(pearson.columns)):
        for j in range(i+1, len(pearson.columns)):
            col1, col2 = pearson.columns[i], pearson.columns[j]
            
            p_val = abs(pearson.iloc[i, j])
            s_val = abs(spearman.iloc[i, j])
            k_val = abs(kendall.iloc[i, j])
            
            if p_val > threshold or s_val > threshold or k_val > threshold:
                high_corr.append({
                    'column1': col1,
                    'column2': col2,
                    'pearson': pearson.iloc[i, j],
                    'spearman': spearman.iloc[i, j],
                    'kendall': kendall.iloc[i, j],
                    'max_abs': max(p_val, s_val, k_val)
                })
    
    # Sort by max absolute correlation
    high_corr.sort(key=lambda x: x['max_abs'], reverse=True)
    
    return high_corr


def detect_outliers(df: pd.DataFrame, methods: List[str] = ['iqr', 'zscore']) -> Dict[str, Any]:
    """
    Detect outliers using multiple methods.
    
    Args:
        df: pandas DataFrame
        methods: List of methods to use ('iqr', 'zscore')
        
    Returns:
        Dictionary with outlier information per column and method
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    outliers = {}
    
    for col in numeric_cols:
        col_outliers = {}
        
        if 'iqr' in methods:
            col_outliers['iqr'] = _detect_outliers_iqr(df[col])
        
        if 'zscore' in methods:
            col_outliers['zscore'] = _detect_outliers_zscore(df[col])
        
        # Combine: outlier if detected by any method
        all_indices = set()
        for method_result in col_outliers.values():
            all_indices.update(method_result['indices'])
        
        if all_indices:
            outliers[col] = {
                'count': len(all_indices),
                'percentage': len(all_indices) / len(df) * 100,
                'indices': sorted(list(all_indices)),
                'methods': col_outliers
            }
    
    return outliers


def _detect_outliers_iqr(series: pd.Series, threshold: float = 1.5) -> Dict[str, Any]:
    """Detect outliers using IQR method."""
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - threshold * IQR
    upper_bound = Q3 + threshold * IQR
    
    outlier_mask = (series < lower_bound) | (series > upper_bound)
    outlier_indices = series[outlier_mask].index.tolist()
    
    return {
        'lower_bound': float(lower_bound),
        'upper_bound': float(upper_bound),
        'count': len(outlier_indices),
        'indices': outlier_indices
    }


def _detect_outliers_zscore(series: pd.Series, threshold: float = 3.0) -> Dict[str, Any]:
    """Detect outliers using Z-score method."""
    z_scores = np.abs(stats.zscore(series, nan_policy='omit'))
    outlier_mask = z_scores > threshold
    outlier_indices = series[outlier_mask].index.tolist()
    
    return {
        'threshold': threshold,
        'count': len(outlier_indices),
        'indices': outlier_indices,
        'max_zscore': float(np.max(z_scores[~np.isnan(z_scores)])) if len(z_scores) > 0 else 0.0
    }


def calculate_detailed_quantiles(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate detailed quantile statistics including 5th and 95th percentiles.
    
    Args:
        df: pandas DataFrame
        
    Returns:
        DataFrame with detailed quantile statistics
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) == 0:
        return pd.DataFrame()
    
    stats_dict = {
        'count': df[numeric_cols].count(),
        'mean': df[numeric_cols].mean(),
        'std': df[numeric_cols].std(),
        'min': df[numeric_cols].min(),
        '5%': df[numeric_cols].quantile(0.05),
        '25%': df[numeric_cols].quantile(0.25),
        '50%': df[numeric_cols].quantile(0.50),
        '75%': df[numeric_cols].quantile(0.75),
        '95%': df[numeric_cols].quantile(0.95),
        'max': df[numeric_cols].max(),
        'range': df[numeric_cols].max() - df[numeric_cols].min(),
        'iqr': df[numeric_cols].quantile(0.75) - df[numeric_cols].quantile(0.25),
        'skewness': df[numeric_cols].skew(),
        'kurtosis': df[numeric_cols].kurtosis(),
    }
    
    return pd.DataFrame(stats_dict)


def test_normality(df: pd.DataFrame, alpha: float = 0.05) -> Dict[str, Any]:
    """
    Test for normality using Shapiro-Wilk test.
    
    Args:
        df: pandas DataFrame
        alpha: Significance level
        
    Returns:
        Dictionary with normality test results per column
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    results = {}
    
    for col in numeric_cols:
        # Sample if too large (Shapiro-Wilk has max sample size)
        data = df[col].dropna()
        if len(data) > 5000:
            data = data.sample(5000, random_state=42)
        
        if len(data) >= 3:  # Minimum sample size
            statistic, p_value = stats.shapiro(data)
            
            results[col] = {
                'statistic': float(statistic),
                'p_value': float(p_value),
                'is_normal': p_value > alpha,
                'alpha': alpha
            }
    
    return results
