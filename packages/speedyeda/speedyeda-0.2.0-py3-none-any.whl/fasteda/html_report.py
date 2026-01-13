"""
Interactive HTML report generation using Plotly.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from pathlib import Path
from typing import Dict, Any, Optional
import json


def generate_html_report(
    df: pd.DataFrame,
    results: Dict[str, Any],
    filepath: str,
    title: str = "SpeedyEDA Report"
) -> str:
    """
    Generate an interactive HTML report using Plotly.
    
    Args:
        df: pandas DataFrame
        results: Analysis results dictionary
        filepath: Output HTML file path
        title: Report title
        
    Returns:
        Path to generated HTML file
    """
    filepath = Path(filepath)
    
    # Create HTML structure
    html_parts = []
    
    # HTML Header
    html_parts.append(_generate_html_header(title))
    
    # Overview Section
    html_parts.append(_generate_overview_section(results))
    
    # Data Quality Alerts
    if 'quality_alerts' in results and results['quality_alerts']:
        html_parts.append(_generate_alerts_section(results['quality_alerts']))
    
    # Statistical Summary
    html_parts.append(_generate_statistics_section(results))
    
    # Correlation Heatmaps
    if 'advanced_correlations' in results:
        html_parts.append(_generate_correlation_section(results['advanced_correlations']))
    
    # Distribution Plots
    html_parts.append(_generate_distribution_section(df))
    
    # Outlier Analysis
    if 'outliers' in results:
        html_parts.append(_generate_outlier_section(results['outliers']))
    
    # Missing Values
    if not results['missing_values'].empty:
        html_parts.append(_generate_missing_section(results['missing_values']))
    
    # Categorical Analysis
    if results['categorical_insights']:
        html_parts.append(_generate_categorical_section(results['categorical_insights']))
    
    # Footer
    html_parts.append(_generate_html_footer())
    
    # Write to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(html_parts))
    
    return str(filepath)


def _generate_html_header(title: str) -> str:
    """Generate HTML header with styling."""
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdn.plot.ly/plotly-2.26.0.min.js"></script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }}
        h1 {{
            color: #667eea;
            text-align: center;
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        h2 {{
            color: #764ba2;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
            margin-top: 40px;
        }}
        h3 {{
            color: #555;
            margin-top: 25px;
        }}
        .alert {{
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            font-weight: 500;
        }}
        .alert-critical {{
            background: #ffe6e6;
            border-left: 5px solid #ff4444;
            color: #cc0000;
        }}
        .alert-warning {{
            background: #fff3cd;
            border-left: 5px solid #ffc107;
            color: #856404;
        }}
        .alert-info {{
            background: #d1ecf1;
            border-left: 5px solid #17a2b8;
            color: #0c5460;
        }}
        .stat-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }}
        .stat-value {{
            font-size: 2em;
            font-weight: bold;
        }}
        .stat-label {{
            font-size: 0.9em;
            opacity: 0.9;
        }}
        .plot-container {{
            margin: 20px 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background: #667eea;
            color: white;
        }}
        tr:hover {{
            background: #f5f5f5;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 {title}</h1>
        <p style="text-align: center; color: #666; font-size: 1.1em;">Generated by SpeedyEDA - Lightning-Fast Data Exploration</p>
"""


def _generate_overview_section(results: Dict[str, Any]) -> str:
    """Generate overview statistics section."""
    info = results['basic_info']
    
    html = """
        <h2>📊 Dataset Overview</h2>
        <div class="stat-grid">
            <div class="stat-card">
                <div class="stat-value">{:,}</div>
                <div class="stat-label">Total Rows</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{}</div>
                <div class="stat-label">Total Columns</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{:.1f} MB</div>
                <div class="stat-label">Memory Usage</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{}</div>
                <div class="stat-label">Numeric Columns</div>
            </div>
        </div>
    """.format(
        info['rows'],
        info['columns'],
        info['memory_usage'] / 1024 / 1024,
        results['data_types']['numeric_count']
    )
    
    return html


def _generate_alerts_section(alerts: list) -> str:
    """Generate data quality alerts section."""
    html = ["<h2>⚠️ Data Quality Alerts</h2>"]
    
    for alert in alerts:
        alert_dict = alert.to_dict()
        severity_class = f"alert-{alert_dict['severity']}"
        icon = {'critical': '🚨', 'warning': '⚠️', 'info': 'ℹ️'}.get(alert_dict['severity'], '•')
        
        html.append(f'<div class="alert {severity_class}">{icon} {alert_dict["message"]}</div>')
    
    return '\n'.join(html)


def _generate_statistics_section(results: Dict[str, Any]) -> str:
    """Generate statistical summary table."""
    if results['statistics'].empty:
        return ""
    
    stats_df = results['statistics']
    
    html = ["<h2>📈 Statistical Summary</h2>"]
    html.append(stats_df.to_html(classes=''))
    
    return '\n'.join(html)


