"""
Semantic Scholar API client for retrieving research publication data.

Semantic Scholar is a free, AI-powered research tool with 200M+ papers.
Free API key available at https://www.semanticscholar.org/product/api

Documentation: https://api.semanticscholar.org/api-docs/
"""

import time
from datetime import datetime
from typing import Any, Dict, List, Optional

import requests
from tqdm import tqdm

from research_trends.models import Publication, SearchResult


class SemanticScholarError(Exception):
    """Exception raised for Semantic Scholar API errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None) -> None:
        super().__init__(message)
        self.status_code = status_code


class SemanticScholarClient:
    """Client for interacting with the Semantic Scholar API.
    
    Semantic Scholar provides free access to 200M+ papers with
    AI-powered features like TLDR summaries and citation intent.
    
    Example:
        >>> client = SemanticScholarClient(api_key="your-key")
        >>> results = client.search("transformer models", max_results=100)
        >>> for pub in results:
        ...     print(pub.title)
    """
    
    BASE_URL = "https://api.semanticscholar.org/graph/v1"
    PARTNER_URL = "https://partner.semanticscholar.org/graph/v1"
    
    # Fields to request
    PAPER_FIELDS = [
        "paperId", "externalIds", "title", "abstract", "year",
        "citationCount", "referenceCount", "isOpenAccess",
        "fieldsOfStudy", "authors", "venue", "publicationDate",
        "journal", "publicationTypes",
    ]
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        use_partner_api: bool = False,
    ) -> None:
        """Initialize the Semantic Scholar client.
        
        Args:
            api_key: Semantic Scholar API key (optional but recommended).
            use_partner_api: Whether to use partner API (requires approval).
        """
        self.api_key = api_key
        self.base_url = self.PARTNER_URL if use_partner_api else self.BASE_URL
        
        self._session = requests.Session()
        if api_key:
            self._session.headers.update({"x-api-key": api_key})
        
        self._last_request_time = 0.0
        # Rate limits: 1 req/sec without key, 10 req/sec with key
        self._min_interval = 0.1 if api_key else 1.0
    
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
        method: str = "GET",
    ) -> Dict[str, Any]:
        """Make a request to the Semantic Scholar API.
        
        Args:
            endpoint: API endpoint.
            params: Query parameters.
            method: HTTP method.
            
        Returns:
            JSON response data.
        """
        self._rate_limit()
        
        url = f"{self.base_url}/{endpoint}"
        params = params or {}
        
        try:
            if method == "GET":
                response = self._session.get(url, params=params)
            else:
                response = self._session.post(url, json=params)
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if e.response else None
            if status_code == 429:
                raise SemanticScholarError("Rate limit exceeded. Consider using an API key.", status_code)
            raise SemanticScholarError(f"HTTP error: {e}", status_code)
        except requests.exceptions.RequestException as e:
            raise SemanticScholarError(f"Request failed: {e}")
    
    def _parse_paper(self, paper: Dict[str, Any]) -> Publication:
        """Parse a Semantic Scholar paper into a Publication.
        
        Args:
            paper: Semantic Scholar paper data.
            
        Returns:
            Publication object.
        """
        # Extract authors
        authors = []
        for author in paper.get("authors", []):
            if author.get("name"):
                authors.append(author["name"])
        
        # Extract publication date
        pub_date = None
        pub_year = paper.get("year")
        if paper.get("publicationDate"):
            try:
                pub_date = datetime.strptime(paper["publicationDate"], "%Y-%m-%d")
            except ValueError:
                pass
        
        # Extract keywords from fields of study
        keywords = [f.lower() for f in paper.get("fieldsOfStudy", []) or []]
        
        # Extract external IDs
        external_ids = paper.get("externalIds", {}) or {}
        doi = external_ids.get("DOI", "")
        
        # Extract journal info
        journal = paper.get("journal", {}) or {}
        
        return Publication(
            scopus_id=paper.get("paperId", ""),
            eid=paper.get("paperId", ""),
            doi=doi,
            title=paper.get("title", "") or "",
            abstract=paper.get("abstract", "") or "",
            authors=authors,
            affiliations=[],  # Not available in basic API
            keywords=keywords,
            publication_name=paper.get("venue", "") or journal.get("name", "") or "",
            issn=journal.get("issn", "") or "",
            volume=journal.get("volume", "") or "",
            pages=journal.get("pages", "") or "",
            publication_date=pub_date,
            publication_year=pub_year,
            citation_count=paper.get("citationCount", 0) or 0,
            document_type=", ".join(paper.get("publicationTypes", []) or []),
            open_access=paper.get("isOpenAccess", False),
            raw_data=paper,
        )
    
    def search(
        self,
        query: str,
        start_year: Optional[int] = None,
        end_year: Optional[int] = None,
        max_results: Optional[int] = None,
        fields_of_study: Optional[List[str]] = None,
        show_progress: bool = True,
        **kwargs: Any,
    ) -> SearchResult:
        """Search for publications in Semantic Scholar.
        
        Args:
            query: Search query.
            start_year: Earliest publication year.
            end_year: Latest publication year.
            max_results: Maximum number of results (default 100).
            fields_of_study: Filter by fields (e.g., ['Computer Science']).
            show_progress: Show progress bar.
            **kwargs: Additional parameters.
            
        Returns:
            SearchResult containing publications and metadata.
        """
        max_results = max_results or 100
        limit = min(100, max_results)  # API max is 100 per request
        
        params: Dict[str, Any] = {
            "query": query,
            "limit": limit,
            "fields": ",".join(self.PAPER_FIELDS),
        }
        
        # Year filter
        if start_year or end_year:
            year_filter = ""
            if start_year and end_year:
                year_filter = f"{start_year}-{end_year}"
            elif start_year:
                year_filter = f"{start_year}-"
            elif end_year:
                year_filter = f"-{end_year}"
            params["year"] = year_filter
        
        # Fields of study filter
        if fields_of_study:
            params["fieldsOfStudy"] = ",".join(fields_of_study)
        
        publications: List[Publication] = []
        offset = 0
        total_results = 0
        
        progress_bar = None
        if show_progress:
            progress_bar = tqdm(total=max_results, desc="Fetching publications")
        
        try:
            while len(publications) < max_results:
                params["offset"] = offset
                data = self._request("paper/search", params)
                
                total_results = data.get("total", 0)
                papers = data.get("data", [])
                
                if not papers:
                    break
                
                for paper in papers:
                    if len(publications) >= max_results:
                        break
                    publications.append(self._parse_paper(paper))
                    if progress_bar:
                        progress_bar.update(1)
                
                offset += len(papers)
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
    
    def get_paper(self, paper_id: str) -> Publication:
        """Get a single paper by ID.
        
        Args:
            paper_id: Semantic Scholar paper ID, DOI, or other identifier.
            
        Returns:
            Publication object.
        """
        params = {"fields": ",".join(self.PAPER_FIELDS)}
        data = self._request(f"paper/{paper_id}", params)
        return self._parse_paper(data)
    
    def get_paper_citations(
        self,
        paper_id: str,
        max_results: int = 100,
    ) -> List[Publication]:
        """Get papers that cite a given paper.
        
        Args:
            paper_id: Semantic Scholar paper ID.
            max_results: Maximum number of citations.
            
        Returns:
            List of Publication objects.
        """
        params = {
            "fields": ",".join(self.PAPER_FIELDS),
            "limit": min(100, max_results),
        }
        
        publications = []
        offset = 0
        
        while len(publications) < max_results:
            params["offset"] = offset
            data = self._request(f"paper/{paper_id}/citations", params)
            
            citations = data.get("data", [])
            if not citations:
                break
            
            for citation in citations:
                if len(publications) >= max_results:
                    break
                citing_paper = citation.get("citingPaper", {})
                if citing_paper:
                    publications.append(self._parse_paper(citing_paper))
            
            offset += len(citations)
        
        return publications
    
    def get_paper_references(
        self,
        paper_id: str,
        max_results: int = 100,
    ) -> List[Publication]:
        """Get papers referenced by a given paper.
        
        Args:
            paper_id: Semantic Scholar paper ID.
            max_results: Maximum number of references.
            
        Returns:
            List of Publication objects.
        """
        params = {
            "fields": ",".join(self.PAPER_FIELDS),
            "limit": min(100, max_results),
        }
        
        publications = []
        offset = 0
        
        while len(publications) < max_results:
            params["offset"] = offset
            data = self._request(f"paper/{paper_id}/references", params)
            
            references = data.get("data", [])
            if not references:
                break
            
            for ref in references:
                if len(publications) >= max_results:
                    break
                cited_paper = ref.get("citedPaper", {})
                if cited_paper:
                    publications.append(self._parse_paper(cited_paper))
            
            offset += len(references)
        
        return publications
    
    def get_author(self, author_id: str) -> Dict[str, Any]:
        """Get author information.
        
        Args:
            author_id: Semantic Scholar author ID.
            
        Returns:
            Author data dictionary.
        """
        fields = "authorId,name,affiliations,paperCount,citationCount,hIndex"
        return self._request(f"author/{author_id}", {"fields": fields})
    
    def get_author_papers(
        self,
        author_id: str,
        max_results: int = 100,
    ) -> List[Publication]:
        """Get papers by an author.
        
        Args:
            author_id: Semantic Scholar author ID.
            max_results: Maximum number of papers.
            
        Returns:
            List of Publication objects.
        """
        params = {
            "fields": ",".join(self.PAPER_FIELDS),
            "limit": min(100, max_results),
        }
        
        publications = []
        offset = 0
        
        while len(publications) < max_results:
            params["offset"] = offset
            data = self._request(f"author/{author_id}/papers", params)
            
            papers = data.get("data", [])
            if not papers:
                break
            
            for paper in papers:
                if len(publications) >= max_results:
                    break
                publications.append(self._parse_paper(paper))
            
            offset += len(papers)
        
        return publications
    
    def close(self) -> None:
        """Close the session."""
        self._session.close()
    
    def __enter__(self) -> "SemanticScholarClient":
        return self
    
    def __exit__(self, *args: Any) -> None:
        self.close()
