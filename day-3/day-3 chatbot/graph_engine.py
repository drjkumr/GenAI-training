from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from chatbot_engine import chat, user_message, assistant_message
import os

# Define the state object
class AgentState(TypedDict):
    messages: List[dict] # Full history for UI
    context: List[dict]  # Context for the API
    category: str        # 'support' or 'suggestion'
    response: str        # Final bot response
    knowledge_base: str  # Content for RAG

import chromadb
from chromadb.utils import embedding_functions
import os

# Initialize ChromaDB (Ephemeral for this session)
chroma_client = chromadb.Client()
# Add a default embedding function (ONNX based, lightweight)
default_ef = embedding_functions.DefaultEmbeddingFunction()
collection = chroma_client.create_collection(name="restaurant_kb", embedding_function=default_ef)

def index_kb(kb_text):
    """Index the knowledge base into ChromaDB."""
    # Split by double newline to get logical blocks (menu, FAQs, etc.)
    chunks = [c.strip() for c in kb_text.split("\n\n") if c.strip()]
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    
    # Clear existing if any (for fresh start)
    existing_count = collection.count()
    if existing_count > 0:
        # In this simple setup we don't need to delete, but for persistence we would
        pass
    
    collection.add(
        documents=chunks,
        ids=ids
    )

# Load and index once on startup
if os.path.exists("rag_knowledge_base.txt"):
    with open("rag_knowledge_base.txt", "r", encoding="utf-8") as f:
        kb_content = f.read()
        index_kb(kb_content)

def router_node(state: AgentState):
    """Categorize the user's request."""
    user_input = state['messages'][-1]['content']
    
    prompt = f"""Categorize the following user request into exactly one of these categories: 'support' or 'suggestion'.
    - 'support': Questions about the menu, opening hours, location, spicy levels, etc.
    - 'suggestion': Suggestions for new food items, drinks, or changes to the restaurant.
    
    Request: {user_input}
    
    Response only with the category name."""
    
    category = chat([{"role": "user", "content": prompt}], system="You are a routing assistant.")
    category = category.strip().lower()
    
    if 'suggestion' in category:
        return {"category": "suggestion"}
    return {"category": "support"}

def support_node(state: AgentState):
    """Handle general support using Semantic RAG."""
    user_input = state['messages'][-1]['content']
    
    # Semantic Search in ChromaDB
    results = collection.query(
        query_texts=[user_input],
        n_results=3 # Get top 3 most relevant chunks
    )
    
    retrieved_docs = results['documents'][0]
    context_str = "\n\n".join(retrieved_docs)
    
    kb = state['knowledge_base']
    system_prompt = f"You are a helpful waiter at ABC South Indian Restaurant. Use the following context to answer.\n\nContext:\n{context_str}\n\nFull Knowledge Base for reference:\n{kb}"
    
    # Generate response
    response = chat(state['context'], system=system_prompt)
    return {"response": response}

def suggestion_node(state: AgentState):
    """Handle menu suggestions and log them."""
    user_input = state['messages'][-1]['content']
    
    # Log the suggestion to a file
    with open("menu_suggestions.txt", "a", encoding="utf-8") as f:
        f.write(f"USER: {user_input}\n---\n")
    
    response = "Thank you so much for your suggestion! 📝 We're always looking to improve our menu at ABC South Indian. I've shared your idea with our kitchen staff. Would you like to order something from our current menu while we consider that?"
    return {"response": response}

# Define the Routing Logic
def route_request(state: AgentState):
    if state['category'] == 'suggestion':
        return 'suggestion'
    return 'support'

# Build the Graph
workflow = StateGraph(AgentState)

workflow.add_node("router", router_node)
workflow.add_node("support_handler", support_node)
workflow.add_node("suggestion_handler", suggestion_node)

workflow.set_entry_point("router")

workflow.add_conditional_edges(
    "router",
    route_request,
    {
        "support": "support_handler",
        "suggestion": "suggestion_handler"
    }
)

workflow.add_edge("support_handler", END)
workflow.add_edge("suggestion_handler", END)

# Compile the graph
chatbot_graph = workflow.compile()
