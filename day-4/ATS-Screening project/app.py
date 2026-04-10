import streamlit as st
import os
import pandas as pd
from utils import load_screenings, add_resume_to_db, search_resumes, parse_resume
from workflow import run_ats_workflow
from dotenv import load_dotenv

load_dotenv()

# Page Config
st.set_page_config(page_title="UltraATS | Resume Screener", page_icon="🚀", layout="wide")

# Custom CSS for Premium Look
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .card {
        background: rgba(255, 255, 255, 0.05);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 1rem;
    }
    .status-badge {
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .shortlisted { background-color: #28a745; color: white; }
    .rejected { background-color: #dc3545; color: white; }
    
    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .animate-in { animation: fadeIn 0.5s ease-out; }
</style>
""", unsafe_allow_html=True)

# Sidebar - API Key Configuration
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/942/942748.png", width=100)
    st.title("Settings")
    api_key = st.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY", ""))
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
        st.success("API Key Active!")
    else:
        st.warning("Please enter OpenAI API Key to start.")

# Main Header
st.markdown("<h1 class='main-header'>UltraATS Screener 🚀</h1>", unsafe_allow_html=True)
st.markdown("### Semantic Resume Intelligence & Automated Scoring")

tab1, tab2, tab3 = st.tabs(["📤 Upload & Screen", "📊 Candidate Dashboard", "🔍 Semantic Search"])

with tab1:
    st.markdown("### 1. Configure Screening")
    roles_data = load_screenings()
    role_names = [r["role"] for r in roles_data]
    
    col1, col2 = st.columns([1, 1])
    with col1:
        selected_role = st.selectbox("Select Target Role", role_names)
    with col2:
        uploaded_files = st.file_uploader("Upload Resumes (PDF, DOCX, TXT)", accept_multiple_files=True)

    if st.button("Run ATS Screening ✨", disabled=not api_key):
        if not uploaded_files:
            st.error("Please upload at least one resume.")
        else:
            if "results" not in st.session_state:
                st.session_state.results = []
            
            with st.status("Analyzing Resumes...", expanded=True) as status:
                for uploaded_file in uploaded_files:
                    st.write(f"Processing {uploaded_file.name}...")
                    
                    # Save file temporarily
                    temp_path = os.path.join("temp", uploaded_file.name)
                    os.makedirs("temp", exist_ok=True)
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    try:
                        # Run Graph
                        result = run_ats_workflow(temp_path, selected_role)
                        result["candidate_name"] = uploaded_file.name
                        st.session_state.results.append(result)
                        
                        # Add to ChromaDB for search later
                        resume_text = parse_resume(temp_path)
                        add_resume_to_db(uploaded_file.name, resume_text, {"role": selected_role, "score": result["score"]})
                        
                    except Exception as e:
                        st.error(f"Error processing {uploaded_file.name}: {e}")
                    
                    # Clean up
                    os.remove(temp_path)
                
                status.update(label="Screening Complete!", state="complete", expanded=False)
            st.success("Done! Head over to the Dashboard to see results.")

with tab2:
    st.markdown("### Candidate Ranking")
    if "results" in st.session_state and st.session_state.results:
        # Convert to DataFrame for easier display
        df = pd.DataFrame(st.session_state.results)
        
        # Highlight candidates with score >= 7.0
        shortlisted_only = df[df["shortlisted"] == True].sort_values(by="score", ascending=False)
        
        if not shortlisted_only.empty:
            st.markdown("#### ✅ Shortlisted Candidates (Score ≥ 7.0)")
            for idx, row in shortlisted_only.iterrows():
                with st.container():
                    st.markdown(f"""
                    <div class="card animate-in">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h3 style="margin: 0;">👤 {row['candidate_name']}</h3>
                            <span class="status-badge shortlisted">SCORE: {row['score']}/10</span>
                        </div>
                        <p style="margin-top: 10px; color: #a0a0a0;"><b>Role:</b> {row['role']}</p>
                        <p><b>Matched Skills:</b> {', '.join(row['matched_skills'])}</p>
                        <p><b>Explanation:</b> {row['explanation']}</p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No candidates have been shortlisted yet.")

        with st.expander("Show All Results (Including Non-Shortlisted)"):
            st.table(df[["candidate_name", "role", "score", "shortlisted"]])
    else:
        st.info("Upload resumes in the first tab to see the dashboard.")

with tab3:
    st.markdown("### Semantic Resume Search")
    st.markdown("Search beyond keywords. Try queries like *'Experience with distributed systems'* or *'Strong backend developer with Docker'*. ")
    
    search_query = st.text_input("Look for specific expertise...")
    if search_query:
        results = search_resumes(search_query)
        if results["documents"]:
            for i in range(len(results["documents"][0])):
                doc = results["documents"][0][i]
                meta = results["metadatas"][0][i]
                name = results["ids"][0][i]
                
                with st.container():
                    st.markdown(f"""
                    <div class="card">
                        <h4>🔍 Match: {name}</h4>
                        <p><b>Original Role Context:</b> {meta.get('role', 'N/A')}</p>
                        <p><b>Snippet:</b> {doc[:300]}...</p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No semantic matches found.")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #666;'>UltraATS v1.0 | Built with LangGraph & Streamlit</p>", unsafe_allow_html=True)
