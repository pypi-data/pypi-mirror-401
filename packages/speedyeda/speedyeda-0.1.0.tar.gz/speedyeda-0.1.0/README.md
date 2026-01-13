# 🚀 FastEDA - One-Line Data Exploration

**Instant insights, beautiful visualizations, and comprehensive summaries** from datasets with just one command.

## ✨ Features

- 📊 **Automatic Statistics** - Mean, median, mode, min/max, std, unique counts, missing values
- 🔍 **Missing Value Analysis** - Highlights and suggestions for handling missing data
- 📈 **Auto Visualizations** - Histograms, boxplots, correlation heatmaps, and more
- 🎨 **Beautiful Terminal Output** - Colorful, emoji-rich displays using `rich`
- 🎭 **Fun Mode** - ASCII charts and emojis for screenshot-worthy results
- 📄 **Export Reports** - Save as PDF, HTML, or interactive dashboards
- 🔧 **Presets** - Pre-configured analysis for common use cases (ecommerce, surveys, finance)
- 🔌 **Plugin System** - Extend with custom visualizations and metrics
- 🤝 **Interactive Mode** - Guided column and plot selection
- 📦 **Batch Processing** - Analyze multiple datasets at once

## 🚀 Quick Start

### Installation

```bash
pip install fasteda
```

### Basic Usage

```bash
# Quick exploration
fasteda sales.csv

# Fun mode with emojis and colors
fasteda survey.xlsx --fun

# Use a preset for common tasks
fasteda products.csv --preset ecommerce

# Interactive mode
fasteda data.csv --interactive

# Batch processing
fasteda file1.csv file2.csv file3.csv
```

### Python API

```python
import pandas as pd
from fasteda import analyze, save_report

df = pd.read_csv("sales.csv")

# Generate EDA
results = analyze(df, fun=True)

# Save report
save_report(results, "sales_report.pdf")
```

## 📋 CLI Options

| Flag | Description |
|------|-------------|
| `--fun` | Adds emojis and colorful output |
| `--summary` | Plain text summary with insights |
| `--plots` | Generate and save visualizations |
| `--save <file>` | Export report (PDF/HTML) |
| `--interactive` | Interactive column/plot selection |
| `--preset <name>` | Use preset (ecommerce, survey, finance) |
| `--columns <cols>` | Analyze specific columns only |
| `--batch` | Process multiple files |
| `--quiet` | Suppress terminal output |

## 🎯 Presets

FastEDA includes built-in presets for common scenarios:

- **ecommerce** - Product analysis, sales trends, customer behavior
- **survey** - Response distributions, sentiment analysis, demographics
- **finance** - Time series, correlations, risk metrics

## 🔌 Plugins

Extend FastEDA with custom plugins:

```python
from fasteda.plugins import register_plugin

@register_plugin("custom_viz")
def my_visualization(df):
    # Your custom analysis
    pass
```

## 📦 Supported Formats

- CSV (`.csv`)
- Excel (`.xlsx`, `.xls`)
- JSON (`.json`)
- Parquet (`.parquet`)

## 🤝 Contributing

Contributions welcome! Share your presets and plugins with the community.

## 📄 License

MIT License - see LICENSE file for details.
