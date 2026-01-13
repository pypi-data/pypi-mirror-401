"""
Tests for the ScopusClient.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

from research_trends.client import ScopusClient, ScopusAPIError, RateLimiter
from research_trends.config import Config
from research_trends.models import Publication, SearchResult


class TestRateLimiter:
    """Tests for the RateLimiter class."""
    
    def test_init(self):
        """Test rate limiter initialization."""
        limiter = RateLimiter(requests_per_second=10)
        assert limiter.requests_per_second == 10
        assert limiter.min_interval == 0.1
    
    def test_wait_first_request(self):
        """Test that first request doesn't wait."""
        limiter = RateLimiter(requests_per_second=10)
        start = datetime.now()
        limiter.wait()
        elapsed = (datetime.now() - start).total_seconds()
        assert elapsed < 0.1


class TestScopusClient:
    """Tests for the ScopusClient class."""
    
    @pytest.fixture
    def mock_config(self):
        """Create a mock configuration."""
        config = Mock(spec=Config)
        config.api_key = "test_api_key"
        config.institution_token = None
        config.rate_limit = 9
        config.cache_ttl = 86400
        config.base_url = "https://api.elsevier.com/content/search/scopus"
        config.abstract_url = "https://api.elsevier.com/content/abstract/scopus_id"
        config.validate.return_value = True
        return config
    
    @pytest.fixture
    def client(self, mock_config):
        """Create a client with mock config."""
        with patch.object(Config, '__init__', return_value=None):
            client = ScopusClient.__new__(ScopusClient)
            client.config = mock_config
            client.rate_limiter = RateLimiter(9)
            client._cache = {}
            client._session = MagicMock()
            return client
    
    def test_build_query_simple(self, client):
        """Test building a simple query."""
        query = client.build_query(query="machine learning")
        assert query == "TITLE-ABS-KEY(machine learning)"
    
    def test_build_query_with_years(self, client):
        """Test building a query with year range."""
        query = client.build_query(
            query="AI",
            start_year=2020,
            end_year=2024
        )
        assert "PUBYEAR > 2019" in query
        assert "PUBYEAR < 2025" in query
    
    def test_build_query_multiple_fields(self, client):
        """Test building a query with multiple fields."""
        query = client.build_query(
            title="neural network",
            keywords=["deep learning", "CNN"],
            authors="Smith"
        )
        assert "TITLE(neural network)" in query
        assert "KEY(deep learning OR CNN)" in query
        assert "AUTH(Smith)" in query
    
    def test_parse_publication(self, client):
        """Test parsing a publication entry."""
        entry = {
            "dc:identifier": "SCOPUS_ID:12345",
            "eid": "2-s2.0-12345",
            "prism:doi": "10.1234/test",
            "dc:title": "Test Publication",
            "dc:description": "Test abstract",
            "author": [{"authname": "Smith, J."}, {"authname": "Doe, J."}],
            "affiliation": [{"affilname": "Test University"}],
            "authkeywords": "keyword1 | keyword2",
            "prism:coverDate": "2024-01-15",
            "citedby-count": "42",
            "prism:publicationName": "Test Journal",
            "subtypeDescription": "Article",
            "openaccess": "1",
        }
        
        pub = client._parse_publication(entry)
        
        assert pub.scopus_id == "12345"
        assert pub.title == "Test Publication"
        assert pub.authors == ["Smith, J.", "Doe, J."]
        assert pub.citation_count == 42
        assert pub.open_access is True
    
    def test_context_manager(self, mock_config):
        """Test client as context manager."""
        with patch.object(Config, '__init__', return_value=None):
            with patch.object(ScopusClient, 'close') as mock_close:
                client = ScopusClient.__new__(ScopusClient)
                client.config = mock_config
                client.rate_limiter = RateLimiter(9)
                client._cache = {}
                client._session = MagicMock()
                
                with client as c:
                    assert c is client
                
                mock_close.assert_called_once()


class TestScopusAPIError:
    """Tests for the ScopusAPIError class."""
    
    def test_error_message(self):
        """Test error message."""
        error = ScopusAPIError("Test error", status_code=401)
        assert str(error) == "Test error"
        assert error.status_code == 401
    
    def test_error_without_status(self):
        """Test error without status code."""
        error = ScopusAPIError("Test error")
        assert error.status_code is None
