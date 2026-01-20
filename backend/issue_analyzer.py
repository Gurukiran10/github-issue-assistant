"""
Core Issue Analyzer module
Handles GitHub API integration and LLM-powered analysis
"""

import re
import json
import logging
import requests
from typing import Dict, Any
import google.generativeai as genai
import os

logger = logging.getLogger(__name__)


class IssueAnalyzer:
    """Analyzes GitHub issues using the Google Gemini API"""
    
    def __init__(self):
        """Initialize the analyzer with API configuration"""
        self.github_api_url = "https://api.github.com"
        
        # Initialize Gemini API
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is not set")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def parse_repo_url(self, repo_url: str) -> tuple:
        """
        Parse GitHub repository URL to extract owner and repo name.
        
        Args:
            repo_url: GitHub repository URL
            
        Returns:
            Tuple of (owner, repo)
            
        Raises:
            ValueError: If URL format is invalid
        """
        # Handle various URL formats
        repo_url = repo_url.strip().rstrip('.git')
        
        # Extract from https://github.com/owner/repo or git@github.com:owner/repo
        match = re.search(r'github\.com[:/]([^/]+)/([^/\s]+?)(?:\.git)?/?$', repo_url)
        
        if not match:
            raise ValueError(
                f"Invalid GitHub URL format. Expected: https://github.com/owner/repo"
            )
        
        owner, repo = match.groups()
        return owner, repo
    
    def fetch_issue_data(self, owner: str, repo: str, issue_number: int) -> Dict[str, Any]:
        """
        Fetch issue data from GitHub API.
        
        Args:
            owner: Repository owner
            repo: Repository name
            issue_number: Issue number to fetch
            
        Returns:
            Dictionary containing issue data
            
        Raises:
            ValueError: If issue doesn't exist or API fails
        """
        headers = {
            "Accept": "application/vnd.github.v3+json"
        }
        
        # Add GitHub token if available for higher rate limits
        github_token = os.getenv("GITHUB_TOKEN")
        if github_token:
            headers["Authorization"] = f"token {github_token}"
        
        # Fetch issue
        issue_url = f"{self.github_api_url}/repos/{owner}/{repo}/issues/{issue_number}"
        
        try:
            response = requests.get(issue_url, headers=headers, timeout=10)
            response.raise_for_status()
            issue = response.json()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                raise ValueError(f"Issue #{issue_number} not found in {owner}/{repo}")
            raise ValueError(f"GitHub API error: {response.status_code}")
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to fetch issue from GitHub: {str(e)}")
        
        # Fetch comments
        comments_url = f"{self.github_api_url}/repos/{owner}/{repo}/issues/{issue_number}/comments"
        
        try:
            comments_response = requests.get(comments_url, headers=headers, timeout=10)
            comments_response.raise_for_status()
            comments = comments_response.json()
        except requests.exceptions.RequestException:
            logger.warning(f"Failed to fetch comments for issue #{issue_number}")
            comments = []
        
        return {
            "title": issue.get("title", ""),
            "body": issue.get("body", ""),
            "comments": [comment.get("body", "") for comment in comments],
            "labels": [label.get("name", "") for label in issue.get("labels", [])],
            "state": issue.get("state", "open"),
            "created_at": issue.get("created_at", ""),
            "updated_at": issue.get("updated_at", ""),
        }
    
    def generate_analysis_prompt(self, issue_data: Dict[str, Any]) -> str:
        """
        Generate a detailed prompt for the LLM.
        
        Args:
            issue_data: Dictionary containing issue information
            
        Returns:
            Formatted prompt string
        """
        comments_text = "\n".join([f"- {comment[:200]}" for comment in issue_data["comments"][:5]])
        
        prompt = f"""Analyze the following GitHub issue and provide a structured analysis.

ISSUE TITLE: {issue_data['title']}

ISSUE BODY:
{issue_data['body'] or 'No description provided'}

COMMENTS (first 5):
{comments_text or 'No comments yet'}

EXISTING LABELS: {', '.join(issue_data['labels']) or 'None'}

Based on this information, analyze the issue and respond with ONLY a valid JSON object (no markdown, no extra text) with the following structure:
{{
  "summary": "A concise one-sentence summary of the main problem or request",
  "type": "One of: bug, feature_request, documentation, question, or other",
  "priority_score": "A score from 1 (low) to 5 (critical), formatted as 'X/5: justification'",
  "suggested_labels": ["label1", "label2", "label3"],
  "potential_impact": "A brief sentence on user impact (especially for bugs)"
}}

IMPORTANT: 
- Return ONLY the JSON object, no additional text
- Ensure priority_score is a string like "3/5: Medium priority due to..."
- suggested_labels should be 2-3 relevant GitHub labels
- Be specific and actionable in your analysis"""
        
        return prompt
    
    def parse_llm_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse and validate LLM response.
        
        Args:
            response_text: Raw response from LLM
            
        Returns:
            Parsed JSON response
            
        Raises:
            ValueError: If response is not valid JSON
        """
        # Try to extract JSON from response
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        
        if not json_match:
            raise ValueError("Could not extract JSON from LLM response")
        
        try:
            data = json.loads(json_match.group())
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in LLM response: {str(e)}")
        
        # Validate required fields
        required_fields = ["summary", "type", "priority_score", "suggested_labels", "potential_impact"]
        missing_fields = [f for f in required_fields if f not in data]
        
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
        
        # Validate type field
        valid_types = ["bug", "feature_request", "documentation", "question", "other"]
        if data["type"] not in valid_types:
            data["type"] = "other"
        
        # Ensure suggested_labels is a list
        if not isinstance(data["suggested_labels"], list):
            data["suggested_labels"] = [str(data["suggested_labels"])]
        
        # Limit to 3 labels
        data["suggested_labels"] = data["suggested_labels"][:3]
        
        return data
    
    def analyze(self, repo_url: str, issue_number: int) -> Dict[str, Any]:
        """
        Main analysis method orchestrating the entire workflow.
        
        Args:
            repo_url: GitHub repository URL
            issue_number: Issue number to analyze
            
        Returns:
            Structured analysis dictionary
        """
        logger.info(f"Starting analysis for {repo_url}#{issue_number}")
        
        # Parse repository URL
        owner, repo = self.parse_repo_url(repo_url)
        logger.info(f"Parsed repository: {owner}/{repo}")
        
        # Fetch issue data
        issue_data = self.fetch_issue_data(owner, repo, issue_number)
        logger.info(f"Fetched issue data: {issue_data['title']}")
        
        # Generate prompt
        prompt = self.generate_analysis_prompt(issue_data)
        logger.debug("Generated analysis prompt")
        
        # Get LLM response
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text
            logger.info("Received LLM response")
        except Exception as e:
            logger.error(f"LLM API error: {str(e)}")
            raise ValueError(f"Failed to generate analysis: {str(e)}")
        
        # Parse and validate response
        analysis = self.parse_llm_response(response_text)
        logger.info("Successfully parsed and validated analysis")
        
        return analysis
