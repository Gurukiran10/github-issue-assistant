"""
FastAPI Backend for AI-Powered GitHub Issue Assistant
Main entry point for the application
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
from issue_analyzer import IssueAnalyzer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="GitHub Issue Assistant",
    description="AI-powered GitHub issue analysis API",
    version="1.0.0"
)

# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class IssueRequest(BaseModel):
    repo_url: str
    issue_number: int


class IssueAnalysis(BaseModel):
    summary: str
    type: str
    priority_score: str
    suggested_labels: list
    potential_impact: str


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "GitHub Issue Assistant API is running"
    }


@app.post("/analyze", response_model=IssueAnalysis)
async def analyze_issue(request: IssueRequest):
    """
    Analyze a GitHub issue using AI.
    
    Args:
        repo_url: GitHub repository URL (e.g., https://github.com/owner/repo)
        issue_number: Issue number to analyze
    
    Returns:
        IssueAnalysis: Structured analysis of the GitHub issue
    """
    try:
        logger.info(f"Analyzing issue #{request.issue_number} from {request.repo_url}")
        
        analyzer = IssueAnalyzer()
        result = analyzer.analyze(request.repo_url, request.issue_number)
        
        return IssueAnalysis(**result)
    
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Detailed health check endpoint"""
    return {
        "status": "healthy",
        "service": "GitHub Issue Assistant API",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
