"""
Unified client for searching across multiple academic databases.

Provides a single interface to query multiple data sources:
- Scopus (requires API key)
- OpenAlex (free, recommended)
- Semantic Scholar (free with optional API key)
- CrossRef (free)
- PubMed (free, biomedical focus)
- Google Scholar (scraped, use sparingly)
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Type, Union

from research_trends.models import Publication, SearchResult


class DataSource(Enum):
    """Available data sources for publication search."""
    
    SCOPUS = auto()
    OPENALEX = auto()
    SEMANTIC_SCHOLAR = auto()
    CROSSREF = auto()
    PUBMED = auto()
    GOOGLE_SCHOLAR = auto()
    
    @classmethod
    def free_sources(cls) -> List["DataSource"]:
        """Get list of free data sources."""
        return [
            cls.OPENALEX,
            cls.SEMANTIC_SCHOLAR,
            cls.CROSSREF,
            cls.PUBMED,
        ]
    
    @classmethod
    def recommended(cls) -> "DataSource":
        """Get the recommended default data source."""
        return cls.OPENALEX


@dataclass
class UnifiedSearchResult:
    """Search results from multiple data sources."""
    
    results: Dict[DataSource, SearchResult]
    query: str
    retrieved_at: datetime
    
    @property
    def total_results(self) -> int:
        """Get total results across all sources."""
        return sum(r.total_results for r in self.results.values())
    
    @property
    def all_publications(self) -> List[Publication]:
        """Get all publications from all sources."""
        pubs = []
        for result in self.results.values():
            pubs.extend(result.publications)
        return pubs
    
    def merge_deduplicated(self) -> List[Publication]:
        """Merge results, removing duplicates by DOI or title.
        
        Returns:
            Deduplicated list of publications.
        """
        seen_dois: set = set()
        seen_titles: set = set()
        unique_pubs: List[Publication] = []
        
        for result in self.results.values():
            for pub in result.publications:
                # Check DOI
                if pub.doi:
                    doi_lower = pub.doi.lower()
                    if doi_lower in seen_dois:
                        continue
                    seen_dois.add(doi_lower)
                
                # Check title similarity
                title_key = pub.title.lower()[:100] if pub.title else ""
                if title_key and title_key in seen_titles:
                    continue
                if title_key:
                    seen_titles.add(title_key)
                
                unique_pubs.append(pub)
        
        return unique_pubs


class UnifiedClient:
    """Unified client for searching multiple academic databases.
    
    Provides a single interface to query multiple data sources with
    automatic fallback, parallel queries, and result merging.
    
    Example:
        >>> client = UnifiedClient()
        >>> # Search default source (OpenAlex)
        >>> results = client.search("machine learning", max_results=100)
        >>> 
        >>> # Search multiple sources
        >>> results = client.search_multiple(
        ...     "deep learning",
        ...     sources=[DataSource.OPENALEX, DataSource.SEMANTIC_SCHOLAR],
        ...     max_results=50
        ... )
        >>> 
        >>> # Get deduplicated results
        >>> publications = results.merge_deduplicated()
    """
    
    def __init__(
        self,
        scopus_api_key: Optional[str] = None,
        semantic_scholar_api_key: Optional[str] = None,
        pubmed_api_key: Optional[str] = None,
        email: Optional[str] = None,
        default_source: DataSource = DataSource.OPENALEX,
    ) -> None:
        """Initialize the unified client.
        
        Args:
            scopus_api_key: Scopus API key (required for Scopus).
            semantic_scholar_api_key: Semantic Scholar API key (optional).
            pubmed_api_key: PubMed/NCBI API key (optional).
            email: Your email for polite pool access (recommended).
            default_source: Default data source for single-source searches.
        """
        self.scopus_api_key = scopus_api_key
        self.semantic_scholar_api_key = semantic_scholar_api_key
        self.pubmed_api_key = pubmed_api_key
        self.email = email
        self.default_source = default_source
        
        # Lazy-loaded clients
        self._clients: Dict[DataSource, Any] = {}
    
    def _get_client(self, source: DataSource) -> Any:
        """Get or create a client for a data source.
        
        Args:
            source: Data source.
            
        Returns:
            Client instance.
        """
        if source in self._clients:
            return self._clients[source]
        
        client: Any = None
        
        if source == DataSource.SCOPUS:
            from research_trends.clients.scopus import ScopusClient
            if not self.scopus_api_key:
                raise ValueError("Scopus API key required")
            client = ScopusClient(api_key=self.scopus_api_key)
            
        elif source == DataSource.OPENALEX:
            from research_trends.clients.openalex import OpenAlexClient
            client = OpenAlexClient(email=self.email)
            
        elif source == DataSource.SEMANTIC_SCHOLAR:
            from research_trends.clients.semantic_scholar import SemanticScholarClient
            client = SemanticScholarClient(api_key=self.semantic_scholar_api_key)
            
        elif source == DataSource.CROSSREF:
            from research_trends.clients.crossref import CrossRefClient
            client = CrossRefClient(email=self.email)
            
        elif source == DataSource.PUBMED:
            from research_trends.clients.pubmed import PubMedClient
            client = PubMedClient(api_key=self.pubmed_api_key, email=self.email)
            
        elif source == DataSource.GOOGLE_SCHOLAR:
            from research_trends.clients.google_scholar import GoogleScholarClient
            client = GoogleScholarClient()
        
        self._clients[source] = client
        return client
    
    def search(
        self,
        query: str,
        source: Optional[DataSource] = None,
        start_year: Optional[int] = None,
        end_year: Optional[int] = None,
        max_results: Optional[int] = None,
        show_progress: bool = True,
        **kwargs: Any,
    ) -> SearchResult:
        """Search a single data source.
        
        Args:
            query: Search query.
            source: Data source (default: OpenAlex).
            start_year: Earliest publication year.
            end_year: Latest publication year.
            max_results: Maximum number of results.
            show_progress: Show progress bar.
            **kwargs: Additional source-specific parameters.
            
        Returns:
            SearchResult containing publications.
        """
        source = source or self.default_source
        client = self._get_client(source)
        
        return client.search(
            query,
            start_year=start_year,
            end_year=end_year,
            max_results=max_results,
            show_progress=show_progress,
            **kwargs,
        )
    
    def search_multiple(
        self,
        query: str,
        sources: Optional[List[DataSource]] = None,
        start_year: Optional[int] = None,
        end_year: Optional[int] = None,
        max_results: Optional[int] = None,
        show_progress: bool = True,
        **kwargs: Any,
    ) -> UnifiedSearchResult:
        """Search multiple data sources.
        
        Args:
            query: Search query.
            sources: List of data sources (default: all free sources).
            start_year: Earliest publication year.
            end_year: Latest publication year.
            max_results: Maximum results per source.
            show_progress: Show progress bar.
            **kwargs: Additional source-specific parameters.
            
        Returns:
            UnifiedSearchResult with results from all sources.
        """
        sources = sources or DataSource.free_sources()
        results: Dict[DataSource, SearchResult] = {}
        
        for source in sources:
            try:
                result = self.search(
                    query,
                    source=source,
                    start_year=start_year,
                    end_year=end_year,
                    max_results=max_results,
                    show_progress=show_progress,
                    **kwargs,
                )
                results[source] = result
            except Exception as e:
                print(f"Warning: {source.name} search failed: {e}")
        
        return UnifiedSearchResult(
            results=results,
            query=query,
            retrieved_at=datetime.now(),
        )
    
    def search_with_fallback(
        self,
        query: str,
        preferred_sources: Optional[List[DataSource]] = None,
        start_year: Optional[int] = None,
        end_year: Optional[int] = None,
        max_results: Optional[int] = None,
        show_progress: bool = True,
        **kwargs: Any,
    ) -> SearchResult:
        """Search with automatic fallback to next source on failure.
        
        Args:
            query: Search query.
            preferred_sources: Ordered list of sources to try.
            start_year: Earliest publication year.
            end_year: Latest publication year.
            max_results: Maximum number of results.
            show_progress: Show progress bar.
            **kwargs: Additional source-specific parameters.
            
        Returns:
            SearchResult from first successful source.
        """
        sources = preferred_sources or [
            DataSource.OPENALEX,
            DataSource.SEMANTIC_SCHOLAR,
            DataSource.CROSSREF,
            DataSource.PUBMED,
        ]
        
        last_error: Optional[Exception] = None
        
        for source in sources:
            try:
                return self.search(
                    query,
                    source=source,
                    start_year=start_year,
                    end_year=end_year,
                    max_results=max_results,
                    show_progress=show_progress,
                    **kwargs,
                )
            except Exception as e:
                last_error = e
                if show_progress:
                    print(f"Warning: {source.name} failed, trying next source...")
        
        raise RuntimeError(f"All data sources failed. Last error: {last_error}")
    
    def get_publication_by_doi(
        self,
        doi: str,
        source: Optional[DataSource] = None,
    ) -> Publication:
        """Get a single publication by DOI.
        
        Args:
            doi: Digital Object Identifier.
            source: Data source to use (default: CrossRef).
            
        Returns:
            Publication object.
        """
        source = source or DataSource.CROSSREF
        client = self._get_client(source)
        
        if source == DataSource.CROSSREF:
            return client.get_work(doi)
        elif source == DataSource.OPENALEX:
            return client.get_work(f"https://doi.org/{doi}")
        elif source == DataSource.SEMANTIC_SCHOLAR:
            return client.get_paper(f"DOI:{doi}")
        else:
            # Fallback to search
            result = self.search(f'"{doi}"', source=source, max_results=1)
            if result.publications:
                return result.publications[0]
            raise ValueError(f"Publication not found: {doi}")
    
    def available_sources(self) -> List[DataSource]:
        """Get list of available data sources based on API keys.
        
        Returns:
            List of available DataSource enums.
        """
        sources = [
            DataSource.OPENALEX,
            DataSource.CROSSREF,
            DataSource.PUBMED,
            DataSource.GOOGLE_SCHOLAR,
        ]
        
        # Add Semantic Scholar (always available, API key optional)
        sources.append(DataSource.SEMANTIC_SCHOLAR)
        
        # Add Scopus if API key available
        if self.scopus_api_key:
            sources.append(DataSource.SCOPUS)
        
        return sources
    
    def close(self) -> None:
        """Close all client sessions."""
        for client in self._clients.values():
            if hasattr(client, 'close'):
                client.close()
        self._clients.clear()
    
    def __enter__(self) -> "UnifiedClient":
        return self
    
    def __exit__(self, *args: Any) -> None:
        self.close()


# Convenience function
def quick_search(
    query: str,
    max_results: int = 100,
    source: DataSource = DataSource.OPENALEX,
) -> List[Publication]:
    """Quick search using default settings.
    
    Args:
        query: Search query.
        max_results: Maximum number of results.
        source: Data source to use.
        
    Returns:
        List of Publication objects.
    """
    with UnifiedClient() as client:
        result = client.search(query, source=source, max_results=max_results)
        return result.publications
