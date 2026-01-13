"""
Research data clients for multiple academic databases.

Provides unified access to:
- Scopus (Elsevier)
- OpenAlex (free, open source)
- Semantic Scholar (free with API key)
- CrossRef (free)
- PubMed/NCBI (free, biomedical)
- Google Scholar (scraped, use responsibly)
"""

from research_trends.clients.scopus import ScopusClient, ScopusAPIError
from research_trends.clients.openalex import OpenAlexClient
from research_trends.clients.semantic_scholar import SemanticScholarClient
from research_trends.clients.crossref import CrossRefClient
from research_trends.clients.pubmed import PubMedClient
from research_trends.clients.google_scholar import GoogleScholarClient
from research_trends.clients.unified import UnifiedClient, DataSource

__all__ = [
    "ScopusClient",
    "ScopusAPIError",
    "OpenAlexClient",
    "SemanticScholarClient",
    "CrossRefClient",
    "PubMedClient",
    "GoogleScholarClient",
    "UnifiedClient",
    "DataSource",
]
