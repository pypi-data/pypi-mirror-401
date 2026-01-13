# 🚀 SpeedyEDA - Production-Ready Data Exploration

[![PyPI version](https://badge.fury.io/py/speedyeda.svg)](https://badge.fury.io/py/speedyeda)
[![GitHub stars](https://img.shields.io/github/stars/Dawaman43/fasteda?style=social)](https://github.com/Dawaman43/fasteda)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Professional-grade exploratory data analysis in one command.**

**Stop writing boilerplate!** SpeedyEDA gives you complete exploratory data analysis in seconds — now with **advanced statistical methods**, **data quality alerts**, and **interactive HTML reports** that rival industry-standard tools.

---

## 💡 **Love this project? [⭐ Star us on GitHub!](https://github.com/Dawaman43/fasteda)** 

Your star helps others discover SpeedyEDA and motivates us to keep improving! 🙏

---

## 🆕 What's New in v0.2.0

✨ **Advanced Statistical Analysis**
- Multiple correlation methods (Pearson, Spearman, Kendall)
- Enhanced outlier detection (IQR + Z-score)
- Detailed quantile statistics (5th, 95th percentiles)
- Normality tests (Shapiro-Wilk)

🚨 **Automated Data Quality Alerts**
- Multicollinearity detection
- High cardinality warnings
- Duplicate row detection
- Class imbalance analysis
- Excessive missing value alerts
- Mixed data type detection

📊 **Interactive HTML Reports**
- Beautiful Plotly visualizations
- Click-to-zoom charts
- Standalone HTML files
- Professional styling

## 📊 SpeedyEDA vs The Competition

| Feature | SpeedyEDA | ydata-profiling | Sweetviz | D-Tale |
|---------|-----------|----------------|----------|--------|
| **Basic Statistics** | ✅ | ✅ | ✅ | ✅ |
| **Multiple Correlations** | ✅ Pearson/Spearman/Kendall | ✅ | ✅ | ✅ |
| **Outlier Detection** | ✅ IQR + Z-score | ✅ | ✅ | ⚠️ |
| **Data Quality Alerts** | ✅ **8 types** | ✅ | ⚠️ Limited | ❌ |
| **Interactive HTML** | ✅ Plotly | ✅ | ✅ | ✅ Flask |
| **Dataset Comparison** | 🔜 v0.3.0 | ❌ | ✅ | ❌ |
| **Target Analysis** | 🔜 v0.3.0 | ✅ | ✅ | ⚠️ |
| **Speed (10K rows)** | ⚡ <1s | ~10s | ~5s | ~3s |
| **Installation Size** | 📦 ~100MB | ~500MB | ~200MB | ~300MB |
| **One-Line CLI** | ✅ | ❌ | ❌ | ❌ |
| **Fun Mode** | ✅ 🎉 | ❌ | ❌ | ❌ |

**Bottom Line**: SpeedyEDA combines the **speed** of simple tools with the **features** of professional ones, plus a delightful UX.

---

## ✨ Core Features

- 📊 **Automatic Statistics** - Mean, median, mode, std, skewness, kurtosis, detailed quantiles
- 🔍 **Advanced Missing Value Analysis** - Patterns, correlations, recommendations
- 📈 **Auto Visualizations** - Histograms, boxplots, correlation heatmaps (static + interactive)
- 🔗 **Multiple Correlation Methods** - Pearson (linear), Spearman (monotonic), Kendall (ordinal)
- 🎯 **Smart Outlier Detection** - IQR method + Z-score with configurable thresholds
- 🚨 **Data Quality Alerts** - Multicollinearity, high cardinality, duplicates, class imbalance, and more
- 🎨 **Beautiful Terminal Output** - Colorful, emoji-rich displays using `rich`
- 📄 **Interactive HTML Reports** - Professional Plotly-based reports with click-to-zoom
- 🔧 **Smart Presets** - Pre-configured for ecommerce, surveys, finance
- 🔌 **Plugin System** - Extend with custom visualizations and metrics
- 🤝 **Interactive Mode** - Guided column and plot selection
- 📦 **Batch Processing** - Analyze multiple datasets at once

## 🚀 Quick Start

### Installation

```bash
pip install speedyeda
```

### Basic Usage

```bash
# Full analysis with data quality alerts
fasteda sales.csv --fun

# Generate interactive HTML report
fasteda data.csv --html report.html

# Use preset with plots and HTML
fasteda products.csv --preset ecommerce --plots --html ecommerce_report.html

# Interactive mode
fasteda survey.xlsx --interactive

# Batch processing with HTML reports
fasteda file1.csv file2.csv file3.csv --batch --html

# Disable advanced features for speed
fasteda huge_dataset.csv --no-advanced
```

### Python API

```python
import pandas as pd
from fasteda import analyze, save_report

df = pd.read_csv("sales.csv")

# Full analysis with advanced features
results = analyze(df, fun=True, advanced=True)

# Check data quality alerts
if results['quality_alerts']:
    for alert in results['quality_alerts']:
        print(alert.message)

# Multiple correlation methods
correlations = results['advanced_correlations']
print(correlations['spearman'])  # Spearman correlation matrix

# Outlier detection
outliers = results['outliers']
for col, info in outliers.items():
    print(f"{col}: {info['count']} outliers ({info['percentage']:.1f}%)")

# Save detailed report
save_report(results, "sales_report.json")
```

## 📋 CLI Options

| Flag | Description |
|------|-------------|
| `--fun` | 🎉 Emojis and colorful output (highly recommended!) |
| `--html <file>` | 📊 **NEW!** Generate interactive HTML report |
| `--no-advanced` | ⚡ Disable advanced features for faster processing |
| `--summary` | 📝 Plain text summary with insights |
| `--plots` | 📊 Generate and save static visualizations |
| `--save <file>` | 💾 Export report (JSON/TXT) |
| `--interactive` | 🤝 Interactive column/plot selection |
| `--preset <name>` | 🎯 Use preset (ecommerce, survey, finance) |
| `--columns <cols>` | 🎯 Analyze specific columns only |
| `--batch` | 📦 Process multiple files |
| `--quiet` | 🤫 Suppress terminal output |

## 🎯 Smart Presets

SpeedyEDA includes built-in presets tailored for common scenarios:

- **📦 ecommerce** - Product analysis, sales trends, customer behavior
- **📋 survey** - Response distributions, sentiment analysis, demographics  
- **💰 finance** - Time series, correlations, risk metrics
- **🔧 general** - Comprehensive all-purpose exploration

```bash
fasteda sales.csv --preset ecommerce --plots --fun
```

## 🔌 Extend with Plugins

Build custom analysis functions:

```python
from fasteda.plugins import register_plugin

@register_plugin("outlier_detection")
def detect_outliers(df, threshold=1.5):
    # Your custom analysis
    return results
```

## 📦 Supported Formats

- 📄 CSV (`.csv`)
- 📊 Excel (`.xlsx`, `.xls`)
- 🗂️ JSON (`.json`)
- ⚡ Parquet (`.parquet`)

## 🌟 Why SpeedyEDA?

**Before SpeedyEDA:**
```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("data.csv")
print(df.describe())
print(df.info())
print(df.isnull().sum())
plt.figure(figsize=(10,6))
# ... 20+ more lines of boilerplate ...
```

**With SpeedyEDA:**
```bash
fasteda data.csv --fun
```

✨ **One command. Complete analysis. Beautiful output.**

## 🤝 Contributing

We'd love your help making SpeedyEDA even better! 

- 🐛 Found a bug? [Open an issue](https://github.com/Dawaman43/fasteda/issues)
- 💡 Have an idea? [Start a discussion](https://github.com/Dawaman43/fasteda/discussions)
- 🎨 Want to contribute? [Submit a PR](https://github.com/Dawaman43/fasteda/pulls)
- ⭐ **Love SpeedyEDA? [Star the repo!](https://github.com/Dawaman43/fasteda)**

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

<div align="center">

**Made with ❤️ by [Dawaman](https://github.com/Dawaman43)**

If SpeedyEDA saves you time, [⭐ star the repo](https://github.com/Dawaman43/fasteda) to show your support!

[🐛 Report Bug](https://github.com/Dawaman43/fasteda/issues) · [💡 Request Feature](https://github.com/Dawaman43/fasteda/issues) · [📖 Documentation](https://github.com/Dawaman43/fasteda#readme)

</div>
