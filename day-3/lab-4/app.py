import streamlit as st
import os
from dotenv import load_dotenv
from research_pipeline import get_research_pipeline

# Load environment variables
load_dotenv()

# Page Setup
st.set_page_config(page_title="Multi-Agent Research Pipeline", page_icon="📝", layout="wide")

# Custom CSS for premium look
st.markdown("""
    <style>
    .main {
        background: #f8f9fa;
        color: #1a1a1a;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    .agent-status {
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
        border-left: 5px solid #2e7d32;
        background: #e8f5e9;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Multi-Agent Research Assistant")
st.markdown("Lab 4: A 3-agent system (Researcher, Writer, Editor) using LangGraph and ChromaDB.")

# Sidebar for API Key
with st.sidebar:
    st.header("Settings")
    # Priority: Manual Input > Environment Variable
    default_key = os.getenv("OPENAI_API_KEY", "")
    api_key = st.text_input("Enter OpenAI API Key", value=default_key, type="password")
    st.info("API Key loaded from .env if available.")

    st.divider()
    st.header("🛠️ LangSmith Tracing")
    enable_tracing = st.checkbox("Enable LangSmith Tracing", value=os.getenv("LANGCHAIN_TRACING_V2") == "true")
    ls_api_key = st.text_input("LangSmith API Key", value=os.getenv("LANGCHAIN_API_KEY", ""), type="password")
    ls_project = st.text_input("LangSmith Project", value=os.getenv("LANGCHAIN_PROJECT", "default"))
    
    if enable_tracing:
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_API_KEY"] = ls_api_key
        os.environ["LANGCHAIN_PROJECT"] = ls_project

# Main Input
topic = st.text_input("What would you like me to research?", placeholder="e.g. The impact of Generative AI on Software Engineering")

if st.button("Start Research Pipeline"):
    if not api_key:
        st.error("Please provide an OpenAI API Key in the sidebar.")
    elif not topic:
        st.warning("Please enter a research topic.")
    else:
        with st.status("Pipeline initializing...", expanded=True) as status:
            try:
                # Initialize Graph
                app = get_research_pipeline(api_key)
                
                # Initial State
                state = {
                    "topic": topic,
                    "research_data": "",
                    "draft": "",
                    "final_report": "",
                    "messages": []
                }
                
                # Run the graph and stream events
                st.write("🏃 Running multi-agent workflow...")
                
                final_state = app.invoke(state)
                
                status.update(label="Research Complete!", state="complete", expanded=False)
                
                # Display Results
                st.divider()
                
                # Report Header with Download Button
                col1, col2 = st.columns([0.8, 0.2])
                with col1:
                    st.subheader("📄 Final Research Report")
                with col2:
                    st.download_button(
                        label="📥 Download Markdown",
                        data=final_state["final_report"],
                        file_name=f"research_report_{topic.replace(' ', '_')}.md",
                        mime="text/markdown"
                    )
                
                st.markdown(final_state["final_report"])
                
                # Optional: Show process logs
                with st.expander("Show Agent Process Logs"):
                    for msg in final_state["messages"]:
                        st.info(msg.content)

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                status.update(label="Pipeline Failed", state="error")

# Footer
st.markdown("---")
st.caption("Built with LangGraph, OpenAI, ChromaDB, and Streamlit.")
