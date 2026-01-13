"""
Data quality alerts and warnings.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List


class DataQualityAlert:
    """Data quality alert with severity and recommendations."""
    
    def __init__(self, alert_type: str, severity: str, message: str, affected_columns: List[str] = None):
        self.alert_type = alert_type
        self.severity = severity  # 'critical', 'warning', 'info'
        self.message = message
        self.affected_columns = affected_columns or []
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': self.alert_type,
            'severity': self.severity,
            'message': self.message,
            'affected_columns': self.affected_columns
        }


def check_data_quality(df: pd.DataFrame, correlation_matrix: pd.DataFrame = None) -> List[DataQualityAlert]:
    """
    Comprehensive data quality checks with actionable alerts.
    
    Args:
        df: pandas DataFrame
        correlation_matrix: Pre-computed correlation matrix (optional)
        
    Returns:
        List of DataQualityAlert objects
    """
    alerts = []
    
    # 1. Check for duplicate rows
    alerts.extend(_check_duplicates(df))
    
    # 2. Check for constant/zero-variance columns
    alerts.extend(_check_constant_columns(df))
    
    # 3. Check for high cardinality
    alerts.extend(_check_high_cardinality(df))
    
    # 4. Check for multicollinearity
    if correlation_matrix is not None:
        alerts.extend(_check_multicollinearity(correlation_matrix))
    
    # 5. Check for imbalanced target (if applicable)
    alerts.extend(_check_class_imbalance(df))
    
    # 6. Check for high missing value columns
    alerts.extend(_check_excessive_missing(df))
    
    # 7. Check for mixed data types
    alerts.extend(_check_mixed_types(df))
    
    return alerts


def _check_duplicates(df: pd.DataFrame) -> List[DataQualityAlert]:
    """Check for duplicate rows."""
    alerts = []
    
    dup_count = df.duplicated().sum()
    if dup_count > 0:
        percentage = dup_count / len(df) * 100
        
        severity = 'critical' if percentage > 10 else 'warning'
        message = f"Found {dup_count:,} duplicate rows ({percentage:.1f}%). Consider removing duplicates with df.drop_duplicates()."
        
        alerts.append(DataQualityAlert('duplicates', severity, message))
    
    return alerts


def _check_constant_columns(df: pd.DataFrame) -> List[DataQualityAlert]:
    """Check for columns with zero variance."""
    alerts = []
    constant_cols = []
    
    for col in df.columns:
        if df[col].nunique() == 1:
            constant_cols.append(col)
    
    if constant_cols:
        message = f"Found {len(constant_cols)} constant column(s) with zero variance: {', '.join(constant_cols[:5])}{'...' if len(constant_cols) > 5 else ''}. These provide no information and should be removed."
        
        alerts.append(DataQualityAlert('constant_columns', 'warning', message, constant_cols))
    
    return alerts


def _check_high_cardinality(df: pd.DataFrame, threshold: int = 100) -> List[DataQualityAlert]:
    """Check for categorical columns with high cardinality."""
    alerts = []
    high_card_cols = []
    
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    
    for col in categorical_cols:
        unique_count = df[col].nunique()
        total_count = len(df)
        
        # High cardinality: >threshold unique values or >50% unique
        if unique_count > threshold and (unique_count / total_count) > 0.5:
            high_card_cols.append((col, unique_count))
    
    if high_card_cols:
        col_details = ', '.join([f"{col} ({count} unique)" for col, count in high_card_cols[:3]])
        message = f"High cardinality detected in {len(high_card_cols)} column(s): {col_details}. Consider using hash encoding, target encoding, or dimensionality reduction."
        
        alerts.append(DataQualityAlert('high_cardinality', 'warning', message, [col for col, _ in high_card_cols]))
    
    return alerts


def _check_multicollinearity(correlation_matrix: pd.DataFrame, threshold: float = 0.9) -> List[DataQualityAlert]:
    """Check for highly correlated features (multicollinearity)."""
    alerts = []
    high_corr_pairs = []
    
    for i in range(len(correlation_matrix.columns)):
        for j in range(i+1, len(correlation_matrix.columns)):
            corr_val = abs(correlation_matrix.iloc[i, j])
            if corr_val > threshold:
                col1 = correlation_matrix.columns[i]
                col2 = correlation_matrix.columns[j]
                high_corr_pairs.append((col1, col2, corr_val))
    
    if high_corr_pairs:
        # Sort by correlation strength
        high_corr_pairs.sort(key=lambda x: x[2], reverse=True)
        
        pair_details = ', '.join([f"{c1} <-> {c2} (r={r:.2f})" for c1, c2, r in high_corr_pairs[:3]])
        message = f"⚠️ Multicollinearity detected! Found {len(high_corr_pairs)} highly correlated pair(s) (|r| > {threshold}): {pair_details}. This can harm ML models - consider removing one feature from each pair."
        
        affected = list(set([col for pair in high_corr_pairs for col in pair[:2]]))
        alerts.append(DataQualityAlert('multicollinearity', 'critical', message, affected))
    
    return alerts


def _check_class_imbalance(df: pd.DataFrame, threshold: float = 0.1) -> List[DataQualityAlert]:
    """Check for class imbalance in binary/categorical columns."""
    alerts = []
    
    categorical_cols = df.select_dtypes(include=['object', 'category', 'bool']).columns
    
    for col in categorical_cols:
        value_counts = df[col].value_counts()
        
        # Check binary columns
        if len(value_counts) == 2:
            min_ratio = value_counts.min() / value_counts.sum()
            
            if min_ratio < threshold:
                minority_class = value_counts.idxmin()
                message = f"Class imbalance in '{col}': minority class '{minority_class}' is only {min_ratio*100:.1f}% of data. Consider using SMOTE, class weights, or stratified sampling."
                
                alerts.append(DataQualityAlert('class_imbalance', 'warning', message, [col]))
    
    return alerts


def _check_excessive_missing(df: pd.DataFrame, threshold: float = 0.5) -> List[DataQualityAlert]:
    """Check for columns with excessive missing values."""
    alerts = []
    high_missing_cols = []
    
    for col in df.columns:
        missing_ratio = df[col].isnull().sum() / len(df)
        
        if missing_ratio > threshold:
            high_missing_cols.append((col, missing_ratio * 100))
    
    if high_missing_cols:
        col_details = ', '.join([f"{col} ({pct:.1f}%)" for col, pct in high_missing_cols[:3]])
        message = f"Excessive missing data in {len(high_missing_cols)} column(s): {col_details}. Consider dropping these columns or using advanced imputation."
        
        alerts.append(DataQualityAlert('excessive_missing', 'warning', message, [col for col, _ in high_missing_cols]))
    
    return alerts


def _check_mixed_types(df: pd.DataFrame) -> List[DataQualityAlert]:
    """Check for object columns that might have mixed types."""
    alerts = []
    mixed_type_cols = []
    
    object_cols = df.select_dtypes(include=['object']).columns
    
    for col in object_cols:
        # Try to infer if it's actually numeric
        non_null = df[col].dropna()
        if len(non_null) > 0:
            try:
                # Attempt conversion
                pd.to_numeric(non_null, errors='raise')
                mixed_type_cols.append(col)
            except (ValueError, TypeError):
                pass
    
    if mixed_type_cols:
        message = f"Possible mixed/incorrect data types in {len(mixed_type_cols)} column(s): {', '.join(mixed_type_cols[:5])}. These might be stored as strings but contain numeric data. Try converting with pd.to_numeric()."
        
        alerts.append(DataQualityAlert('mixed_types', 'info', message, mixed_type_cols))
    
    return alerts


def format_alerts_for_display(alerts: List[DataQualityAlert]) -> str:
    """Format alerts for terminal display."""
    if not alerts:
        return "✅ No data quality issues detected!"
    
    output = []
    
    # Group by severity
    critical = [a for a in alerts if a.severity == 'critical']
    warnings = [a for a in alerts if a.severity == 'warning']
    info = [a for a in alerts if a.severity == 'info']
    
    if critical:
        output.append(f"\n🚨 CRITICAL ISSUES ({len(critical)}):")
        for alert in critical:
            output.append(f"   • {alert.message}")
    
    if warnings:
        output.append(f"\n⚠️  WARNINGS ({len(warnings)}):")
        for alert in warnings:
            output.append(f"   • {alert.message}")
    
    if info:
        output.append(f"\nℹ️  INFO ({len(info)}):")
        for alert in info:
            output.append(f"   • {alert.message}")
    
    return '\n'.join(output)
