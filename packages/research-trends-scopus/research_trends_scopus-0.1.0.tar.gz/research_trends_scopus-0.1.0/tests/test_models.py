"""
Tests for data models.
"""

import pytest
from datetime import datetime

from research_trends.models import (
    Publication,
    SearchResult,
    TrendData,
    Recommendation,
    Network,
    NetworkNode,
    NetworkEdge,
)


class TestPublication:
    """Tests for the Publication model."""
    
    def test_creation(self):
        """Test creating a publication."""
        pub = Publication(
            scopus_id="12345",
            title="Test Publication",
            authors=["Author One", "Author Two"],
        )
        
        assert pub.scopus_id == "12345"
        assert pub.title == "Test Publication"
        assert len(pub.authors) == 2
    
    def test_defaults(self):
        """Test default values."""
        pub = Publication(scopus_id="123")
        
        assert pub.title == ""
        assert pub.authors == []
        assert pub.citation_count == 0
        assert pub.open_access is False
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        pub = Publication(
            scopus_id="123",
            title="Test",
            publication_date=datetime(2024, 1, 15),
        )
        
        d = pub.to_dict()
        
        assert d["scopus_id"] == "123"
        assert d["title"] == "Test"
        assert d["publication_date"] == "2024-01-15T00:00:00"
    
    def test_from_dict(self):
        """Test creation from dictionary."""
        d = {
            "scopus_id": "123",
            "title": "Test Publication",
            "authors": ["Author One"],
            "publication_date": "2024-01-15T00:00:00",
            "citation_count": 42,
        }
        
        pub = Publication.from_dict(d)
        
        assert pub.scopus_id == "123"
        assert pub.title == "Test Publication"
        assert pub.citation_count == 42
        assert pub.publication_date == datetime(2024, 1, 15)
    
    def test_roundtrip(self):
        """Test to_dict and from_dict roundtrip."""
        original = Publication(
            scopus_id="123",
            title="Test",
            authors=["A", "B"],
            keywords=["kw1", "kw2"],
            publication_date=datetime(2024, 1, 15),
            citation_count=100,
            open_access=True,
        )
        
        d = original.to_dict()
        restored = Publication.from_dict(d)
        
        assert restored.scopus_id == original.scopus_id
        assert restored.title == original.title
        assert restored.authors == original.authors
        assert restored.citation_count == original.citation_count


class TestSearchResult:
    """Tests for the SearchResult model."""
    
    def test_creation(self):
        """Test creating a search result."""
        pubs = [
            Publication(scopus_id="1"),
            Publication(scopus_id="2"),
        ]
        
        result = SearchResult(
            publications=pubs,
            total_results=100,
            query="test query",
            retrieved_at=datetime.now(),
        )
        
        assert len(result) == 2
        assert result.total_results == 100
        assert result.query == "test query"
    
    def test_iteration(self):
        """Test iterating over search results."""
        pubs = [
            Publication(scopus_id="1"),
            Publication(scopus_id="2"),
        ]
        
        result = SearchResult(
            publications=pubs,
            total_results=2,
            query="test",
            retrieved_at=datetime.now(),
        )
        
        ids = [p.scopus_id for p in result]
        assert ids == ["1", "2"]
    
    def test_to_dict_from_dict(self):
        """Test serialization roundtrip."""
        pubs = [Publication(scopus_id="1", title="Test")]
        original = SearchResult(
            publications=pubs,
            total_results=1,
            query="test",
            retrieved_at=datetime(2024, 1, 15, 12, 0, 0),
        )
        
        d = original.to_dict()
        restored = SearchResult.from_dict(d)
        
        assert len(restored) == 1
        assert restored.total_results == 1
        assert restored.query == "test"


class TestTrendData:
    """Tests for the TrendData model."""
    
    def test_creation(self):
        """Test creating trend data."""
        trends = TrendData(
            yearly_counts={2020: 10, 2021: 20},
            author_counts={"Author A": 5},
        )
        
        assert trends.yearly_counts[2020] == 10
        assert trends.author_counts["Author A"] == 5
    
    def test_defaults(self):
        """Test default values."""
        trends = TrendData()
        
        assert trends.yearly_counts == {}
        assert trends.open_access_ratio == 0.0


class TestRecommendation:
    """Tests for the Recommendation model."""
    
    def test_creation(self):
        """Test creating a recommendation."""
        rec = Recommendation(
            title="Test Recommendation",
            description="A test description",
            category="emerging_topics",
            score=0.85,
            keywords=["kw1", "kw2"],
            rationale="Test rationale",
        )
        
        assert rec.title == "Test Recommendation"
        assert rec.score == 0.85
        assert len(rec.keywords) == 2
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        rec = Recommendation(
            title="Test",
            description="Desc",
            category="venues",
            score=0.5,
        )
        
        d = rec.to_dict()
        
        assert d["title"] == "Test"
        assert d["score"] == 0.5
        assert d["category"] == "venues"


class TestNetwork:
    """Tests for network models."""
    
    def test_network_node(self):
        """Test creating a network node."""
        node = NetworkNode(
            id="author1",
            label="Author One",
            type="author",
            weight=10.0,
        )
        
        assert node.id == "author1"
        assert node.weight == 10.0
    
    def test_network_edge(self):
        """Test creating a network edge."""
        edge = NetworkEdge(
            source="author1",
            target="author2",
            weight=5.0,
        )
        
        assert edge.source == "author1"
        assert edge.target == "author2"
    
    def test_network(self):
        """Test creating a network."""
        nodes = [
            NetworkNode(id="1", label="A", type="author"),
            NetworkNode(id="2", label="B", type="author"),
        ]
        edges = [
            NetworkEdge(source="1", target="2"),
        ]
        
        network = Network(nodes=nodes, edges=edges, type="coauthorship")
        
        assert len(network.nodes) == 2
        assert len(network.edges) == 1
        assert network.type == "coauthorship"
