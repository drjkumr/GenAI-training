import os
import json
from typing import TypedDict, List, Annotated, Dict, Any
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from utils import parse_resume, load_screenings

# Define the state of the workflow
class AgentState(TypedDict):
    resume_path: str
    target_role: str
    resume_text: str
    criteria: Dict[str, Any]
    match_data: Dict[str, Any]
    score: float
    shortlisted: bool
    explanation: str
    output: Dict[str, Any]

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# Node 1: Resume Parser
def resume_parser_node(state: AgentState):
    print("--- PARSING RESUME ---")
    text = parse_resume(state["resume_path"])
    return {"resume_text": text}

# Node 2: Criteria Loader
def criteria_loader_node(state: AgentState):
    print("--- LOADING CRITERIA ---")
    all_screenings = load_screenings()
    # Find the specific role
    role_criteria = next((s for s in all_screenings if s["role"] == state["target_role"]), None)
    if not role_criteria:
        raise ValueError(f"Role '{state['target_role']}' not found in screenings.txt")
    return {"criteria": role_criteria}

# Node 3: Matcher
def matcher_node(state: AgentState):
    print("--- MATCHING RESUME ---")
    prompt = f"""
    Compare the following resume text against the job criteria.
    
    JOB CRITERIA:
    {json.dumps(state['criteria'], indent=2)}
    
    RESUME TEXT:
    {state['resume_text']}
    
    Identify:
    1. Matched Skills
    2. Missing Skills
    3. Experience Match (Yes/No)
    4. Education Match (Yes/No)
    
    Return ONLY a JSON object.
    """
    response = llm.invoke([SystemMessage(content="You are an expert HR recruiter."), HumanMessage(content=prompt)])
    # Extract JSON from response (handling potential markdown blocks)
    content = response.content.replace("```json", "").replace("```", "").strip()
    match_data = json.loads(content)
    return {"match_data": match_data}

# Node 4: Scoring
def scoring_node(state: AgentState):
    print("--- SCORING ---")
    prompt = f"""
    Based on the following match analysis, provide an ATS score between 0 and 10.
    
    MATCH ANALYSIS:
    {json.dumps(state['match_data'], indent=2)}
    
    JOB CRITERIA:
    {json.dumps(state['criteria'], indent=2)}
    
    The score should be a float. Factors:
    - Skill overlap: 50%
    - Experience: 30%
    - Education: 10%
    - Project buzzwords: 10%
    
    Return ONLY the score as a float.
    """
    response = llm.invoke([SystemMessage(content="You are an ATS Scoring Algorithm."), HumanMessage(content=prompt)])
    try:
        score = float(response.content.strip())
    except:
        # Fallback if LLM returns text
        score = 5.0 
    return {"score": score}

# Node 5: Filter
def filter_node(state: AgentState):
    print("--- FILTERING ---")
    is_shortlisted = state["score"] >= 7.0
    return {"shortlisted": is_shortlisted}

# Node 6: Explanation
def explanation_node(state: AgentState):
    print("--- GENERATING EXPLANATION ---")
    prompt = f"""
    Generate a human-readable explanation for the candidate regarding their ATS score of {state['score']}/10 for the role of {state['target_role']}.
    Shortlisted: {state['shortlisted']}
    
    Analysis:
    {json.dumps(state['match_data'], indent=2)}
    
    Keep it professional and constructive.
    """
    response = llm.invoke([SystemMessage(content="You are a career coach."), HumanMessage(content=prompt)])
    
    explanation = response.content.strip()
    
    # Construct final output
    final_output = {
        "role": state["target_role"],
        "score": state["score"],
        "shortlisted": state["shortlisted"],
        "matched_skills": state["match_data"].get("matched_skills", []),
        "missing_skills": state["match_data"].get("missing_skills", []),
        "explanation": explanation
    }
    
    return {"explanation": explanation, "output": final_output}

# Build Graph
workflow = StateGraph(AgentState)

workflow.add_node("parser", resume_parser_node)
workflow.add_node("loader", criteria_loader_node)
workflow.add_node("matcher", matcher_node)
workflow.add_node("scoring", scoring_node)
workflow.add_node("filter", filter_node)
workflow.add_node("explanation", explanation_node)

workflow.set_entry_point("parser")
workflow.add_edge("parser", "loader")
workflow.add_edge("loader", "matcher")
workflow.add_edge("matcher", "scoring")
workflow.add_edge("scoring", "filter")
workflow.add_edge("filter", "explanation")
workflow.add_edge("explanation", END)

app_graph = workflow.compile()

def run_ats_workflow(resume_path: str, target_role: str):
    initial_state = {
        "resume_path": resume_path,
        "target_role": target_role,
        "resume_text": "",
        "criteria": {},
        "match_data": {},
        "score": 0.0,
        "shortlisted": False,
        "explanation": "",
        "output": {}
    }
    result = app_graph.invoke(initial_state)
    return result["output"]
