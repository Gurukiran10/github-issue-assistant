"""
Streamlit Frontend for GitHub Issue Assistant
Simple and user-friendly interface for analyzing GitHub issues
"""

import streamlit as st
import requests
import json
import time
import os

# Page configuration
st.set_page_config(
    page_title="GitHub Issue Assistant",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header
st.title("🔍 GitHub Issue Assistant")
st.markdown("Leverage AI to analyze GitHub issues and generate actionable insights")

# Get backend URL from environment or use default, but override if an old host is configured
default_backend_url = os.getenv("BACKEND_URL")
if not default_backend_url or "github-issue-assistant-f33e" in default_backend_url:
    default_backend_url = "https://github-issue-assistant-backend.onrender.com"

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    api_url = st.text_input(
        "API Endpoint",
        value=default_backend_url,
        help="URL of the backend API server"
    )
    
    # Add usage instructions
    st.markdown("---")
    st.header("📖 How to Use")
    st.markdown("""
    1. **Paste a URL**: Enter a public GitHub repository link.
    2. **Issue Number**: Specify the ID of the issue you want to analyze.
    3. **Analyze**: Click the 'Analyze' button to start the AI engine.
    4. **Explore Tabs**: View the summary, metrics, and labels, or copy the raw JSON.
    """)
    st.info("💡 Tip: Use full URLs like 'https://github.com/facebook/react'")

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

# Validation
def validate_inputs(repo_url: str, issue_number: int):
    errors = []
    if not repo_url or not repo_url.strip():
        errors.append("Repository URL is required")
    elif "github.com" not in repo_url.lower():
        errors.append("Please enter a valid GitHub repository URL")
    if issue_number < 1:
        errors.append("Issue number must be positive")
    return len(errors) == 0, errors

# API call
def call_api(api_url: str, repo_url: str, issue_number: int):
    endpoint = f"{api_url}/analyze"
    payload = {"repo_url": repo_url, "issue_number": issue_number}
    response = requests.post(endpoint, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()

# Analyze button
if st.button("🚀 Analyze Issue", type="primary"):
    is_valid, errors = validate_inputs(repo_url, issue_number)
    
    if not is_valid:
        st.error("❌ " + " | ".join(errors))
    else:
        with st.spinner("🔄 Analyzing issue..."):
            try:
                start_time = time.time()
                analysis = call_api(api_url, repo_url, issue_number)
                duration = time.time() - start_time
                
                st.session_state.analysis_result = analysis
                st.session_state.analysis_repo_url = repo_url
                st.session_state.analysis_issue_number = issue_number
                st.session_state.analysis_duration = round(duration, 2)
                
                st.success("✅ Analysis complete!")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Display results
if "analysis_result" in st.session_state:
    analysis = st.session_state.analysis_result
    
    st.markdown("---")
    st.markdown("## 📊 Analysis Results")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Summary", "Metrics", "Labels", "JSON"])
    
    with tab1:
        st.markdown("### 📝 Issue Summary")
        st.info(analysis["summary"])
        
        if "reasoning" in analysis:
            with st.expander("🔍 See AI Reasoning"):
                st.write(analysis["reasoning"])
        
        st.markdown("### 📌 Issue Type")
        type_emoji = {"bug": "🔴", "feature_request": "🟢", "documentation": "🔵", "question": "🟡", "other": "⚫"}
        emoji = type_emoji.get(analysis["type"], "⚫")
        st.write(f"{emoji} **{analysis['type'].replace('_', ' ').title()}**")
        
        st.markdown("### 💥 Potential Impact")
        st.warning(analysis["potential_impact"])
    
    with tab2:
        st.markdown("### 📈 Priority Score")
        try:
            score_num = int(analysis["priority_score"].split("/")[0])
            st.metric("Priority Level", f"{score_num}/5")
        except:
            st.write(analysis["priority_score"])
        
        st.write(f"**Details:** {analysis['priority_score']}")
        if "analysis_duration" in st.session_state:
            st.caption(f"⏱️ Completed in {st.session_state.analysis_duration}s")
    
    with tab3:
        st.markdown("### 🏷️ Suggested Labels")
        labels = analysis["suggested_labels"]
        if labels:
            cols = st.columns(len(labels))
            for col, label in zip(cols, labels):
                with col:
                    st.button(f"#{label}", disabled=True)
        else:
            st.info("No labels suggested")
    
    with tab4:
        st.markdown("### 📋 Full JSON Response")
        col1, col2 = st.columns(2)
        
        with col1:
            st.json(analysis)
        
        with col2:
            json_str = json.dumps(analysis, indent=2)
            st.text_area("Copy JSON:", value=json_str, height=300, disabled=True)
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption(f"📍 Repository: {st.session_state.analysis_repo_url}")
    with col2:
        st.caption(f"🔢 Issue: #{st.session_state.analysis_issue_number}")
    with col3:
        st.caption(f"⏰ Analyzed at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
else:
    st.info("""
    👋 **Welcome to GitHub Issue Assistant!**
    
    This tool uses AI to analyze GitHub issues and provide structured insights including:
    - **Summary**: One-sentence overview
    - **Type**: Classification (bug, feature request, etc.)
    - **Priority Score**: Numerical priority with justification
    - **Suggested Labels**: Recommended GitHub labels
    - **Impact Analysis**: Potential user impact
    
    Start by entering a repository URL and issue number above.
    """)
