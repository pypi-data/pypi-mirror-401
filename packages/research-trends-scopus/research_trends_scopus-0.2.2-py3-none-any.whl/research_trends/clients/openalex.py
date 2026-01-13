"""
OpenAlex API client for retrieving research publication data.

OpenAlex is a free, open catalog of the world's scholarly papers,
researchers, journals, and institutions. No API key required.

Documentation: https://docs.openalex.org/
"""

import time
from datetime import datetime
from typing import Any, Dict, Iterator, List, Optional, Union
from urllib.parse import quote

import requests
from tqdm import tqdm

from research_trends.models import Publication, SearchResult


class OpenAlexError(Exception):
    """Exception raised for OpenAlex API errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None) -> None:
        super().__init__(message)
        self.status_code = status_code


class OpenAlexClient:
    """Client for interacting with the OpenAlex API.
    
    OpenAlex is completely free and requires no API key.
    It contains 250M+ scholarly works with citation data.
    
    Example:
        >>> client = OpenAlexClient()
        >>> results = client.search("machine learning", max_results=100)
        >>> for pub in results:
        ...     print(pub.title)
    """
    
    BASE_URL = "https://api.openalex.org"
    
    def __init__(
        self,
        email: Optional[str] = None,
        polite_pool: bool = True,
    ) -> None:
        """Initialize the OpenAlex client.
        
        Args:
            email: Your email for the polite pool (faster rate limits).
            polite_pool: Whether to use polite pool (recommended).
        """
        self.email = email
        self.polite_pool = polite_pool
        self._session = requests.Session()
        
        # Set user agent for polite pool
        if email and polite_pool:
            self._session.headers.update({
                "User-Agent": f"mailto:{email}",
            })
        
        self._last_request_time = 0.0
        # OpenAlex: 10 req/sec for polite pool, 1 req/sec otherwise
        self._min_interval = 0.1 if (email and polite_pool) else 1.0
    
    def _rate_limit(self) -> None:
        """Apply rate limiting."""
        elapsed = time.time() - self._last_request_time
        if elapsed < self._min_interval:
            time.sleep(self._min_interval - elapsed)
        self._last_request_time = time.time()
    
    def _request(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make a request to the OpenAlex API.
        
        Args:
            endpoint: API endpoint.
            params: Query parameters.
            
        Returns:
            JSON response data.
        """
        self._rate_limit()
        
        url = f"{self.BASE_URL}/{endpoint}"
        params = params or {}
        
        # Add email for polite pool
        if self.email:
            params["mailto"] = self.email
        
        try:
            response = self._session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if e.response else None
            raise OpenAlexError(f"HTTP error: {e}", status_code)
        except requests.exceptions.RequestException as e:
            raise OpenAlexError(f"Request failed: {e}")
    
    def _parse_work(self, work: Dict[str, Any]) -> Publication:
        """Parse an OpenAlex work into a Publication.
        
        Args:
            work: OpenAlex work data.
            
        Returns:
            Publication object.
        """
        # Extract authors
        authors = []
        affiliations = set()
        for authorship in work.get("authorships", []):
            author = authorship.get("author", {})
            if author.get("display_name"):
                authors.append(author["display_name"])
            for inst in authorship.get("institutions", []):
                if inst.get("display_name"):
                    affiliations.add(inst["display_name"])
        
        # Extract publication date
        pub_date = None
        pub_year = work.get("publication_year")
        if work.get("publication_date"):
            try:
                pub_date = datetime.strptime(work["publication_date"], "%Y-%m-%d")
            except ValueError:
                pass
        
        # Extract keywords/concepts
        keywords = []
        for concept in work.get("concepts", [])[:10]:  # Top 10 concepts
            if concept.get("display_name"):
                keywords.append(concept["display_name"].lower())
        
        # Extract source info
        source = work.get("primary_location", {}).get("source", {}) or {}
        
        return Publication(
            scopus_id=work.get("id", "").replace("https://openalex.org/", ""),
            eid=work.get("id", ""),
            doi=work.get("doi", "").replace("https://doi.org/", "") if work.get("doi") else "",
            title=work.get("title", "") or "",
            abstract=work.get("abstract", "") or "",
            authors=authors,
            affiliations=list(affiliations),
            keywords=keywords,
            publication_name=source.get("display_name", "") or "",
            issn=source.get("issn_l", "") or "",
            publication_date=pub_date,
            publication_year=pub_year,
            citation_count=work.get("cited_by_count", 0) or 0,
            document_type=work.get("type", "") or "",
            open_access=work.get("open_access", {}).get("is_oa", False),
            raw_data=work,
        )
    
    def search(
        self,
        query: str,
        start_year: Optional[int] = None,
        end_year: Optional[int] = None,
        max_results: Optional[int] = None,
        sort: str = "cited_by_count:desc",
        show_progress: bool = True,
        **kwargs: Any,
    ) -> SearchResult:
        """Search for publications in OpenAlex.
        
        Args:
            query: Search query.
            start_year: Earliest publication year.
            end_year: Latest publication year.
            max_results: Maximum number of results (default 100).
            sort: Sort order (e.g., 'cited_by_count:desc', 'publication_date:desc').
            show_progress: Show progress bar.
            **kwargs: Additional filter parameters.
            
        Returns:
            SearchResult containing publications and metadata.
        """
        max_results = max_results or 100
        per_page = min(200, max_results)  # OpenAlex max is 200
        
        # Build filter
        filters = []
        if start_year:
            filters.append(f"publication_year:>={start_year}")
        if end_year:
            filters.append(f"publication_year:<={end_year}")
        
        # Additional filters from kwargs
        for key, value in kwargs.items():
            filters.append(f"{key}:{value}")
        
        params: Dict[str, Any] = {
            "search": query,
            "per_page": per_page,
            "sort": sort,
        }
        
        if filters:
            params["filter"] = ",".join(filters)
        
        publications: List[Publication] = []
        cursor = "*"
        
        progress_bar = None
        if show_progress:
            progress_bar = tqdm(total=max_results, desc="Fetching publications")
        
        try:
            while len(publications) < max_results:
                params["cursor"] = cursor
                data = self._request("works", params)
                
                results = data.get("results", [])
                if not results:
                    break
                
                for work in results:
                    if len(publications) >= max_results:
                        break
                    publications.append(self._parse_work(work))
                    if progress_bar:
                        progress_bar.update(1)
                
                # Get next cursor
                meta = data.get("meta", {})
                cursor = meta.get("next_cursor")
                if not cursor:
                    break
                    
        finally:
            if progress_bar:
                progress_bar.close()
        
        return SearchResult(
            publications=publications,
            total_results=data.get("meta", {}).get("count", len(publications)),
            query=query,
            retrieved_at=datetime.now(),
        )
    
    def get_work(self, work_id: str) -> Publication:
        """Get a single work by ID.
        
        Args:
            work_id: OpenAlex work ID (e.g., 'W2741809807').
            
        Returns:
            Publication object.
        """
        if not work_id.startswith("W"):
            work_id = f"W{work_id}"
        
        data = self._request(f"works/{work_id}")
        return self._parse_work(data)
    
    def get_author(self, author_id: str) -> Dict[str, Any]:
        """Get author information.
        
        Args:
            author_id: OpenAlex author ID.
            
        Returns:
            Author data dictionary.
        """
        if not author_id.startswith("A"):
            author_id = f"A{author_id}"
        
        return self._request(f"authors/{author_id}")
    
    def get_institution(self, institution_id: str) -> Dict[str, Any]:
        """Get institution information.
        
        Args:
            institution_id: OpenAlex institution ID.
            
        Returns:
            Institution data dictionary.
        """
        if not institution_id.startswith("I"):
            institution_id = f"I{institution_id}"
        
        return self._request(f"institutions/{institution_id}")
    
    def search_authors(
        self,
        query: str,
        max_results: int = 25,
    ) -> List[Dict[str, Any]]:
        """Search for authors.
        
        Args:
            query: Search query.
            max_results: Maximum number of results.
            
        Returns:
            List of author data dictionaries.
        """
        params = {
            "search": query,
            "per_page": min(200, max_results),
        }
        data = self._request("authors", params)
        return data.get("results", [])[:max_results]
    
    def close(self) -> None:
        """Close the session."""
        self._session.close()
    
    def __enter__(self) -> "OpenAlexClient":
        return self
    
    def __exit__(self, *args: Any) -> None:
        self.close()
