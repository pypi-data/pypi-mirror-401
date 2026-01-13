"""
Tests for the Recommender.
"""

import pytest
from datetime import datetime

from research_trends.analyzer import TrendAnalyzer
from research_trends.recommender import Recommender
from research_trends.models import Publication, SearchResult


class TestRecommender:
    """Tests for the Recommender class."""
    
    @pytest.fixture
    def sample_publications(self):
        """Create sample publications for testing."""
        publications = []
        
        # Create publications with various patterns
        for i in range(10):
            publications.append(Publication(
                scopus_id=str(i),
                title=f"Publication {i}",
                authors=[f"Author{i % 3}", f"Author{(i + 1) % 3}"],
                affiliations=[f"University{i % 2}"],
                keywords=["AI", "machine learning", f"topic{i % 4}"],
                publication_year=2020 + (i % 4),
                citation_count=i * 10,
                open_access=i % 2 == 0,
                document_type="Article",
                publication_name=f"Journal{i % 3}",
            ))
        
        return publications
    
    @pytest.fixture
    def recommender(self, sample_publications):
        """Create recommender with sample data."""
        analyzer = TrendAnalyzer(sample_publications)
        return Recommender(analyzer)
    
    def test_init(self, recommender):
        """Test recommender initialization."""
        assert recommender.analyzer is not None
        assert recommender.trends is not None
    
    def test_get_recommendations(self, recommender):
        """Test getting recommendations."""
        recommendations = recommender.get_recommendations(top_n=3)
        
        assert len(recommendations) > 0
        
        for rec in recommendations:
            assert rec.title is not None
            assert rec.description is not None
            assert 0 <= rec.score <= 1
            assert rec.category in [
                'emerging_topics',
                'research_gaps',
                'collaborations',
                'venues',
            ]
    
    def test_get_recommendations_by_category(self, recommender):
        """Test filtering recommendations by category."""
        recommendations = recommender.get_recommendations(
            top_n=3,
            include_categories=['venues']
        )
        
        categories = [r.category for r in recommendations]
        assert all(c == 'venues' for c in categories)
    
    def test_get_topic_suggestions(self, recommender):
        """Test topic suggestions."""
        suggestions = recommender.get_topic_suggestions(
            current_keywords=["AI"],
            top_n=5
        )
        
        assert isinstance(suggestions, list)
        # Should suggest related topics but not AI itself
        assert "ai" not in [s.lower() for s in suggestions]
    
    def test_explain_recommendation(self, recommender):
        """Test recommendation explanation."""
        recommendations = recommender.get_recommendations(top_n=1)
        
        if recommendations:
            explanation = recommender.explain_recommendation(recommendations[0])
            assert len(explanation) > 0
            assert recommendations[0].rationale in explanation
    
    def test_to_report(self, recommender):
        """Test report generation."""
        report = recommender.to_report()
        
        assert "RESEARCH RECOMMENDATIONS REPORT" in report
        assert len(report) > 100
    
    def test_recommendation_sorting(self, recommender):
        """Test that recommendations are sorted by score."""
        recommendations = recommender.get_recommendations(top_n=10)
        
        if len(recommendations) > 1:
            scores = [r.score for r in recommendations]
            assert scores == sorted(scores, reverse=True)


class TestRecommendationCategories:
    """Test individual recommendation categories."""
    
    @pytest.fixture
    def rich_publications(self):
        """Create a richer dataset for testing."""
        publications = []
        
        # Create diverse publications
        topics = [
            ("AI healthcare", ["AI", "healthcare", "diagnosis"]),
            ("Machine learning", ["machine learning", "algorithms", "optimization"]),
            ("Deep learning", ["deep learning", "neural networks", "CNN"]),
            ("NLP", ["natural language", "text mining", "transformers"]),
        ]
        
        for i in range(40):
            topic, keywords = topics[i % len(topics)]
            publications.append(Publication(
                scopus_id=str(i),
                title=f"{topic} Study {i}",
                authors=[f"Author{i % 5}", f"Author{(i + 2) % 5}"],
                affiliations=[f"University{i % 3}"],
                keywords=keywords + [f"specific{i % 8}"],
                publication_year=2019 + (i % 6),
                citation_count=i * 5,
                open_access=i % 3 == 0,
                document_type="Article" if i % 4 != 0 else "Conference Paper",
                publication_name=f"Journal{i % 4}",
            ))
        
        return publications
    
    @pytest.fixture
    def rich_recommender(self, rich_publications):
        """Create recommender with rich data."""
        analyzer = TrendAnalyzer(rich_publications)
        return Recommender(analyzer)
    
    def test_emerging_topics(self, rich_recommender):
        """Test emerging topics recommendations."""
        recommendations = rich_recommender.get_recommendations(
            top_n=5,
            include_categories=['emerging_topics']
        )
        
        for rec in recommendations:
            assert rec.category == 'emerging_topics'
            assert len(rec.keywords) > 0
    
    def test_venue_recommendations(self, rich_recommender):
        """Test venue recommendations."""
        recommendations = rich_recommender.get_recommendations(
            top_n=5,
            include_categories=['venues']
        )
        
        for rec in recommendations:
            assert rec.category == 'venues'
            assert "Journal" in rec.title or "Venue" in rec.title
