"""
Tests for the TrendAnalyzer.
"""

import pytest
from datetime import datetime
from unittest.mock import Mock

from research_trends.analyzer import TrendAnalyzer
from research_trends.models import Publication, SearchResult


class TestTrendAnalyzer:
    """Tests for the TrendAnalyzer class."""
    
    @pytest.fixture
    def sample_publications(self):
        """Create sample publications for testing."""
        return [
            Publication(
                scopus_id="1",
                title="Machine Learning in Healthcare",
                authors=["Smith, J.", "Doe, J."],
                affiliations=["MIT", "Stanford"],
                keywords=["machine learning", "healthcare", "AI"],
                publication_year=2022,
                citation_count=100,
                open_access=True,
                document_type="Article",
                publication_name="Nature",
            ),
            Publication(
                scopus_id="2",
                title="Deep Learning Applications",
                authors=["Smith, J.", "Brown, A."],
                affiliations=["MIT", "Harvard"],
                keywords=["deep learning", "neural networks", "AI"],
                publication_year=2022,
                citation_count=50,
                open_access=False,
                document_type="Article",
                publication_name="Science",
            ),
            Publication(
                scopus_id="3",
                title="AI in Medicine",
                authors=["Johnson, M."],
                affiliations=["Stanford"],
                keywords=["AI", "medicine", "healthcare"],
                publication_year=2023,
                citation_count=25,
                open_access=True,
                document_type="Conference Paper",
                publication_name="AI Conference",
            ),
        ]
    
    @pytest.fixture
    def analyzer(self, sample_publications):
        """Create analyzer with sample data."""
        return TrendAnalyzer(sample_publications)
    
    def test_init_with_list(self, sample_publications):
        """Test initialization with list of publications."""
        analyzer = TrendAnalyzer(sample_publications)
        assert len(analyzer.publications) == 3
    
    def test_init_with_search_result(self, sample_publications):
        """Test initialization with SearchResult."""
        result = SearchResult(
            publications=sample_publications,
            total_results=3,
            query="test",
            retrieved_at=datetime.now(),
        )
        analyzer = TrendAnalyzer(result)
        assert len(analyzer.publications) == 3
    
    def test_analyze(self, analyzer):
        """Test comprehensive analysis."""
        trends = analyzer.analyze()
        
        assert trends.yearly_counts == {2022: 2, 2023: 1}
        assert "Smith, J." in trends.author_counts
        assert trends.author_counts["Smith, J."] == 2
        assert "AI" in trends.keyword_counts
    
    def test_get_top_authors(self, analyzer):
        """Test getting top authors."""
        top = analyzer.get_top_authors(n=2)
        
        assert len(top) == 2
        assert top[0][0] == "Smith, J."
        assert top[0][1] == 2
    
    def test_get_top_keywords(self, analyzer):
        """Test getting top keywords."""
        top = analyzer.get_top_keywords(n=3)
        
        assert len(top) == 3
        keywords = [kw for kw, _ in top]
        assert "ai" in keywords
    
    def test_get_top_affiliations(self, analyzer):
        """Test getting top affiliations."""
        top = analyzer.get_top_affiliations(n=3)
        
        affiliations = [a for a, _ in top]
        assert "MIT" in affiliations
        assert "Stanford" in affiliations
    
    def test_get_most_cited(self, analyzer):
        """Test getting most cited publications."""
        most_cited = analyzer.get_most_cited(n=2)
        
        assert len(most_cited) == 2
        assert most_cited[0].citation_count == 100
        assert most_cited[1].citation_count == 50
    
    def test_get_growth_rate(self, analyzer):
        """Test calculating growth rate."""
        growth = analyzer.get_growth_rate()
        
        assert 2023 in growth
        assert growth[2023] == -50.0  # 1 vs 2 = -50%
    
    def test_open_access_ratio(self, analyzer):
        """Test open access ratio calculation."""
        trends = analyzer.analyze()
        
        # 2 out of 3 are open access
        assert abs(trends.open_access_ratio - 2/3) < 0.001
    
    def test_citation_stats(self, analyzer):
        """Test citation statistics."""
        trends = analyzer.analyze()
        
        assert trends.citation_stats["total"] == 175
        assert trends.citation_stats["max"] == 100
        assert trends.citation_stats["min"] == 25
    
    def test_document_type_counts(self, analyzer):
        """Test document type counting."""
        trends = analyzer.analyze()
        
        assert trends.document_type_counts["Article"] == 2
        assert trends.document_type_counts["Conference Paper"] == 1
    
    def test_to_dataframe(self, analyzer):
        """Test exporting to DataFrame."""
        df = analyzer.to_dataframe()
        
        assert len(df) == 3
        assert "title" in df.columns
        assert "authors" in df.columns
    
    def test_summary(self, analyzer):
        """Test summary generation."""
        summary = analyzer.summary()
        
        assert summary["total_publications"] == 3
        assert summary["unique_authors"] == 4
        assert summary["year_range"] == (2022, 2023)
    
    def test_coauthorship_network(self, analyzer):
        """Test co-authorship network building."""
        network = analyzer.get_coauthorship_network()
        
        assert len(network.nodes) > 0
        assert len(network.edges) > 0
        
        # Smith collaborated with both Doe and Brown
        author_ids = [n.id for n in network.nodes]
        assert "Smith, J." in author_ids
    
    def test_networkx_graph(self, analyzer):
        """Test NetworkX graph export."""
        G = analyzer.get_networkx_graph()
        
        assert G.number_of_nodes() > 0
        assert G.number_of_edges() > 0
    
    def test_empty_publications(self):
        """Test handling of empty publication list."""
        analyzer = TrendAnalyzer([])
        trends = analyzer.analyze()
        
        assert trends.yearly_counts == {}
        assert trends.open_access_ratio == 0.0
