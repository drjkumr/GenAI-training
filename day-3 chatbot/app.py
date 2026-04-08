import streamlit as st
import os
from chatbot_engine import user_message, assistant_message, chat

# PAGE CONFIG
st.set_page_config(page_title="ABC South Indian Chatbot", page_icon="🍛")

# CUSTOM STYLING (Yellow Theme)
st.markdown("""
    <style>
    .stApp {
        background-color: #e6a50e;
    }
    .user-bubble {
        background-color: #FBC02D;
        color: black;
        padding: 10px 15px;
        border-radius: 20px 20px 0px 20px;
        margin-bottom: 10px;
        display: inline-block;
        float: right;
        clear: both;
        max-width: 80%;
    }
    .bot-bubble {
        background-color: #FFF9C4;
        color: black;
        padding: 10px 15px;
        border-radius: 20px 20px 20px 0px;
        margin-bottom: 10px;
        display: inline-block;
        float: left;
        clear: both;
        border: 1px solid #FDD835;
        max-width: 80%;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
    }
    </style>
""", unsafe_allow_html=True)

from graph_engine import chatbot_graph

# LOAD DATA
def load_text(filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    return ""

knowledge_base = load_text("rag_knowledge_base.txt")

# SESSION STATE
if "messages" not in st.session_state:
    st.session_state.messages = [] # For rendering
if "context" not in st.session_state:
    st.session_state.context = [] # For Chatbot API

st.title("🍛 ABC South Indian Restaurant")
st.subheader("Your AI Waiter")

# DISPLAY CHAT HISTORY
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# USER INPUT
user_input = st.chat_input("Ask me about our menu, hours, or give us a suggestion!")

if user_input:
    # 1. Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    user_message(st.session_state.context, user_input)
    
    # Rerender to show user message immediately
    st.rerun()

# GENERATE RESPONSE
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.spinner("Processing request..."):
        # Invoke the LangGraph workflow
        initial_state = {
            "messages": st.session_state.messages,
            "context": st.session_state.context,
            "knowledge_base": knowledge_base
        }
        
        final_state = chatbot_graph.invoke(initial_state)
        response = final_state.get("response", "I'm sorry, I couldn't process that.")
        
        # 5. Add assistant message to history
        st.session_state.messages.append({"role": "assistant", "content": response})
        assistant_message(st.session_state.context, response)
        
        # Rerun to show bot message
        st.rerun()