def _generate_correlation_section(correlations: Dict[str, Any]) -> str:
    """Generate correlation heatmaps."""
    html = ["<h2>🔗 Correlation Analysis</h2>"]
    
    for method in ['pearson', 'spearman', 'kendall']:
        if method in correlations and not correlations[method].empty:
            corr_matrix = correlations[method]
            
            # Create heatmap
            fig = go.Figure(data=go.Heatmap(
                z=corr_matrix.values,
                x=corr_matrix.columns,
                y=corr_matrix.columns,
                colorscale='RdBu',
                zmid=0,
                text=corr_matrix.values,
                texttemplate='%{text:.2f}',
                textfont={"size": 10},
                colorbar=dict(title="Correlation")
            ))
            
            fig.update_layout(
                title=f'{method.capitalize()} Correlation Matrix',
                width=800,
                height=700,
                xaxis=dict(tickangle=-45)
            )
            
            html.append(f'<h3>{method.capitalize()} Correlation</h3>')
            html.append(f'<div class="plot-container" id="{method}-corr"></div>')
            html.append(f'<script>Plotly.newPlot("{method}-corr", {fig.to_json()});</script>')
    
    return '\n'.join(html)


def _generate_distribution_section(df: pd.DataFrame) -> str:
    """Generate distribution plots for numeric columns."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns[:6]  # Limit to 6
    
    if len(numeric_cols) == 0:
        return ""
    
    html = ["<h2>📊 Distributions</h2>"]
    
    for col in numeric_cols:
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=df[col], name=col, nbinsx=30))
        fig.update_layout(
            title=f'Distribution of {col}',
            xaxis_title=col,
            yaxis_title='Frequency',
            width=600,
            height=400
        )
        
        html.append(f'<div class="plot-container" id="dist-{col}"></div>')
        html.append(f'<script>Plotly.newPlot("dist-{col}", {fig.to_json()});</script>')
    
    return '\n'.join(html)


def _generate_outlier_section(outliers: Dict[str, Any]) -> str:
    """Generate outlier analysis section."""
    if not outliers:
        return ""
    
    html = ["<h2>🎯 Outlier Detection</h2>"]
    
    for col, outlier_info in list(outliers.items())[:5]:  # Limit to 5 columns
        count = outlier_info['count']
        pct = outlier_info['percentage']
        
        html.append(f"<h3>{col}</h3>")
        html.append(f"<p><strong>{count}</strong> outliers detected ({pct:.1f}% of data)</p>")
    
    return '\n'.join(html)


def _generate_missing_section(missing_df: pd.DataFrame) -> str:
    """Generate missing values visualization."""
    html = ["<h2>❓ Missing Values</h2>"]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=missing_df['column'],
        y=missing_df['missing_percent'],
        text=missing_df['missing_percent'].round(1),
        texttemplate='%{text}%',
        textposition='outside',
    ))
    
    fig.update_layout(
        title='Missing Values by Column',
        xaxis_title='Column',
        yaxis_title='Missing %',
        width=800,
        height=400
    )
    
    html.append('<div class="plot-container" id="missing"></div>')
    html.append(f'<script>Plotly.newPlot("missing", {fig.to_json()});</script>')
    
    return '\n'.join(html)


def _generate_categorical_section(cat_insights: Dict[str, Any]) -> str:
    """Generate categorical insights section."""
    html = ["<h2>🏷️ Categorical Analysis</h2>"]
    
    for col, data in list(cat_insights.items())[:5]:  # Limit to 5
        html.append(f"<h3>{col}</h3>")
        html.append(f"<p><strong>{data['unique_count']}</strong> unique values</p>")
        
        if data['top_values']:
            values = list(data['top_values'].keys())[:10]
            counts = list(data['top_values'].values())[:10]
            
            fig = go.Figure()
            fig.add_trace(go.Bar(x=counts, y=values, orientation='h'))
            fig.update_layout(
                title=f'Top Values: {col}',
                xaxis_title='Count',
                yaxis_title='Value',
                width=600,
                height=400
            )
            
            html.append(f'<div class="plot-container" id="cat-{col}"></div>')
            html.append(f'<script>Plotly.newPlot("cat-{col}", {fig.to_json()});</script>')
    
    return '\n'.join(html)


def _generate_html_footer() -> str:
    """Generate HTML footer."""
    return """
        <hr style="margin-top: 50px; border: none; border-top: 2px solid #ddd;">
        <p style="text-align: center; color: #888; padding: 20px;">
            Generated by <strong>SpeedyEDA v0.2.0</strong> • 
            <a href="https://github.com/Dawaman43/fasteda" style="color: #667eea;">⭐ Star on GitHub</a>
        </p>
    </div>
</body>
</html>
"""
