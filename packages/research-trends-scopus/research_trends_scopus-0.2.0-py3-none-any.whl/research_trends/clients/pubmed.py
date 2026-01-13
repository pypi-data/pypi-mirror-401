"""
PubMed/NCBI API client for retrieving biomedical research publications.

PubMed is a free database of biomedical literature from MEDLINE,
life science journals, and online books. 36M+ citations.

Documentation: https://www.ncbi.nlm.nih.gov/books/NBK25497/
"""

import time
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Any, Dict, List, Optional

import requests
from tqdm import tqdm

from research_trends.models import Publication, SearchResult


class PubMedError(Exception):
    """Exception raised for PubMed API errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None) -> None:
        super().__init__(message)
        self.status_code = status_code


class PubMedClient:
    """Client for interacting with the PubMed/NCBI E-utilities API.
    
    PubMed provides free access to 36M+ biomedical literature citations.
    No API key required, but one is recommended for higher rate limits.
    
    Get an API key at: https://www.ncbi.nlm.nih.gov/account/settings/
    
    Example:
        >>> client = PubMedClient(api_key="your-key")
        >>> results = client.search("cancer treatment", max_results=100)
        >>> for pub in results:
        ...     print(pub.title)
    """
    
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        email: Optional[str] = None,
    ) -> None:
        """Initialize the PubMed client.
        
        Args:
            api_key: NCBI API key (optional but recommended).
            email: Your email (required by NCBI for tracking).
        """
        self.api_key = api_key
        self.email = email
        self._session = requests.Session()
        
        self._last_request_time = 0.0
        # Rate limits: 3 req/sec without key, 10 req/sec with key
        self._min_interval = 0.1 if api_key else 0.34
    
    def _rate_limit(self) -> None:
        """Apply rate limiting."""
        elapsed = time.time() - self._last_request_time
        if elapsed < self._min_interval:
            time.sleep(self._min_interval - elapsed)
        self._last_request_time = time.time()
    
    def _add_auth_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Add authentication parameters."""
        if self.api_key:
            params["api_key"] = self.api_key
        if self.email:
            params["email"] = self.email
        return params
    
    def _request(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        return_xml: bool = False,
    ) -> Any:
        """Make a request to the PubMed API.
        
        Args:
            endpoint: API endpoint.
            params: Query parameters.
            return_xml: Return raw XML instead of JSON.
            
        Returns:
            Response data.
        """
        self._rate_limit()
        
        url = f"{self.BASE_URL}/{endpoint}"
        params = self._add_auth_params(params or {})
        
        if not return_xml:
            params["retmode"] = "json"
        
        try:
            response = self._session.get(url, params=params)
            response.raise_for_status()
            
            if return_xml:
                return response.text
            return response.json()
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if e.response else None
            raise PubMedError(f"HTTP error: {e}", status_code)
        except requests.exceptions.RequestException as e:
            raise PubMedError(f"Request failed: {e}")
    
    def _parse_article(self, article: ET.Element) -> Publication:
        """Parse a PubMed article XML into a Publication.
        
        Args:
            article: PubMed article XML element.
            
        Returns:
            Publication object.
        """
        medline = article.find("MedlineCitation")
        if medline is None:
            medline = article
        
        # Get PMID
        pmid_elem = medline.find("PMID")
        pmid = pmid_elem.text if pmid_elem is not None else ""
        
        # Get article info
        article_elem = medline.find("Article")
        if article_elem is None:
            return Publication(scopus_id=pmid)
        
        # Title
        title_elem = article_elem.find("ArticleTitle")
        title = "".join(title_elem.itertext()) if title_elem is not None else ""
        
        # Abstract
        abstract = ""
        abstract_elem = article_elem.find("Abstract")
        if abstract_elem is not None:
            abstract_texts = []
            for text in abstract_elem.findall("AbstractText"):
                if text.text:
                    label = text.get("Label", "")
                    if label:
                        abstract_texts.append(f"{label}: {text.text}")
                    else:
                        abstract_texts.append(text.text)
            abstract = " ".join(abstract_texts)
        
        # Authors
        authors = []
        affiliations = set()
        author_list = article_elem.find("AuthorList")
        if author_list is not None:
            for author in author_list.findall("Author"):
                name_parts = []
                lastname = author.find("LastName")
                forename = author.find("ForeName")
                if forename is not None and forename.text:
                    name_parts.append(forename.text)
                if lastname is not None and lastname.text:
                    name_parts.append(lastname.text)
                if name_parts:
                    authors.append(" ".join(name_parts))
                
                for affil in author.findall("AffiliationInfo/Affiliation"):
                    if affil.text:
                        affiliations.add(affil.text)
        
        # Journal info
        journal = article_elem.find("Journal")
        journal_title = ""
        issn = ""
        volume = ""
        issue = ""
        pub_date = None
        pub_year = None
        
        if journal is not None:
            title_elem = journal.find("Title")
            if title_elem is not None:
                journal_title = title_elem.text or ""
            
            issn_elem = journal.find("ISSN")
            if issn_elem is not None:
                issn = issn_elem.text or ""
            
            ji = journal.find("JournalIssue")
            if ji is not None:
                vol_elem = ji.find("Volume")
                if vol_elem is not None:
                    volume = vol_elem.text or ""
                issue_elem = ji.find("Issue")
                if issue_elem is not None:
                    issue = issue_elem.text or ""
                
                pub_date_elem = ji.find("PubDate")
                if pub_date_elem is not None:
                    year_elem = pub_date_elem.find("Year")
                    month_elem = pub_date_elem.find("Month")
                    day_elem = pub_date_elem.find("Day")
                    
                    if year_elem is not None and year_elem.text:
                        pub_year = int(year_elem.text)
                        
                        month = 1
                        day = 1
                        if month_elem is not None and month_elem.text:
                            try:
                                month = int(month_elem.text)
                            except ValueError:
                                # Month might be text like "Jan"
                                month_map = {
                                    "jan": 1, "feb": 2, "mar": 3, "apr": 4,
                                    "may": 5, "jun": 6, "jul": 7, "aug": 8,
                                    "sep": 9, "oct": 10, "nov": 11, "dec": 12
                                }
                                month = month_map.get(month_elem.text.lower()[:3], 1)
                        if day_elem is not None and day_elem.text:
                            try:
                                day = int(day_elem.text)
                            except ValueError:
                                pass
                        
                        try:
                            pub_date = datetime(pub_year, month, day)
                        except ValueError:
                            pass
        
        # Pages
        pagination = article_elem.find("Pagination/MedlinePgn")
        pages = pagination.text if pagination is not None else ""
        
        # DOI and other IDs
        doi = ""
        article_ids = article.find("PubmedData/ArticleIdList")
        if article_ids is not None:
            for id_elem in article_ids.findall("ArticleId"):
                if id_elem.get("IdType") == "doi":
                    doi = id_elem.text or ""
                    break
        
        # Keywords (MeSH terms)
        keywords = []
        mesh_list = medline.find("MeshHeadingList")
        if mesh_list is not None:
            for mesh in mesh_list.findall("MeshHeading/DescriptorName"):
                if mesh.text:
                    keywords.append(mesh.text.lower())
        
        # Publication types
        pub_types = []
        pub_type_list = article_elem.find("PublicationTypeList")
        if pub_type_list is not None:
            for pt in pub_type_list.findall("PublicationType"):
                if pt.text:
                    pub_types.append(pt.text)
        
        return Publication(
            scopus_id=pmid,
            eid=f"PMID:{pmid}",
            doi=doi,
            title=title,
            abstract=abstract,
            authors=authors,
            affiliations=list(affiliations),
            keywords=keywords,
            publication_name=journal_title,
            issn=issn,
            volume=volume,
            issue=issue,
            pages=pages,
            publication_date=pub_date,
            publication_year=pub_year,
            citation_count=0,  # PubMed doesn't provide citation counts
            document_type=", ".join(pub_types),
            open_access=False,  # Would need PMC check
            raw_data={},
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
        """Search for publications in PubMed.
        
        Args:
            query: Search query (supports PubMed search syntax).
            start_year: Earliest publication year.
            end_year: Latest publication year.
            max_results: Maximum number of results (default 100).
            sort: Sort order ('relevance', 'pub_date').
            show_progress: Show progress bar.
            **kwargs: Additional search parameters.
            
        Returns:
            SearchResult containing publications and metadata.
        """
        max_results = max_results or 100
        
        # Build date filter
        if start_year or end_year:
            date_range = f"{start_year or 1900}:{end_year or 2100}[dp]"
            query = f"({query}) AND {date_range}"
        
        # First, search to get IDs
        search_params = {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "sort": sort,
            "usehistory": "y",
        }
        
        search_result = self._request("esearch.fcgi", search_params)
        
        esearch = search_result.get("esearchresult", {})
        total_results = int(esearch.get("count", 0))
        id_list = esearch.get("idlist", [])
        web_env = esearch.get("webenv", "")
        query_key = esearch.get("querykey", "")
        
        if not id_list:
            return SearchResult(
                publications=[],
                total_results=0,
                query=query,
                retrieved_at=datetime.now(),
            )
        
        # Fetch full records in batches
        publications: List[Publication] = []
        batch_size = 100
        
        progress_bar = None
        if show_progress:
            progress_bar = tqdm(total=len(id_list), desc="Fetching publications")
        
        try:
            for start in range(0, len(id_list), batch_size):
                fetch_params = {
                    "db": "pubmed",
                    "query_key": query_key,
                    "WebEnv": web_env,
                    "retstart": start,
                    "retmax": min(batch_size, len(id_list) - start),
                    "rettype": "xml",
                }
                
                xml_data = self._request("efetch.fcgi", fetch_params, return_xml=True)
                
                # Parse XML
                root = ET.fromstring(xml_data)
                for article in root.findall(".//PubmedArticle"):
                    pub = self._parse_article(article)
                    publications.append(pub)
                    if progress_bar:
                        progress_bar.update(1)
                        
        finally:
            if progress_bar:
                progress_bar.close()
        
        return SearchResult(
            publications=publications,
            total_results=total_results,
            query=query,
            retrieved_at=datetime.now(),
        )
    
    def get_article(self, pmid: str) -> Publication:
        """Get a single article by PMID.
        
        Args:
            pmid: PubMed ID.
            
        Returns:
            Publication object.
        """
        params = {
            "db": "pubmed",
            "id": pmid,
            "rettype": "xml",
        }
        
        xml_data = self._request("efetch.fcgi", params, return_xml=True)
        root = ET.fromstring(xml_data)
        
        article = root.find(".//PubmedArticle")
        if article is None:
            raise PubMedError(f"Article not found: {pmid}")
        
        return self._parse_article(article)
    
    def get_related_articles(
        self,
        pmid: str,
        max_results: int = 20,
    ) -> List[Publication]:
        """Get articles related to a given PMID.
        
        Args:
            pmid: PubMed ID.
            max_results: Maximum number of results.
            
        Returns:
            List of Publication objects.
        """
        # Get related IDs
        link_params = {
            "dbfrom": "pubmed",
            "db": "pubmed",
            "id": pmid,
            "cmd": "neighbor_score",
        }
        
        link_result = self._request("elink.fcgi", link_params)
        
        # Extract linked PMIDs
        pmids = []
        linksets = link_result.get("linksets", [])
        if linksets:
            for linkset in linksets[0].get("linksetdbs", []):
                if linkset.get("linkname") == "pubmed_pubmed":
                    for link in linkset.get("links", [])[:max_results]:
                        pmids.append(str(link))
        
        if not pmids:
            return []
        
        # Fetch articles
        fetch_params = {
            "db": "pubmed",
            "id": ",".join(pmids),
            "rettype": "xml",
        }
        
        xml_data = self._request("efetch.fcgi", fetch_params, return_xml=True)
        root = ET.fromstring(xml_data)
        
        publications = []
        for article in root.findall(".//PubmedArticle"):
            publications.append(self._parse_article(article))
        
        return publications
    
    def close(self) -> None:
        """Close the session."""
        self._session.close()
    
    def __enter__(self) -> "PubMedClient":
        return self
    
    def __exit__(self, *args: Any) -> None:
        self.close()
