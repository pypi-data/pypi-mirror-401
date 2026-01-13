"""
Data models for Research Trends.

Defines the data structures used throughout the package.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class Publication:
    """Represents a research publication from Scopus.
    
    Attributes:
        scopus_id: Unique Scopus identifier.
        eid: Electronic identifier.
        doi: Digital Object Identifier.
        title: Publication title.
        abstract: Publication abstract.
        authors: List of author names.
        affiliations: List of affiliated institutions.
        keywords: Author-provided keywords.
        publication_name: Name of journal/conference.
        issn: ISSN of the publication venue.
        volume: Volume number.
        issue: Issue number.
        pages: Page range.
        publication_date: Full publication date.
        publication_year: Year of publication.
        citation_count: Number of citations.
        document_type: Type of document.
        source_type: Type of source (journal, conference, etc.).
        open_access: Whether the publication is open access.
        subject_areas: List of subject area classifications.
        raw_data: Original API response data.
    """
    
    scopus_id: str
    eid: str = ""
    doi: str = ""
    title: str = ""
    abstract: str = ""
    authors: List[str] = field(default_factory=list)
    affiliations: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    publication_name: str = ""
    issn: str = ""
    volume: str = ""
    issue: str = ""
    pages: str = ""
    publication_date: Optional[datetime] = None
    publication_year: Optional[int] = None
    citation_count: int = 0
    document_type: str = ""
    source_type: str = ""
    open_access: bool = False
    subject_areas: List[str] = field(default_factory=list)
    raw_data: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation.
        
        Returns:
            Dictionary with all publication data.
        """
        return {
            "scopus_id": self.scopus_id,
            "eid": self.eid,
            "doi": self.doi,
            "title": self.title,
            "abstract": self.abstract,
            "authors": self.authors,
            "affiliations": self.affiliations,
            "keywords": self.keywords,
            "publication_name": self.publication_name,
            "issn": self.issn,
            "volume": self.volume,
            "issue": self.issue,
            "pages": self.pages,
            "publication_date": self.publication_date.isoformat() if self.publication_date else None,
            "publication_year": self.publication_year,
            "citation_count": self.citation_count,
            "document_type": self.document_type,
            "source_type": self.source_type,
            "open_access": self.open_access,
            "subject_areas": self.subject_areas,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Publication":
        """Create a Publication from a dictionary.
        
        Args:
            data: Dictionary with publication data.
            
        Returns:
            Publication instance.
        """
        pub_date = data.get("publication_date")
        if pub_date and isinstance(pub_date, str):
            pub_date = datetime.fromisoformat(pub_date)
        
        return cls(
            scopus_id=data.get("scopus_id", ""),
            eid=data.get("eid", ""),
            doi=data.get("doi", ""),
            title=data.get("title", ""),
            abstract=data.get("abstract", ""),
            authors=data.get("authors", []),
            affiliations=data.get("affiliations", []),
            keywords=data.get("keywords", []),
            publication_name=data.get("publication_name", ""),
            issn=data.get("issn", ""),
            volume=data.get("volume", ""),
            issue=data.get("issue", ""),
            pages=data.get("pages", ""),
            publication_date=pub_date,
            publication_year=data.get("publication_year"),
            citation_count=data.get("citation_count", 0),
            document_type=data.get("document_type", ""),
            source_type=data.get("source_type", ""),
            open_access=data.get("open_access", False),
            subject_areas=data.get("subject_areas", []),
            raw_data=data.get("raw_data", {}),
        )


@dataclass
class SearchResult:
    """Container for search results.
    
    Attributes:
        publications: List of retrieved publications.
        total_results: Total number of results available.
        query: The search query used.
        retrieved_at: Timestamp of retrieval.
    """
    
    publications: List[Publication]
    total_results: int
    query: str
    retrieved_at: datetime
    
    def __len__(self) -> int:
        """Return number of publications retrieved."""
        return len(self.publications)
    
    def __iter__(self):
        """Iterate over publications."""
        return iter(self.publications)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation.
        
        Returns:
            Dictionary with search result data.
        """
        return {
            "publications": [p.to_dict() for p in self.publications],
            "total_results": self.total_results,
            "query": self.query,
            "retrieved_at": self.retrieved_at.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SearchResult":
        """Create a SearchResult from a dictionary.
        
        Args:
            data: Dictionary with search result data.
            
        Returns:
            SearchResult instance.
        """
        return cls(
            publications=[Publication.from_dict(p) for p in data.get("publications", [])],
            total_results=data.get("total_results", 0),
            query=data.get("query", ""),
            retrieved_at=datetime.fromisoformat(data["retrieved_at"]),
        )


@dataclass
class TrendData:
    """Container for trend analysis data.
    
    Attributes:
        yearly_counts: Publication counts by year.
        author_counts: Publication counts by author.
        affiliation_counts: Publication counts by affiliation.
        keyword_counts: Publication counts by keyword.
        journal_counts: Publication counts by journal.
        citation_stats: Citation statistics.
        document_type_counts: Counts by document type.
        subject_area_counts: Counts by subject area.
    """
    
    yearly_counts: Dict[int, int] = field(default_factory=dict)
    author_counts: Dict[str, int] = field(default_factory=dict)
    affiliation_counts: Dict[str, int] = field(default_factory=dict)
    keyword_counts: Dict[str, int] = field(default_factory=dict)
    journal_counts: Dict[str, int] = field(default_factory=dict)
    citation_stats: Dict[str, Any] = field(default_factory=dict)
    document_type_counts: Dict[str, int] = field(default_factory=dict)
    subject_area_counts: Dict[str, int] = field(default_factory=dict)
    open_access_ratio: float = 0.0
    yearly_citations: Dict[int, int] = field(default_factory=dict)
    yearly_open_access: Dict[int, float] = field(default_factory=dict)


@dataclass
class Recommendation:
    """A research area recommendation.
    
    Attributes:
        title: Short title for the recommendation.
        description: Detailed description.
        category: Type of recommendation (topic, methodology, collaboration).
        score: Relevance/importance score (0-1).
        keywords: Related keywords.
        rationale: Explanation for the recommendation.
    """
    
    title: str
    description: str
    category: str
    score: float
    keywords: List[str] = field(default_factory=list)
    rationale: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "score": self.score,
            "keywords": self.keywords,
            "rationale": self.rationale,
        }


@dataclass
class NetworkNode:
    """A node in a collaboration/citation network.
    
    Attributes:
        id: Unique identifier.
        label: Display label.
        type: Node type (author, affiliation, publication).
        weight: Node weight/size.
        attributes: Additional attributes.
    """
    
    id: str
    label: str
    type: str
    weight: float = 1.0
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass 
class NetworkEdge:
    """An edge in a collaboration/citation network.
    
    Attributes:
        source: Source node ID.
        target: Target node ID.
        weight: Edge weight.
        attributes: Additional attributes.
    """
    
    source: str
    target: str
    weight: float = 1.0
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Network:
    """A collaboration or citation network.
    
    Attributes:
        nodes: List of network nodes.
        edges: List of network edges.
        type: Network type (coauthorship, citation, etc.).
    """
    
    nodes: List[NetworkNode] = field(default_factory=list)
    edges: List[NetworkEdge] = field(default_factory=list)
    type: str = "coauthorship"
