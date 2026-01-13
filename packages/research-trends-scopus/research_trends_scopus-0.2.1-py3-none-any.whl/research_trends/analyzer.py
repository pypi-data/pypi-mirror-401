"""
Trend analysis module for Research Trends.

Provides comprehensive analysis of publication trends including:
- Temporal trends
- Author productivity
- Institutional output
- Keyword/topic analysis
- Citation patterns
- Network analysis
"""

from collections import Counter, defaultdict
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

from research_trends.models import (
    Publication,
    SearchResult,
    TrendData,
    Network,
    NetworkNode,
    NetworkEdge,
)


class TrendAnalyzer:
    """Analyzer for research publication trends.
    
    Provides methods to analyze various aspects of research publications
    including temporal trends, author productivity, collaboration patterns,
    and topic evolution.
    
    Example:
        >>> analyzer = TrendAnalyzer(search_result)
        >>> trends = analyzer.analyze()
        >>> top_authors = analyzer.get_top_authors(n=10)
    """
    
    def __init__(
        self,
        data: SearchResult | List[Publication] | pd.DataFrame,
    ) -> None:
        """Initialize the analyzer with publication data.
        
        Args:
            data: Publication data as SearchResult, list of Publications,
                or pandas DataFrame.
        """
        if isinstance(data, SearchResult):
            self.publications = data.publications
        elif isinstance(data, pd.DataFrame):
            self.publications = self._from_dataframe(data)
        else:
            self.publications = data
        
        self._df: Optional[pd.DataFrame] = None
        self._trend_data: Optional[TrendData] = None
        self._coauthorship_network: Optional[Network] = None
    
    def _from_dataframe(self, df: pd.DataFrame) -> List[Publication]:
        """Convert DataFrame to list of Publications.
        
        Args:
            df: DataFrame with publication data.
            
        Returns:
            List of Publication objects.
        """
        publications = []
        for _, row in df.iterrows():
            publications.append(Publication.from_dict(row.to_dict()))
        return publications
    
    @property
    def df(self) -> pd.DataFrame:
        """Get publications as a pandas DataFrame.
        
        Returns:
            DataFrame with publication data.
        """
        if self._df is None:
            self._df = pd.DataFrame([p.to_dict() for p in self.publications])
        return self._df
    
    def analyze(self) -> TrendData:
        """Perform comprehensive trend analysis.
        
        Returns:
            TrendData object with analysis results.
        """
        if self._trend_data is not None:
            return self._trend_data
        
        self._trend_data = TrendData(
            yearly_counts=self._compute_yearly_counts(),
            author_counts=self._compute_author_counts(),
            affiliation_counts=self._compute_affiliation_counts(),
            keyword_counts=self._compute_keyword_counts(),
            journal_counts=self._compute_journal_counts(),
            citation_stats=self._compute_citation_stats(),
            document_type_counts=self._compute_document_type_counts(),
            subject_area_counts=self._compute_subject_area_counts(),
            open_access_ratio=self._compute_open_access_ratio(),
            yearly_citations=self._compute_yearly_citations(),
            yearly_open_access=self._compute_yearly_open_access(),
        )
        
        return self._trend_data
    
    def _compute_yearly_counts(self) -> Dict[int, int]:
        """Compute publication counts by year."""
        years = [p.publication_year for p in self.publications if p.publication_year]
        return dict(Counter(years))
    
    def _compute_author_counts(self) -> Dict[str, int]:
        """Compute publication counts by author."""
        authors = []
        for p in self.publications:
            authors.extend(p.authors)
        return dict(Counter(authors))
    
    def _compute_affiliation_counts(self) -> Dict[str, int]:
        """Compute publication counts by affiliation."""
        affiliations = []
        for p in self.publications:
            affiliations.extend(p.affiliations)
        return dict(Counter(affiliations))
    
    def _compute_keyword_counts(self) -> Dict[str, int]:
        """Compute keyword frequencies."""
        keywords = []
        for p in self.publications:
            keywords.extend([kw.lower().strip() for kw in p.keywords])
        return dict(Counter(keywords))
    
    def _compute_journal_counts(self) -> Dict[str, int]:
        """Compute publication counts by journal."""
        journals = [p.publication_name for p in self.publications if p.publication_name]
        return dict(Counter(journals))
    
    def _compute_citation_stats(self) -> Dict[str, Any]:
        """Compute citation statistics."""
        citations = [p.citation_count for p in self.publications]
        
        if not citations:
            return {
                "total": 0,
                "mean": 0,
                "median": 0,
                "max": 0,
                "min": 0,
                "std": 0,
            }
        
        return {
            "total": sum(citations),
            "mean": np.mean(citations),
            "median": np.median(citations),
            "max": max(citations),
            "min": min(citations),
            "std": np.std(citations),
        }
    
    def _compute_document_type_counts(self) -> Dict[str, int]:
        """Compute counts by document type."""
        doc_types = [p.document_type for p in self.publications if p.document_type]
        return dict(Counter(doc_types))
    
    def _compute_subject_area_counts(self) -> Dict[str, int]:
        """Compute counts by subject area."""
        areas = []
        for p in self.publications:
            areas.extend(p.subject_areas)
        return dict(Counter(areas))
    
    def _compute_open_access_ratio(self) -> float:
        """Compute ratio of open access publications."""
        if not self.publications:
            return 0.0
        oa_count = sum(1 for p in self.publications if p.open_access)
        return oa_count / len(self.publications)
    
    def _compute_yearly_citations(self) -> Dict[int, int]:
        """Compute total citations by publication year."""
        yearly_cites: Dict[int, int] = defaultdict(int)
        for p in self.publications:
            if p.publication_year:
                yearly_cites[p.publication_year] += p.citation_count
        return dict(yearly_cites)
    
    def _compute_yearly_open_access(self) -> Dict[int, float]:
        """Compute open access ratio by year."""
        yearly_total: Dict[int, int] = defaultdict(int)
        yearly_oa: Dict[int, int] = defaultdict(int)
        
        for p in self.publications:
            if p.publication_year:
                yearly_total[p.publication_year] += 1
                if p.open_access:
                    yearly_oa[p.publication_year] += 1
        
        return {
            year: yearly_oa[year] / total
            for year, total in yearly_total.items()
        }
    
    def get_top_authors(self, n: int = 10) -> List[Tuple[str, int]]:
        """Get top authors by publication count.
        
        Args:
            n: Number of top authors to return.
            
        Returns:
            List of (author_name, count) tuples.
        """
        trends = self.analyze()
        sorted_authors = sorted(
            trends.author_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_authors[:n]
    
    def get_top_keywords(self, n: int = 20) -> List[Tuple[str, int]]:
        """Get top keywords by frequency.
        
        Args:
            n: Number of top keywords to return.
            
        Returns:
            List of (keyword, count) tuples.
        """
        trends = self.analyze()
        sorted_keywords = sorted(
            trends.keyword_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_keywords[:n]
    
    def get_top_affiliations(self, n: int = 10) -> List[Tuple[str, int]]:
        """Get top affiliations by publication count.
        
        Args:
            n: Number of top affiliations to return.
            
        Returns:
            List of (affiliation, count) tuples.
        """
        trends = self.analyze()
        sorted_affiliations = sorted(
            trends.affiliation_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_affiliations[:n]
    
    def get_top_journals(self, n: int = 10) -> List[Tuple[str, int]]:
        """Get top journals by publication count.
        
        Args:
            n: Number of top journals to return.
            
        Returns:
            List of (journal, count) tuples.
        """
        trends = self.analyze()
        sorted_journals = sorted(
            trends.journal_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_journals[:n]
    
    def get_most_cited(self, n: int = 10) -> List[Publication]:
        """Get most cited publications.
        
        Args:
            n: Number of publications to return.
            
        Returns:
            List of most cited Publication objects.
        """
        sorted_pubs = sorted(
            self.publications,
            key=lambda x: x.citation_count,
            reverse=True
        )
        return sorted_pubs[:n]
    
    def get_growth_rate(self) -> Dict[int, float]:
        """Calculate year-over-year growth rate.
        
        Returns:
            Dictionary mapping years to growth rates.
        """
        trends = self.analyze()
        yearly = trends.yearly_counts
        
        sorted_years = sorted(yearly.keys())
        growth_rates = {}
        
        for i, year in enumerate(sorted_years[1:], 1):
            prev_year = sorted_years[i - 1]
            prev_count = yearly[prev_year]
            curr_count = yearly[year]
            
            if prev_count > 0:
                growth_rates[year] = (curr_count - prev_count) / prev_count * 100
            else:
                growth_rates[year] = 0.0
        
        return growth_rates
    
    def get_keyword_trends(self) -> pd.DataFrame:
        """Get keyword frequency trends over time.
        
        Returns:
            DataFrame with years as index and keywords as columns.
        """
        keyword_by_year: Dict[int, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        
        for p in self.publications:
            if p.publication_year:
                for kw in p.keywords:
                    keyword_by_year[p.publication_year][kw.lower().strip()] += 1
        
        df = pd.DataFrame(keyword_by_year).T.fillna(0).astype(int)
        df.index.name = "year"
        return df.sort_index()
    
    def get_coauthorship_network(self) -> Network:
        """Build co-authorship network.
        
        Returns:
            Network object representing co-authorships.
        """
        if self._coauthorship_network is not None:
            return self._coauthorship_network
        
        # Count co-authorships
        coauthorships: Dict[Tuple[str, str], int] = defaultdict(int)
        author_counts: Dict[str, int] = defaultdict(int)
        
        for p in self.publications:
            authors = p.authors
            for author in authors:
                author_counts[author] += 1
            
            # Create pairs
            for i, author1 in enumerate(authors):
                for author2 in authors[i + 1:]:
                    pair = tuple(sorted([author1, author2]))
                    coauthorships[pair] += 1
        
        # Build network
        nodes = [
            NetworkNode(
                id=author,
                label=author,
                type="author",
                weight=count,
            )
            for author, count in author_counts.items()
        ]
        
        edges = [
            NetworkEdge(
                source=pair[0],
                target=pair[1],
                weight=count,
            )
            for pair, count in coauthorships.items()
        ]
        
        self._coauthorship_network = Network(
            nodes=nodes,
            edges=edges,
            type="coauthorship",
        )
        
        return self._coauthorship_network
    
    def get_networkx_graph(self) -> nx.Graph:
        """Get co-authorship network as NetworkX graph.
        
        Returns:
            NetworkX Graph object.
        """
        network = self.get_coauthorship_network()
        
        G = nx.Graph()
        
        for node in network.nodes:
            G.add_node(node.id, label=node.label, weight=node.weight)
        
        for edge in network.edges:
            G.add_edge(edge.source, edge.target, weight=edge.weight)
        
        return G
    
    def cluster_topics(self, n_clusters: int = 5) -> Dict[int, List[str]]:
        """Cluster publications into topics using TF-IDF and K-means.
        
        Args:
            n_clusters: Number of topic clusters.
            
        Returns:
            Dictionary mapping cluster IDs to representative keywords.
        """
        # Combine title and abstract for each publication
        texts = []
        for p in self.publications:
            text = f"{p.title} {p.abstract} {' '.join(p.keywords)}"
            texts.append(text)
        
        if len(texts) < n_clusters:
            return {}
        
        # TF-IDF vectorization
        vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2),
        )
        
        tfidf_matrix = vectorizer.fit_transform(texts)
        
        # K-means clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(tfidf_matrix)
        
        # Get top terms for each cluster
        feature_names = vectorizer.get_feature_names_out()
        cluster_terms: Dict[int, List[str]] = {}
        
        for i in range(n_clusters):
            center = kmeans.cluster_centers_[i]
            top_indices = center.argsort()[-10:][::-1]
            cluster_terms[i] = [feature_names[idx] for idx in top_indices]
        
        return cluster_terms
    
    def get_emerging_keywords(
        self,
        recent_years: int = 2,
        min_count: int = 3,
    ) -> List[Tuple[str, float]]:
        """Identify emerging keywords based on recent growth.
        
        Args:
            recent_years: Number of recent years to consider.
            min_count: Minimum keyword count to consider.
            
        Returns:
            List of (keyword, growth_score) tuples sorted by growth.
        """
        keyword_df = self.get_keyword_trends()
        
        if keyword_df.empty:
            return []
        
        years = sorted(keyword_df.index)
        if len(years) < 2:
            return []
        
        recent = years[-recent_years:] if len(years) >= recent_years else years
        older = years[:-recent_years] if len(years) > recent_years else []
        
        emerging = []
        
        for keyword in keyword_df.columns:
            recent_count = keyword_df.loc[recent, keyword].sum()
            older_count = keyword_df.loc[older, keyword].sum() if older else 0
            
            if recent_count >= min_count:
                if older_count == 0:
                    growth = float(recent_count)
                else:
                    growth = (recent_count - older_count) / older_count
                
                if growth > 0:
                    emerging.append((keyword, growth))
        
        return sorted(emerging, key=lambda x: x[1], reverse=True)
    
    def to_dataframe(self) -> pd.DataFrame:
        """Export publications to DataFrame.
        
        Returns:
            DataFrame with publication data.
        """
        return self.df.copy()
    
    def summary(self) -> Dict[str, Any]:
        """Get a summary of the analysis.
        
        Returns:
            Dictionary with summary statistics.
        """
        trends = self.analyze()
        
        return {
            "total_publications": len(self.publications),
            "year_range": (
                min(trends.yearly_counts.keys()) if trends.yearly_counts else None,
                max(trends.yearly_counts.keys()) if trends.yearly_counts else None,
            ),
            "unique_authors": len(trends.author_counts),
            "unique_affiliations": len(trends.affiliation_counts),
            "unique_keywords": len(trends.keyword_counts),
            "unique_journals": len(trends.journal_counts),
            "citation_stats": trends.citation_stats,
            "open_access_ratio": trends.open_access_ratio,
            "document_types": trends.document_type_counts,
        }
