"""
Research Trends - A comprehensive tool for research trend analysis.

This package provides tools to:
- Retrieve research data from multiple academic databases
- Analyze publication trends and patterns
- Generate interactive dashboards
- Recommend research areas to explore

Supported data sources:
- Scopus (requires API key)
- OpenAlex (free, recommended)
- Semantic Scholar (free)
- CrossRef (free)
- PubMed (free, biomedical)
- Google Scholar (scraped)
"""

# Legacy import for backward compatibility
from research_trends.client import ScopusClient

# New multi-source clients
from research_trends.clients import (
    ScopusClient as ScopusAPIClient,
    OpenAlexClient,
    SemanticScholarClient,
    CrossRefClient,
    PubMedClient,
    GoogleScholarClient,
    UnifiedClient,
    DataSource,
)

from research_trends.analyzer import TrendAnalyzer
from research_trends.dashboard import Dashboard
from research_trends.recommender import Recommender
from research_trends.config import Config

__version__ = "0.2.1"
__author__ = "Research Trends Team"
__email__ = "research-trends@example.com"

__all__ = [
    # Clients
    "ScopusClient",
    "OpenAlexClient",
    "SemanticScholarClient",
    "CrossRefClient",
    "PubMedClient",
    "GoogleScholarClient",
    "UnifiedClient",
    "DataSource",
    # Analysis
    "TrendAnalyzer",
    "Dashboard",
    "Recommender",
    "Config",
    "__version__",
]
