"""
FastEDA - One-line data exploration for developers & data scientists.
"""

__version__ = "0.1.0"

from fasteda.analysis import analyze
from fasteda.report import save_report

__all__ = ["analyze", "save_report", "__version__"]
