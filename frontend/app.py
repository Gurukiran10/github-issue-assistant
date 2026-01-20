"""
Streamlit Frontend for GitHub Issue Assistant
Simple and user-friendly interface for analyzing GitHub issues
"""

import streamlit as st
import requests
import json
from urllib.parse import urlparse
import time

# Page configuration
st.set_page_config(
    page_title="GitHub Issue Assistant",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stButton>button {
        width: 100%;
        padding: 0.5rem 1rem;
        font-size: 1rem;
    }
    .analysis-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("🔍 GitHub Issue Assistant")
st.markdown("Leverage AI to analyze GitHub issues and generate actionable insights")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    api_url = st.text_input(
        "API Endpoint",
        value="http://localhost:8000",
        help="URL of the backend API server"
    )
    
    st.markdown("---")
    st.markdown("""
    ### 📖 How to Use:
    1. Enter a GitHub repository URL
    2. Specify the issue number
    3. Click "Analyze Issue"
    4. View the AI-generated analysis
    
    ### 💡 Tips:
    - Make sure the backend API is running
    - Use public repositories
    - The analysis typically takes 5-10 seconds
    """)

# Main content area
st.markdown("---")

# Input section
col1, col2 = st.columns([3, 1])

with col1:
    repo_url = st.text_input(
        "GitHub Repository URL",
        placeholder="https://github.com/facebook/react",
        help="Enter the full GitHub repository URL"
    )

with col2:
    issue_number = st.number_input(
        "Issue Number",
        min_value=1,
        value=1,
        help="Enter the issue number to analyze"
    )

# Validation and analysis
def validate_inputs(repo_url: str, issue_number: int) -> tuple:
    """Validate user inputs"""
    errors = []
    
    if not repo_url or not repo_url.strip():
        errors.append("Repository URL is required")
    elif "github.com" not in repo_url.lower():
        errors.append("Please enter a valid GitHub repository URL")
    
    if issue_number < 1:
        errors.append("Issue number must be positive")
    
    return len(errors) == 0, errors


def call_api(api_url: str, repo_url: str, issue_number: int) -> dict:
    """Call the backend API"""
    endpoint = f"{api_url}/analyze"
    payload = {
        "repo_url": repo_url,
        "issue_number": issue_number
    }
    
    try:
        response = requests.post(
            endpoint,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        raise Exception(f"Cannot connect to API at {api_url}. Is the backend running?")
    except requests.exceptions.Timeout:
        raise Exception("API request timed out. The issue might be too large.")
    except requests.exceptions.HTTPError as e:
        try:
            error_detail = response.json().get("detail", str(e))
        except:
            error_detail = str(e)
        raise Exception(f"API Error: {error_detail}")
    except Exception as e:
        raise Exception(f"Unexpected error: {str(e)}")


# Analyze button
if st.button("🚀 Analyze Issue", type="primary"):
    is_valid, errors = validate_inputs(repo_url, issue_number)
    
    if not is_valid:
        st.error("❌ " + " | ".join(errors))
    else:
        with st.spinner("🔄 Analyzing issue..."):
            try:
                analysis = call_api(api_url, repo_url, issue_number)
                
                # Store result in session state
                st.session_state.analysis_result = analysis
                st.session_state.analysis_repo_url = repo_url
                st.session_state.analysis_issue_number = issue_number
                
                st.success("✅ Analysis complete!")
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Display results if available
if "analysis_result" in st.session_state:
    analysis = st.session_state.analysis_result
    
    st.markdown("---")
    st.markdown("## 📊 Analysis Results")
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["Summary", "Metrics", "Labels", "JSON"])
    
    with tab1:
        st.markdown("### 📝 Issue Summary")
        st.info(analysis["summary"])
        
        st.markdown("### 📌 Issue Type")
        type_colors = {
            "bug": "🔴",
            "feature_request": "🟢",
            "documentation": "🔵",
            "question": "🟡",
            "other": "⚫"
        }
        type_emoji = type_colors.get(analysis["type"], "⚫")
        st.write(f"{type_emoji} **{analysis['type'].replace('_', ' ').title()}**")
        
        st.markdown("### 💥 Potential Impact")
        st.warning(analysis["potential_impact"])
    
    with tab2:
        st.markdown("### 📈 Priority Score")
        
        # Extract score from string like "3/5: ..."
        priority_str = analysis["priority_score"]
        try:
            score_num = int(priority_str.split("/")[0])
            st.metric("Priority Level", f"{score_num}/5")
        except:
            st.write(priority_str)
        
        st.write(f"**Details:** {priority_str}")
    
    with tab3:
        st.markdown("### 🏷️ Suggested Labels")
        
        labels = analysis["suggested_labels"]
        if labels:
            cols = st.columns(len(labels))
            for col, label in zip(cols, labels):
                with col:
                    st.button(
                        f"#{label}",
                        key=f"label_{label}",
                        disabled=True
                    )
        else:
            st.info("No labels suggested")
    
    with tab4:
        st.markdown("### 📋 Full JSON Response")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.json(analysis)
        
        with col2:
            # Copy button
            json_str = json.dumps(analysis, indent=2)
            st.text_area(
                "Copy JSON:",
                value=json_str,
                height=300,
                disabled=True
            )
            
            if st.button("📋 Copy to Clipboard", key="copy_json"):
                st.success("✅ Copied to clipboard!")
    
    # Footer info
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.caption(f"📍 Repository: {st.session_state.analysis_repo_url}")
    
    with col2:
        st.caption(f"🔢 Issue: #{st.session_state.analysis_issue_number}")
    
    with col3:
        st.caption(f"⏰ Analyzed at: {time.strftime('%Y-%m-%d %H:%M:%S')}")

else:
    # Welcome message
    st.info("""
    👋 **Welcome to GitHub Issue Assistant!**
    
    This tool uses AI to analyze GitHub issues and provide structured insights including:
    - **Summary**: One-sentence overview of the issue
    - **Type**: Classification (bug, feature request, documentation, question, or other)
    - **Priority Score**: Numerical priority with justification
    - **Suggested Labels**: Recommended GitHub labels for organization
    - **Impact Analysis**: Potential user impact (especially for bugs)
    
    Start by entering a repository URL and issue number above, then click "Analyze Issue".
    """)

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: gray; font-size: 0.8rem;">
    <p>GitHub Issue Assistant | Powered by AI | Built for SeedlingLabs</p>
</div>
""", unsafe_allow_html=True)
