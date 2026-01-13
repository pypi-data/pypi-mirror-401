"""
Core analysis functions for exploratory data analysis.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional


def analyze(
    df: pd.DataFrame,
    fun: bool = False,
    columns: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Perform comprehensive exploratory data analysis on a DataFrame.
    
    Args:
        df: pandas DataFrame to analyze
        fun: Enable fun mode with emojis and colorful output
        columns: Optional list of columns to analyze (None = all columns)
        
    Returns:
        Dictionary containing analysis results
    """
    if columns:
        df = df[columns]
    
    results = {
        'basic_info': _get_basic_info(df),
        'statistics': _get_statistics(df),
        'missing_values': _get_missing_values(df),
        'data_types': _get_data_types(df),
        'correlations': _get_correlations(df),
        'categorical_insights': _get_categorical_insights(df),
        'fun_mode': fun
    }
    
    return results


def _get_basic_info(df: pd.DataFrame) -> Dict[str, Any]:
    """Get basic dataset information."""
    return {
        'shape': df.shape,
        'rows': len(df),
        'columns': len(df.columns),
        'column_names': list(df.columns),
        'memory_usage': df.memory_usage(deep=True).sum(),
    }


def _get_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """Get descriptive statistics for numeric columns."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) == 0:
        return pd.DataFrame()
    
    stats = df[numeric_cols].describe()
    
    # Add additional statistics
    stats.loc['mode'] = df[numeric_cols].mode().iloc[0] if len(df) > 0 else np.nan
    stats.loc['skewness'] = df[numeric_cols].skew()
    stats.loc['kurtosis'] = df[numeric_cols].kurtosis()
    
    return stats


def _get_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Analyze missing values in the dataset."""
    missing_count = df.isnull().sum()
    missing_percent = (missing_count / len(df)) * 100
    
    missing_df = pd.DataFrame({
        'column': df.columns,
        'missing_count': missing_count.values,
        'missing_percent': missing_percent.values
    })
    
    # Only return columns with missing values
    missing_df = missing_df[missing_df['missing_count'] > 0]
    missing_df = missing_df.sort_values('missing_count', ascending=False)
    
    return missing_df


def _get_data_types(df: pd.DataFrame) -> Dict[str, Any]:
    """Analyze data types in the dataset."""
    type_counts = df.dtypes.value_counts()
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
    
    return {
        'type_distribution': type_counts.to_dict(),
        'numeric_columns': numeric_cols,
        'categorical_columns': categorical_cols,
        'datetime_columns': datetime_cols,
        'numeric_count': len(numeric_cols),
        'categorical_count': len(categorical_cols),
        'datetime_count': len(datetime_cols),
    }


def _get_correlations(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate correlations between numeric columns."""
    numeric_df = df.select_dtypes(include=[np.number])
    
    if numeric_df.shape[1] < 2:
        return {
            'correlation_matrix': pd.DataFrame(),
            'high_correlations': []
        }
    
    corr_matrix = numeric_df.corr()
    
    # Find high correlations (absolute value > 0.7, excluding diagonal)
    high_corr = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            corr_val = corr_matrix.iloc[i, j]
            if abs(corr_val) > 0.7:
                high_corr.append({
                    'column1': corr_matrix.columns[i],
                    'column2': corr_matrix.columns[j],
                    'correlation': corr_val
                })
    
    return {
        'correlation_matrix': corr_matrix,
        'high_correlations': high_corr
    }


def _get_categorical_insights(df: pd.DataFrame) -> Dict[str, Any]:
    """Analyze categorical columns."""
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    
    insights = {}
    for col in categorical_cols:
        value_counts = df[col].value_counts()
        insights[col] = {
            'unique_count': df[col].nunique(),
            'top_values': value_counts.head(10).to_dict(),
            'most_common': value_counts.index[0] if len(value_counts) > 0 else None,
            'most_common_count': value_counts.iloc[0] if len(value_counts) > 0 else 0,
        }
    
    return insights
