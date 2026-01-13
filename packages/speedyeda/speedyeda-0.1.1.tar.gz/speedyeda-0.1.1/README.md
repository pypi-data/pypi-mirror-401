# 🚀 SpeedyEDA - Lightning-Fast Data Exploration

[![PyPI version](https://badge.fury.io/py/speedyeda.svg)](https://badge.fury.io/py/speedyeda)
[![GitHub stars](https://img.shields.io/github/stars/Dawaman43/fasteda?style=social)](https://github.com/Dawaman43/fasteda)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Instant insights, beautiful visualizations, and comprehensive summaries** from datasets with just one command.

**Stop writing boilerplate!** SpeedyEDA gives you complete exploratory data analysis in seconds. Perfect for data scientists, analysts, and developers who want instant insights without the setup.

---

## 💡 **Love this project? [⭐ Star us on GitHub!](https://github.com/Dawaman43/fasteda)** 

Your star helps others discover SpeedyEDA and motivates us to keep improving! 🙏

---

## ✨ Features

- 📊 **Automatic Statistics** - Mean, median, mode, min/max, std, skewness, kurtosis
- 🔍 **Missing Value Analysis** - Highlights and actionable suggestions
- 📈 **Auto Visualizations** - Histograms, boxplots, correlation heatmaps, and more
- 🎨 **Beautiful Terminal Output** - Colorful, emoji-rich displays using `rich`
- 🎭 **Fun Mode** - Screenshot-worthy results with emojis and ASCII art
- 📄 **Export Reports** - Save as JSON or text with one flag
- 🔧 **Presets** - Pre-configured analysis (ecommerce, surveys, finance)
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
# Quick exploration with beautiful output
fasteda sales.csv --fun

# Use a preset for instant domain-specific insights
fasteda products.csv --preset ecommerce

# Generate plots automatically
fasteda data.csv --plots

# Interactive mode - let SpeedyEDA guide you
fasteda survey.xlsx --interactive

# Batch processing
fasteda file1.csv file2.csv file3.csv --batch
```

### Python API

```python
import pandas as pd
from fasteda import analyze, save_report

df = pd.read_csv("sales.csv")

# Generate comprehensive EDA
results = analyze(df, fun=True)

# Save detailed report
save_report(results, "sales_report.json")
```

## 📋 CLI Options

| Flag | Description |
|------|-------------|
| `--fun` | 🎉 Emojis and colorful output (highly recommended!) |
| `--summary` | 📝 Plain text summary with insights |
| `--plots` | 📊 Generate and save visualizations |
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
