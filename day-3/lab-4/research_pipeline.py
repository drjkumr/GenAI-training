import os
from typing import TypedDict, Annotated, List
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
import chromadb
from chromadb.utils import embedding_functions

# Define the state object
class AgentState(TypedDict):
    topic: str
    research_data: str
    draft: str
    final_report: str
    messages: List[BaseMessage]

def get_research_pipeline(openai_api_key):
    # Initialize the LLM
    llm = ChatOpenAI(model="gpt-4o-mini", api_key=openai_api_key)
    search = DuckDuckGoSearchRun()
    
    # Initialize ChromaDB (Persistent Client)
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=openai_api_key,
        model_name="text-embedding-3-small"
    )
    collection = chroma_client.get_or_create_collection(
        name="research_notes",
        embedding_function=openai_ef
    )

    # Agent Nodes
    def researcher_node(state: AgentState):
        topic = state["topic"]
        print(f"--- RESEARCHER: Searching for info on {topic} ---")
        
        # Perform search
        search_results = search.run(topic)
        
        # Store in ChromaDB for future reference
        collection.add(
            documents=[search_results],
            ids=[f"res_{topic[:10]}_{len(search_results)}"],
            metadatas=[{"topic": topic}]
        )
        
        return {"research_data": search_results, "messages": [AIMessage(content=f"Found information on {topic}.")]}

    def writer_node(state: AgentState):
        research_data = state["research_data"]
        topic = state["topic"]
        print(f"--- WRITER: Drafting report ---")
        
        prompt = f"""You are a professional technical writer. 
        Topic: {topic}
        Research Data: {research_data}
        
        Write a detailed report based on the research data provided. 
        Use markdown formatting. Ensure it is well-structured with sections."""
        
        response = llm.invoke(prompt)
        return {"draft": response.content, "messages": [AIMessage(content="Drafted the initial report.")]}

    def editor_node(state: AgentState):
        draft = state["draft"]
        print(f"--- EDITOR: Polishing report ---")
        
        prompt = f"""You are an expert editor. Review and polish the following report draft.
        Improve clarity, tone, and formatting.
        
        Draft:
        {draft}
        
        Return the final polished version in markdown."""
        
        response = llm.invoke(prompt)
        
        # Save final report to ChromaDB as well
        collection.add(
            documents=[response.content],
            ids=[f"final_{state['topic'][:10]}"],
            metadatas=[{"type": "final_report", "topic": state["topic"]}]
        )
        
        return {"final_report": response.content, "messages": [AIMessage(content="Edited and finalized the report.")]}

    # Define the graph
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("writer", writer_node)
    workflow.add_node("editor", editor_node)

    # Define edges
    workflow.set_entry_point("researcher")
    workflow.add_edge("researcher", "writer")
    workflow.add_edge("writer", "editor")
    workflow.add_edge("editor", END)

    return workflow.compile()
