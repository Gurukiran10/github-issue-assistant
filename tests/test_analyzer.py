"""
Unit tests for the GitHub Issue Assistant backend
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import json
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from issue_analyzer import IssueAnalyzer


class TestIssueAnalyzer:
    """Test suite for IssueAnalyzer"""
    
    @pytest.fixture
    def analyzer(self):
        """Fixture to create analyzer instance"""
        with patch.dict(os.environ, {'GOOGLE_API_KEY': 'test_key'}):
            with patch('issue_analyzer.genai'):
                return IssueAnalyzer()
    
    def test_parse_repo_url_https(self):
        """Test parsing HTTPS repository URLs"""
        analyzer = IssueAnalyzer.__new__(IssueAnalyzer)
        
        owner, repo = analyzer.parse_repo_url("https://github.com/facebook/react")
        assert owner == "facebook"
        assert repo == "react"
    
    def test_parse_repo_url_https_with_git(self):
        """Test parsing HTTPS repository URLs with .git suffix"""
        analyzer = IssueAnalyzer.__new__(IssueAnalyzer)
        
        owner, repo = analyzer.parse_repo_url("https://github.com/facebook/react.git")
        assert owner == "facebook"
        assert repo == "react"
    
    def test_parse_repo_url_ssh(self):
        """Test parsing SSH repository URLs"""
        analyzer = IssueAnalyzer.__new__(IssueAnalyzer)
        
        owner, repo = analyzer.parse_repo_url("git@github.com:facebook/react.git")
        assert owner == "facebook"
        assert repo == "react"
    
    def test_parse_repo_url_invalid(self):
        """Test parsing invalid repository URLs"""
        analyzer = IssueAnalyzer.__new__(IssueAnalyzer)
        
        with pytest.raises(ValueError):
            analyzer.parse_repo_url("https://gitlab.com/owner/repo")
    
    def test_parse_llm_response_valid(self):
        """Test parsing valid LLM response"""
        analyzer = IssueAnalyzer.__new__(IssueAnalyzer)
        
        response = """{
            "summary": "Test summary",
            "type": "bug",
            "priority_score": "3/5: Medium priority",
            "suggested_labels": ["bug", "ui"],
            "potential_impact": "Test impact"
        }"""
        
        result = analyzer.parse_llm_response(response)
        
        assert result["summary"] == "Test summary"
        assert result["type"] == "bug"
        assert result["priority_score"] == "3/5: Medium priority"
        assert len(result["suggested_labels"]) == 2
        assert result["potential_impact"] == "Test impact"
    
    def test_parse_llm_response_with_markdown(self):
        """Test parsing LLM response with markdown formatting"""
        analyzer = IssueAnalyzer.__new__(IssueAnalyzer)
        
        response = """Here's the analysis:
        ```json
        {
            "summary": "Test summary",
            "type": "feature_request",
            "priority_score": "2/5: Low priority",
            "suggested_labels": ["feature"],
            "potential_impact": "Test impact"
        }
        ```"""
        
        result = analyzer.parse_llm_response(response)
        
        assert result["summary"] == "Test summary"
        assert result["type"] == "feature_request"
    
    def test_parse_llm_response_invalid_json(self):
        """Test parsing invalid JSON response"""
        analyzer = IssueAnalyzer.__new__(IssueAnalyzer)
        
        with pytest.raises(ValueError):
            analyzer.parse_llm_response("{invalid json}")
    
    def test_parse_llm_response_missing_fields(self):
        """Test parsing response with missing required fields"""
        analyzer = IssueAnalyzer.__new__(IssueAnalyzer)
        
        response = """{
            "summary": "Test summary",
            "type": "bug"
        }"""
        
        with pytest.raises(ValueError):
            analyzer.parse_llm_response(response)
    
    def test_parse_llm_response_invalid_type(self):
        """Test parsing response with invalid type"""
        analyzer = IssueAnalyzer.__new__(IssueAnalyzer)
        
        response = """{
            "summary": "Test summary",
            "type": "invalid_type",
            "priority_score": "3/5",
            "suggested_labels": ["label"],
            "potential_impact": "Impact"
        }"""
        
        result = analyzer.parse_llm_response(response)
        assert result["type"] == "other"  # Should default to "other"
    
    def test_generate_analysis_prompt(self):
        """Test prompt generation"""
        analyzer = IssueAnalyzer.__new__(IssueAnalyzer)
        
        issue_data = {
            "title": "Test Issue",
            "body": "Test body",
            "comments": ["Comment 1", "Comment 2"],
            "labels": ["bug"],
            "state": "open",
            "created_at": "2024-01-01",
            "updated_at": "2024-01-02"
        }
        
        prompt = analyzer.generate_analysis_prompt(issue_data)
        
        assert "Test Issue" in prompt
        assert "Test body" in prompt
        assert "Comment 1" in prompt
        assert "json" in prompt.lower()


class TestIntegration:
    """Integration tests"""
    
    @pytest.mark.asyncio
    async def test_api_endpoint(self):
        """Test API endpoint (requires backend running)"""
        # This test would require the API to be running
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
