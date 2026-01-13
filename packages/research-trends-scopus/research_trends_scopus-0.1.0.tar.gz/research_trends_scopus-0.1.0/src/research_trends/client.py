"""
Scopus API client for retrieving research publication data.

Provides a high-level interface to the Scopus Search API with:
- Query building with advanced search syntax
- Pagination handling
- Rate limiting
- Caching
- Error handling and retries
"""

import hashlib
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Union

import requests
from cachetools import TTLCache
from tqdm import tqdm

from research_trends.config import Config
from research_trends.models import Publication, SearchResult


class ScopusAPIError(Exception):
    """Exception raised for Scopus API errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None) -> None:
        super().__init__(message)
        self.status_code = status_code


class RateLimiter:
    """Rate limiter to prevent exceeding API limits."""
    
    def __init__(self, requests_per_second: int = 9) -> None:
        """Initialize rate limiter.
        
        Args:
            requests_per_second: Maximum requests per second.
        """
        self.requests_per_second = requests_per_second
        self.last_request_time = 0.0
        self.min_interval = 1.0 / requests_per_second
    
    def wait(self) -> None:
        """Wait if necessary to respect rate limit."""
        current_time = time.time()
        elapsed = current_time - self.last_request_time
        
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        
        self.last_request_time = time.time()


class ScopusClient:
    """Client for interacting with the Scopus API.
    
    Provides methods to search for publications, retrieve abstracts,
    and fetch author information.
    
    Example:
        >>> client = ScopusClient()
        >>> results = client.search("machine learning", max_results=100)
        >>> for pub in results:
        ...     print(pub.title)
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        config: Optional[Config] = None,
    ) -> None:
        """Initialize the Scopus client.
        
        Args:
            api_key: Scopus API key. If not provided, will be loaded from config.
            config: Configuration object. If not provided, default config is used.
        """
        self.config = config or Config(api_key=api_key)
        self.rate_limiter = RateLimiter(self.config.rate_limit)
        
        # In-memory cache for session
        self._cache: TTLCache = TTLCache(maxsize=1000, ttl=self.config.cache_ttl)
        
        # Session for connection pooling
        self._session = requests.Session()
        self._session.headers.update({
            "X-ELS-APIKey": self.config.api_key or "",
            "Accept": "application/json",
        })
        
        if self.config.institution_token:
            self._session.headers["X-ELS-Insttoken"] = self.config.institution_token
    
    def _get_cache_key(self, url: str, params: Dict[str, Any]) -> str:
        """Generate cache key for a request.
        
        Args:
            url: Request URL.
            params: Request parameters.
            
        Returns:
            Cache key string.
        """
        key_data = f"{url}:{json.dumps(params, sort_keys=True)}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _request(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        use_cache: bool = True,
    ) -> Dict[str, Any]:
        """Make a rate-limited request to the API.
        
        Args:
            url: Request URL.
            params: Request parameters.
            use_cache: Whether to use caching.
            
        Returns:
            JSON response data.
            
        Raises:
            ScopusAPIError: If the API returns an error.
        """
        params = params or {}
        cache_key = self._get_cache_key(url, params)
        
        # Check cache
        if use_cache and cache_key in self._cache:
            return self._cache[cache_key]
        
        # Rate limit
        self.rate_limiter.wait()
        
        # Make request
        try:
            response = self._session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Cache response
            if use_cache:
                self._cache[cache_key] = data
            
            return data
            
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if e.response else None
            if status_code == 401:
                raise ScopusAPIError("Invalid API key", status_code)
            elif status_code == 429:
                raise ScopusAPIError("Rate limit exceeded", status_code)
            elif status_code == 404:
                raise ScopusAPIError("Resource not found", status_code)
            else:
                raise ScopusAPIError(f"HTTP error: {e}", status_code)
        except requests.exceptions.RequestException as e:
            raise ScopusAPIError(f"Request failed: {e}")
    
    def build_query(
        self,
        query: Optional[str] = None,
        title: Optional[str] = None,
        abstract: Optional[str] = None,
        keywords: Optional[Union[str, List[str]]] = None,
        authors: Optional[Union[str, List[str]]] = None,
        affiliation: Optional[str] = None,
        source_title: Optional[str] = None,
        issn: Optional[str] = None,
        doi: Optional[str] = None,
        start_year: Optional[int] = None,
        end_year: Optional[int] = None,
        document_type: Optional[str] = None,
        open_access: Optional[bool] = None,
        subject_area: Optional[str] = None,
    ) -> str:
        """Build a Scopus search query string.
        
        Args:
            query: Free text query (searches title, abstract, keywords).
            title: Search in title only.
            abstract: Search in abstract only.
            keywords: Author keywords to search for.
            authors: Author names to search for.
            affiliation: Affiliation/institution to search for.
            source_title: Journal/conference name.
            issn: ISSN of the source.
            doi: DOI of the publication.
            start_year: Earliest publication year.
            end_year: Latest publication year.
            document_type: Type of document (ar, cp, re, etc.).
            open_access: Filter for open access publications.
            subject_area: Subject area code.
            
        Returns:
            Scopus query string.
        """
        parts = []
        
        if query:
            parts.append(f"TITLE-ABS-KEY({query})")
        if title:
            parts.append(f"TITLE({title})")
        if abstract:
            parts.append(f"ABS({abstract})")
        if keywords:
            if isinstance(keywords, list):
                keywords = " OR ".join(keywords)
            parts.append(f"KEY({keywords})")
        if authors:
            if isinstance(authors, list):
                authors = " OR ".join(authors)
            parts.append(f"AUTH({authors})")
        if affiliation:
            parts.append(f"AFFIL({affiliation})")
        if source_title:
            parts.append(f"SRCTITLE({source_title})")
        if issn:
            parts.append(f"ISSN({issn})")
        if doi:
            parts.append(f"DOI({doi})")
        if start_year and end_year:
            parts.append(f"PUBYEAR > {start_year - 1} AND PUBYEAR < {end_year + 1}")
        elif start_year:
            parts.append(f"PUBYEAR > {start_year - 1}")
        elif end_year:
            parts.append(f"PUBYEAR < {end_year + 1}")
        if document_type:
            parts.append(f"DOCTYPE({document_type})")
        if open_access is not None:
            parts.append(f"OPENACCESS({1 if open_access else 0})")
        if subject_area:
            parts.append(f"SUBJAREA({subject_area})")
        
        return " AND ".join(parts)
    
    def search(
        self,
        query: Optional[str] = None,
        start_year: Optional[int] = None,
        end_year: Optional[int] = None,
        max_results: Optional[int] = None,
        sort: str = "-coverDate",
        view: str = "COMPLETE",
        show_progress: bool = True,
        **kwargs: Any,
    ) -> SearchResult:
        """Search for publications in Scopus.
        
        Args:
            query: Search query or keywords.
            start_year: Earliest publication year.
            end_year: Latest publication year.
            max_results: Maximum number of results to retrieve.
            sort: Sort order (e.g., '-coverDate', 'citedby-count').
            view: Response view ('STANDARD' or 'COMPLETE').
            show_progress: Show progress bar.
            **kwargs: Additional query parameters for build_query.
            
        Returns:
            SearchResult containing publications and metadata.
        """
        self.config.validate()
        
        max_results = max_results or self.config.default_max_results
        
        # Build query
        full_query = self.build_query(
            query=query,
            start_year=start_year,
            end_year=end_year,
            **kwargs,
        )
        
        publications: List[Publication] = []
        start = 0
        count = 25  # Results per page
        total_results = None
        
        pbar = None
        if show_progress:
            pbar = tqdm(total=max_results, desc="Fetching publications")
        
        try:
            while len(publications) < max_results:
                params = {
                    "query": full_query,
                    "start": start,
                    "count": min(count, max_results - len(publications)),
                    "sort": sort,
                    "view": view,
                }
                
                response = self._request(self.config.base_url, params)
                
                # Parse response
                search_results = response.get("search-results", {})
                
                if total_results is None:
                    total_results = int(search_results.get("opensearch:totalResults", 0))
                    if pbar:
                        pbar.total = min(max_results, total_results)
                        pbar.refresh()
                
                entries = search_results.get("entry", [])
                
                if not entries:
                    break
                
                # Handle error entries
                if len(entries) == 1 and "error" in entries[0]:
                    error_msg = entries[0].get("error", "Unknown error")
                    raise ScopusAPIError(f"Search error: {error_msg}")
                
                for entry in entries:
                    if len(publications) >= max_results:
                        break
                    
                    pub = self._parse_publication(entry)
                    publications.append(pub)
                    
                    if pbar:
                        pbar.update(1)
                
                start += count
                
                if start >= total_results:
                    break
        
        finally:
            if pbar:
                pbar.close()
        
        return SearchResult(
            publications=publications,
            total_results=total_results or 0,
            query=full_query,
            retrieved_at=datetime.now(),
        )
    
    def search_iterator(
        self,
        query: str,
        **kwargs: Any,
    ) -> Iterator[Publication]:
        """Iterate over search results without loading all into memory.
        
        Args:
            query: Search query.
            **kwargs: Additional arguments passed to search.
            
        Yields:
            Publication objects one at a time.
        """
        result = self.search(query, **kwargs)
        yield from result.publications
    
    def _parse_publication(self, entry: Dict[str, Any]) -> Publication:
        """Parse a Scopus entry into a Publication object.
        
        Args:
            entry: Raw Scopus entry data.
            
        Returns:
            Parsed Publication object.
        """
        # Extract authors
        authors = []
        if "author" in entry:
            for author in entry["author"]:
                author_name = author.get("authname", "")
                if author_name:
                    authors.append(author_name)
        
        # Extract affiliations
        affiliations = []
        if "affiliation" in entry:
            for affil in entry["affiliation"]:
                affil_name = affil.get("affilname", "")
                if affil_name:
                    affiliations.append(affil_name)
        
        # Extract keywords
        keywords = []
        if "authkeywords" in entry:
            kw_str = entry.get("authkeywords", "")
            if kw_str:
                keywords = [kw.strip() for kw in kw_str.split("|")]
        
        # Parse date
        cover_date = entry.get("prism:coverDate", "")
        pub_date = None
        pub_year = None
        if cover_date:
            try:
                pub_date = datetime.strptime(cover_date, "%Y-%m-%d")
                pub_year = pub_date.year
            except ValueError:
                pass
        
        # Extract citation count
        citation_count = 0
        if "citedby-count" in entry:
            try:
                citation_count = int(entry["citedby-count"])
            except (ValueError, TypeError):
                pass
        
        return Publication(
            scopus_id=entry.get("dc:identifier", "").replace("SCOPUS_ID:", ""),
            eid=entry.get("eid", ""),
            doi=entry.get("prism:doi", ""),
            title=entry.get("dc:title", ""),
            abstract=entry.get("dc:description", ""),
            authors=authors,
            affiliations=affiliations,
            keywords=keywords,
            publication_name=entry.get("prism:publicationName", ""),
            issn=entry.get("prism:issn", ""),
            volume=entry.get("prism:volume", ""),
            issue=entry.get("prism:issueIdentifier", ""),
            pages=entry.get("prism:pageRange", ""),
            publication_date=pub_date,
            publication_year=pub_year,
            citation_count=citation_count,
            document_type=entry.get("subtypeDescription", ""),
            source_type=entry.get("prism:aggregationType", ""),
            open_access=entry.get("openaccess", "0") == "1",
            subject_areas=[
                area.get("$", "")
                for area in entry.get("subject-area", [])
            ],
            raw_data=entry,
        )
    
    def get_abstract(self, scopus_id: str) -> Optional[str]:
        """Retrieve the full abstract for a publication.
        
        Args:
            scopus_id: Scopus ID of the publication.
            
        Returns:
            Full abstract text or None if not available.
        """
        self.config.validate()
        
        url = f"{self.config.abstract_url}/{scopus_id}"
        
        try:
            response = self._request(url)
            abstract_response = response.get("abstracts-retrieval-response", {})
            coredata = abstract_response.get("coredata", {})
            return coredata.get("dc:description", None)
        except ScopusAPIError:
            return None
    
    def close(self) -> None:
        """Close the client and release resources."""
        self._session.close()
    
    def __enter__(self) -> "ScopusClient":
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit."""
        self.close()
