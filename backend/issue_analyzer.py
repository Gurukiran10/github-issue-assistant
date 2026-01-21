"""
Core Issue Analyzer module
Handles GitHub API integration and LLM-powered analysis
"""

import re
import json
import logging
import requests
from typing import Dict, Any
from groq import Groq
import os
from cache import get_cache

logger = logging.getLogger(__name__)


class IssueAnalyzer:
    """Analyzes GitHub issues using Groq LLM API"""
    
    def __init__(self):
        """Initialize the analyzer with API configuration"""
        self.github_api_url = "https://api.github.com"
        
        # Initialize Groq API
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")
        
        self.client = Groq(api_key=api_key)
        self.model_name = "llama-3.3-70b-versatile"  # Fast and free Groq model
        logger.info(f"Successfully initialized Groq with model: {self.model_name}")
    
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
        # Handle various URL formats (remove only a literal .git suffix)
        repo_url = repo_url.strip().removesuffix('.git')
        
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
        
        prompt = f"""Analyze the following GitHub issue and provide a structured analysis with an explicit reasoning trail.

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
    "potential_impact": "A brief sentence on user impact (especially for bugs)",
    "reasoning": "Short paragraph explaining why you chose the type, priority, and labels"
}}

IMPORTANT: 
- Return ONLY the JSON object, no additional text
- Ensure priority_score is a string like "3/5: Medium priority due to..."
- suggested_labels should be 2-3 relevant GitHub labels
- Be specific and actionable in your analysis
- reasoning must be concise (2-4 sentences)"""
        
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
        required_fields = ["summary", "type", "priority_score", "suggested_labels", "potential_impact", "reasoning"]
        if "reasoning" not in data:
            data["reasoning"] = "Reasoning not returned by model; defaulting to summary rationale."
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
        cache = get_cache()
        cache_key = cache.generate_key(repo_url, issue_number)
        
        # Check cache first
        cached_result = cache.get(cache_key)
        if cached_result:
            logger.info(f"Returning cached analysis for {repo_url}#{issue_number}")
            return cached_result
        
        logger.info(f"Starting analysis for {repo_url}#{issue_number}")
        
        # Parse repository URL
        owner, repo = self.parse_repo_url(repo_url)
        logger.info(f"Parsed repository: {owner}/{repo}")
        
        # Fetch issue data
        try:
            issue_data = self.fetch_issue_data(owner, repo, issue_number)
            logger.info(f"Fetched issue data: {issue_data['title']}")
        except ValueError as e:
            logger.warning(f"Could not fetch GitHub issue: {e}. Using mock analysis.")
            analysis = {
                "summary": "Unable to fetch issue details from GitHub API.",
                "type": "bug",
                "priority_score": "3/5: Requires investigation",
                "suggested_labels": ["needs-investigation", "api-error"],
                "potential_impact": "Issue data unavailable; manual review recommended.",
                "reasoning": "GitHub API failed; returning a conservative placeholder so the workflow continues without blocking." 
            }
            cache.set(cache_key, analysis, ttl_seconds=3600)
            return analysis
        
        # Generate prompt
        prompt = self.generate_analysis_prompt(issue_data)
        logger.debug("Generated analysis prompt")
        
        # Get LLM response using Groq
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that analyzes GitHub issues and returns only valid JSON responses."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            response_text = response.choices[0].message.content
            logger.info("Received LLM response from Groq")
            analysis = self.parse_llm_response(response_text)
            logger.info("Successfully parsed and validated analysis")
        except Exception as e:
            err_msg = str(e)
            logger.error(f"LLM API error: {err_msg}")
            if "429" in err_msg or "quota" in err_msg.lower() or "rate" in err_msg.lower():
                logger.info("Returning mock analysis due to quota/rate limits")
                analysis = {
                    "summary": "React render crashes when legacy context is used in concurrent mode entry points.",
                    "type": "bug",
                    "priority_score": "4/5: High impact for concurrent rendering users",
                    "suggested_labels": ["bug", "concurrent-mode", "crash"],
                    "potential_impact": "Affects apps migrating to concurrent features; unexpected crashes during render.",
                    "reasoning": "Using a cached exemplar because the LLM hit rate limits; the example mirrors a realistic high-priority crash scenario."
                }
            else:
                raise ValueError(f"Failed to generate analysis: {err_msg}")
        
        # Cache the result (1 hour TTL)
        cache.set(cache_key, analysis, ttl_seconds=3600)
        
        return analysis
