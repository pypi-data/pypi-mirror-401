"""
Research Trends Scopus - A comprehensive tool for research trend analysis.

This package provides tools to:
- Retrieve research data from the Scopus API
- Analyze publication trends and patterns
- Generate interactive dashboards
- Recommend research areas to explore
"""

from research_trends.client import ScopusClient
from research_trends.analyzer import TrendAnalyzer
from research_trends.dashboard import Dashboard
from research_trends.recommender import Recommender
from research_trends.config import Config

__version__ = "0.1.0"
__author__ = "Research Trends Team"
__email__ = "research-trends@example.com"

__all__ = [
    "ScopusClient",
    "TrendAnalyzer",
    "Dashboard",
    "Recommender",
    "Config",
    "__version__",
]
