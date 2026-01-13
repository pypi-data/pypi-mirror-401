"""
Google Scholar scraper for retrieving research publication data.

WARNING: Google Scholar does not have an official API. This scraper
should be used responsibly and sparingly. Excessive use may result
in IP blocking. Consider using OpenAlex or Semantic Scholar instead.

Use at your own risk. This is for educational purposes only.
"""

import random
import re
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import quote_plus, urlencode

import requests
from tqdm import tqdm

from research_trends.models import Publication, SearchResult


class GoogleScholarError(Exception):
    """Exception raised for Google Scholar scraping errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None) -> None:
        super().__init__(message)
        self.status_code = status_code


class GoogleScholarClient:
    """Scraper for Google Scholar.
    
    WARNING: This scraper should be used responsibly. Google Scholar
    does not provide an official API and may block excessive requests.
    
    For production use, consider OpenAlex or Semantic Scholar instead.
    
    Example:
        >>> client = GoogleScholarClient()
        >>> results = client.search("deep learning", max_results=20)
        >>> for pub in results:
        ...     print(pub.title, pub.citation_count)
    """
    
    BASE_URL = "https://scholar.google.com"
    
    # User agents to rotate
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    ]
    
    def __init__(
        self,
        proxy: Optional[str] = None,
        min_delay: float = 5.0,
        max_delay: float = 15.0,
    ) -> None:
        """Initialize the Google Scholar scraper.
        
        Args:
            proxy: Optional proxy URL (e.g., 'http://proxy:8080').
            min_delay: Minimum delay between requests in seconds.
            max_delay: Maximum delay between requests in seconds.
        """
        self.proxy = proxy
        self.min_delay = min_delay
        self.max_delay = max_delay
        
        self._session = requests.Session()
        if proxy:
            self._session.proxies = {
                "http": proxy,
                "https": proxy,
            }
        
        self._last_request_time = 0.0
        self._request_count = 0
    
    def _get_headers(self) -> Dict[str, str]:
        """Get randomized headers."""
        return {
            "User-Agent": random.choice(self.USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
    
    def _rate_limit(self) -> None:
        """Apply randomized rate limiting."""
        elapsed = time.time() - self._last_request_time
        delay = random.uniform(self.min_delay, self.max_delay)
        
        if elapsed < delay:
            time.sleep(delay - elapsed)
        
        self._last_request_time = time.time()
        self._request_count += 1
        
        # Extra delay every few requests
        if self._request_count % 5 == 0:
            time.sleep(random.uniform(2, 5))
    
    def _request(self, url: str, params: Optional[Dict[str, Any]] = None) -> str:
        """Make a request to Google Scholar.
        
        Args:
            url: Request URL.
            params: Query parameters.
            
        Returns:
            HTML response.
        """
        self._rate_limit()
        
        try:
            response = self._session.get(
                url,
                params=params,
                headers=self._get_headers(),
                timeout=30,
            )
            
            # Check for CAPTCHA or blocking
            if response.status_code == 429:
                raise GoogleScholarError(
                    "Rate limited by Google Scholar. Wait and try again later.",
                    429
                )
            
            if "captcha" in response.text.lower() or "unusual traffic" in response.text.lower():
                raise GoogleScholarError(
                    "CAPTCHA detected. Google Scholar has blocked this request.",
                    403
                )
            
            response.raise_for_status()
            return response.text
            
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if e.response else None
            raise GoogleScholarError(f"HTTP error: {e}", status_code)
        except requests.exceptions.RequestException as e:
            raise GoogleScholarError(f"Request failed: {e}")
    
    def _parse_result(self, html_block: str) -> Optional[Publication]:
        """Parse a single search result from HTML.
        
        Args:
            html_block: HTML block for one result.
            
        Returns:
            Publication object or None if parsing fails.
        """
        try:
            # Extract title and link
            title_match = re.search(
                r'<h3[^>]*class="gs_rt"[^>]*>.*?<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>',
                html_block,
                re.DOTALL
            )
            
            if not title_match:
                # Try without link (some results don't have links)
                title_match = re.search(
                    r'<h3[^>]*class="gs_rt"[^>]*>(.*?)</h3>',
                    html_block,
                    re.DOTALL
                )
                if title_match:
                    title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
                    url = ""
                else:
                    return None
            else:
                url = title_match.group(1)
                title = re.sub(r'<[^>]+>', '', title_match.group(2)).strip()
            
            # Clean title
            title = re.sub(r'\s+', ' ', title).strip()
            title = title.replace('[PDF]', '').replace('[HTML]', '').strip()
            
            # Extract authors and publication info
            meta_match = re.search(
                r'<div[^>]*class="gs_a"[^>]*>(.*?)</div>',
                html_block,
                re.DOTALL
            )
            
            authors = []
            publication_name = ""
            pub_year = None
            
            if meta_match:
                meta_text = re.sub(r'<[^>]+>', '', meta_match.group(1))
                meta_text = re.sub(r'\s+', ' ', meta_text).strip()
                
                # Parse: "Author1, Author2 - Journal, Year - Publisher"
                parts = meta_text.split(' - ')
                if parts:
                    author_text = parts[0].strip()
                    authors = [a.strip() for a in author_text.split(',') if a.strip() and '…' not in a]
                
                if len(parts) > 1:
                    journal_year = parts[1].strip()
                    # Extract year
                    year_match = re.search(r'\b(19|20)\d{2}\b', journal_year)
                    if year_match:
                        pub_year = int(year_match.group(0))
                    # Extract journal (everything before the year)
                    if year_match:
                        publication_name = journal_year[:year_match.start()].strip().rstrip(',')
                    else:
                        publication_name = journal_year
            
            # Extract abstract/snippet
            abstract_match = re.search(
                r'<div[^>]*class="gs_rs"[^>]*>(.*?)</div>',
                html_block,
                re.DOTALL
            )
            abstract = ""
            if abstract_match:
                abstract = re.sub(r'<[^>]+>', '', abstract_match.group(1))
                abstract = re.sub(r'\s+', ' ', abstract).strip()
            
            # Extract citation count
            citation_count = 0
            cite_match = re.search(r'Cited by (\d+)', html_block)
            if cite_match:
                citation_count = int(cite_match.group(1))
            
            # Extract DOI if present
            doi = ""
            doi_match = re.search(r'10\.\d{4,}/[^\s<"]+', html_block)
            if doi_match:
                doi = doi_match.group(0)
            
            # Generate a pseudo-ID from title
            pseudo_id = re.sub(r'[^a-z0-9]', '', title.lower())[:50]
            
            return Publication(
                scopus_id=f"gs_{pseudo_id}",
                eid=url,
                doi=doi,
                title=title,
                abstract=abstract,
                authors=authors,
                affiliations=[],
                keywords=[],
                publication_name=publication_name,
                issn="",
                publication_date=datetime(pub_year, 1, 1) if pub_year else None,
                publication_year=pub_year,
                citation_count=citation_count,
                document_type="",
                open_access=False,
                raw_data={"url": url, "source": "google_scholar"},
            )
            
        except Exception:
            return None
    
    def search(
        self,
        query: str,
        start_year: Optional[int] = None,
        end_year: Optional[int] = None,
        max_results: Optional[int] = None,
        sort_by_date: bool = False,
        show_progress: bool = True,
        **kwargs: Any,
    ) -> SearchResult:
        """Search for publications in Google Scholar.
        
        Args:
            query: Search query.
            start_year: Earliest publication year.
            end_year: Latest publication year.
            max_results: Maximum number of results (default 20, max recommended 100).
            sort_by_date: Sort by date instead of relevance.
            show_progress: Show progress bar.
            **kwargs: Additional parameters (ignored).
            
        Returns:
            SearchResult containing publications and metadata.
            
        Warning:
            Use sparingly to avoid being blocked by Google.
        """
        max_results = min(max_results or 20, 100)  # Cap at 100 to avoid blocking
        
        params: Dict[str, Any] = {
            "q": query,
            "hl": "en",
        }
        
        if start_year:
            params["as_ylo"] = start_year
        if end_year:
            params["as_yhi"] = end_year
        if sort_by_date:
            params["scisbd"] = 1
        
        publications: List[Publication] = []
        start = 0
        total_results = 0
        
        progress_bar = None
        if show_progress:
            progress_bar = tqdm(total=max_results, desc="Fetching publications")
        
        try:
            while len(publications) < max_results:
                params["start"] = start
                
                html = self._request(f"{self.BASE_URL}/scholar", params)
                
                # Extract total results count (approximate)
                if total_results == 0:
                    count_match = re.search(r'About ([\d,]+) results', html)
                    if count_match:
                        total_results = int(count_match.group(1).replace(',', ''))
                
                # Extract individual results
                # Each result is in a div with class "gs_r gs_or gs_scl"
                result_blocks = re.findall(
                    r'<div[^>]*class="gs_r gs_or gs_scl"[^>]*>(.*?)</div>\s*</div>\s*</div>',
                    html,
                    re.DOTALL
                )
                
                if not result_blocks:
                    # Try alternative pattern
                    result_blocks = re.findall(
                        r'<div[^>]*data-cid="[^"]*"[^>]*>(.*?)<div class="gs_fl',
                        html,
                        re.DOTALL
                    )
                
                if not result_blocks:
                    break
                
                found_new = False
                for block in result_blocks:
                    if len(publications) >= max_results:
                        break
                    
                    pub = self._parse_result(block)
                    if pub:
                        publications.append(pub)
                        found_new = True
                        if progress_bar:
                            progress_bar.update(1)
                
                if not found_new:
                    break
                
                start += 10  # Google Scholar shows 10 results per page
                
        finally:
            if progress_bar:
                progress_bar.close()
        
        return SearchResult(
            publications=publications,
            total_results=total_results or len(publications),
            query=query,
            retrieved_at=datetime.now(),
        )
    
    def get_author_publications(
        self,
        author_id: str,
        max_results: int = 20,
    ) -> List[Publication]:
        """Get publications by a Google Scholar author.
        
        Args:
            author_id: Google Scholar author ID (from URL).
            max_results: Maximum number of publications.
            
        Returns:
            List of Publication objects.
        """
        params = {
            "user": author_id,
            "hl": "en",
            "cstart": 0,
            "pagesize": min(100, max_results),
        }
        
        html = self._request(f"{self.BASE_URL}/citations", params)
        
        # Parse author's publications
        publications = []
        
        # Find publication entries
        pub_matches = re.findall(
            r'<tr[^>]*class="gsc_a_tr"[^>]*>(.*?)</tr>',
            html,
            re.DOTALL
        )
        
        for match in pub_matches[:max_results]:
            # Extract title
            title_match = re.search(r'<a[^>]*class="gsc_a_at"[^>]*>(.*?)</a>', match)
            if not title_match:
                continue
            title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
            
            # Extract citation count
            cite_match = re.search(r'<a[^>]*class="gsc_a_ac[^"]*"[^>]*>(\d+)</a>', match)
            citation_count = int(cite_match.group(1)) if cite_match else 0
            
            # Extract year
            year_match = re.search(r'<span[^>]*class="gsc_a_h[^"]*"[^>]*>(\d{4})</span>', match)
            pub_year = int(year_match.group(1)) if year_match else None
            
            pseudo_id = re.sub(r'[^a-z0-9]', '', title.lower())[:50]
            
            publications.append(Publication(
                scopus_id=f"gs_{pseudo_id}",
                title=title,
                publication_year=pub_year,
                citation_count=citation_count,
                raw_data={"source": "google_scholar_author"},
            ))
        
        return publications
    
    def get_citation_count(self, title: str) -> int:
        """Get citation count for a paper by title.
        
        Args:
            title: Paper title.
            
        Returns:
            Citation count.
        """
        result = self.search(f'"{title}"', max_results=1, show_progress=False)
        
        if result.publications:
            return result.publications[0].citation_count
        return 0
    
    def close(self) -> None:
        """Close the session."""
        self._session.close()
    
    def __enter__(self) -> "GoogleScholarClient":
        return self
    
    def __exit__(self, *args: Any) -> None:
        self.close()
