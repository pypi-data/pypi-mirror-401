"""
CrossRef API client for retrieving research publication metadata.

CrossRef is a free service providing metadata for 150M+ DOIs.
No API key required, but polite pool with email is recommended.

Documentation: https://api.crossref.org/swagger-ui/index.html
"""

import time
from datetime import datetime
from typing import Any, Dict, List, Optional

import requests
from tqdm import tqdm

from research_trends.models import Publication, SearchResult


class CrossRefError(Exception):
    """Exception raised for CrossRef API errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None) -> None:
        super().__init__(message)
        self.status_code = status_code


class CrossRefClient:
    """Client for interacting with the CrossRef API.
    
    CrossRef provides free access to metadata for 150M+ scholarly works.
    No API key required. Email recommended for polite pool access.
    
    Note: CrossRef provides metadata only, not citation counts.
    
    Example:
        >>> client = CrossRefClient(email="your@email.com")
        >>> results = client.search("neural networks", max_results=100)
        >>> for pub in results:
        ...     print(pub.title, pub.doi)
    """
    
    BASE_URL = "https://api.crossref.org"
    
    def __init__(
        self,
        email: Optional[str] = None,
    ) -> None:
        """Initialize the CrossRef client.
        
        Args:
            email: Your email for the polite pool (faster rate limits).
        """
        self.email = email
        self._session = requests.Session()
        
        headers = {"User-Agent": "ResearchTrends/1.0"}
        if email:
            headers["User-Agent"] = f"ResearchTrends/1.0 (mailto:{email})"
        self._session.headers.update(headers)
        
        self._last_request_time = 0.0
        # CrossRef: ~50 req/sec for polite pool
        self._min_interval = 0.02 if email else 0.1
    
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
        """Make a request to the CrossRef API.
        
        Args:
            endpoint: API endpoint.
            params: Query parameters.
            
        Returns:
            JSON response data.
        """
        self._rate_limit()
        
        url = f"{self.BASE_URL}/{endpoint}"
        params = params or {}
        
        try:
            response = self._session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("message", data)
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if e.response else None
            raise CrossRefError(f"HTTP error: {e}", status_code)
        except requests.exceptions.RequestException as e:
            raise CrossRefError(f"Request failed: {e}")
    
    def _parse_work(self, work: Dict[str, Any]) -> Publication:
        """Parse a CrossRef work into a Publication.
        
        Args:
            work: CrossRef work data.
            
        Returns:
            Publication object.
        """
        # Extract title
        title = ""
        if work.get("title"):
            title = work["title"][0] if isinstance(work["title"], list) else work["title"]
        
        # Extract authors
        authors = []
        affiliations = set()
        for author in work.get("author", []):
            name_parts = []
            if author.get("given"):
                name_parts.append(author["given"])
            if author.get("family"):
                name_parts.append(author["family"])
            if name_parts:
                authors.append(" ".join(name_parts))
            for affil in author.get("affiliation", []):
                if affil.get("name"):
                    affiliations.add(affil["name"])
        
        # Extract publication date
        pub_date = None
        pub_year = None
        
        date_parts = None
        for date_field in ["published-print", "published-online", "created"]:
            if work.get(date_field, {}).get("date-parts"):
                date_parts = work[date_field]["date-parts"][0]
                break
        
        if date_parts:
            pub_year = date_parts[0] if len(date_parts) > 0 else None
            if len(date_parts) >= 3:
                try:
                    pub_date = datetime(date_parts[0], date_parts[1], date_parts[2])
                except (ValueError, TypeError):
                    pass
        
        # Extract keywords/subjects
        keywords = [s.lower() for s in work.get("subject", [])]
        
        # Extract ISSN
        issn = ""
        if work.get("ISSN"):
            issn = work["ISSN"][0] if isinstance(work["ISSN"], list) else work["ISSN"]
        
        # Extract container (journal) title
        container_title = ""
        if work.get("container-title"):
            container_title = work["container-title"][0] if isinstance(work["container-title"], list) else work["container-title"]
        
        return Publication(
            scopus_id=work.get("DOI", ""),
            eid=work.get("DOI", ""),
            doi=work.get("DOI", ""),
            title=title,
            abstract=work.get("abstract", "") or "",
            authors=authors,
            affiliations=list(affiliations),
            keywords=keywords,
            publication_name=container_title,
            issn=issn,
            volume=work.get("volume", "") or "",
            issue=work.get("issue", "") or "",
            pages=work.get("page", "") or "",
            publication_date=pub_date,
            publication_year=pub_year,
            citation_count=work.get("is-referenced-by-count", 0) or 0,
            document_type=work.get("type", "") or "",
            open_access=False,  # CrossRef doesn't provide this directly
            raw_data=work,
        )
    
    def search(
        self,
        query: str,
        start_year: Optional[int] = None,
        end_year: Optional[int] = None,
        max_results: Optional[int] = None,
        sort: str = "relevance",
        show_progress: bool = True,
        **kwargs: Any,
    ) -> SearchResult:
        """Search for publications in CrossRef.
        
        Args:
            query: Search query.
            start_year: Earliest publication year.
            end_year: Latest publication year.
            max_results: Maximum number of results (default 100).
            sort: Sort order ('relevance', 'published', 'indexed').
            show_progress: Show progress bar.
            **kwargs: Additional filter parameters.
            
        Returns:
            SearchResult containing publications and metadata.
        """
        max_results = max_results or 100
        rows = min(100, max_results)  # CrossRef max is 100 per request
        
        params: Dict[str, Any] = {
            "query": query,
            "rows": rows,
            "sort": sort,
        }
        
        # Date filter
        filters = []
        if start_year:
            filters.append(f"from-pub-date:{start_year}")
        if end_year:
            filters.append(f"until-pub-date:{end_year}")
        
        if filters:
            params["filter"] = ",".join(filters)
        
        publications: List[Publication] = []
        offset = 0
        total_results = 0
        
        progress_bar = None
        if show_progress:
            progress_bar = tqdm(total=max_results, desc="Fetching publications")
        
        try:
            while len(publications) < max_results:
                params["offset"] = offset
                data = self._request("works", params)
                
                total_results = data.get("total-results", 0)
                items = data.get("items", [])
                
                if not items:
                    break
                
                for item in items:
                    if len(publications) >= max_results:
                        break
                    publications.append(self._parse_work(item))
                    if progress_bar:
                        progress_bar.update(1)
                
                offset += len(items)
                if offset >= total_results:
                    break
                    
        finally:
            if progress_bar:
                progress_bar.close()
        
        return SearchResult(
            publications=publications,
            total_results=total_results,
            query=query,
            retrieved_at=datetime.now(),
        )
    
    def get_work(self, doi: str) -> Publication:
        """Get a single work by DOI.
        
        Args:
            doi: Digital Object Identifier.
            
        Returns:
            Publication object.
        """
        # Remove URL prefix if present
        doi = doi.replace("https://doi.org/", "").replace("http://doi.org/", "")
        
        data = self._request(f"works/{doi}")
        return self._parse_work(data)
    
    def get_journal(self, issn: str) -> Dict[str, Any]:
        """Get journal information by ISSN.
        
        Args:
            issn: Journal ISSN.
            
        Returns:
            Journal data dictionary.
        """
        return self._request(f"journals/{issn}")
    
    def get_journal_works(
        self,
        issn: str,
        max_results: int = 100,
    ) -> List[Publication]:
        """Get works from a specific journal.
        
        Args:
            issn: Journal ISSN.
            max_results: Maximum number of works.
            
        Returns:
            List of Publication objects.
        """
        params = {"rows": min(100, max_results)}
        
        publications = []
        offset = 0
        
        while len(publications) < max_results:
            params["offset"] = offset
            data = self._request(f"journals/{issn}/works", params)
            
            items = data.get("items", [])
            if not items:
                break
            
            for item in items:
                if len(publications) >= max_results:
                    break
                publications.append(self._parse_work(item))
            
            offset += len(items)
        
        return publications
    
    def close(self) -> None:
        """Close the session."""
        self._session.close()
    
    def __enter__(self) -> "CrossRefClient":
        return self
    
    def __exit__(self, *args: Any) -> None:
        self.close()
