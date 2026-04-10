import os
import re
from typing import List, Dict, Any
import docx
from pypdf import PdfReader
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

load_dotenv()

# Setup ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")
# Using OpenAI Default Embedding if API Key is present, otherwise fallback to basic
openai_ef = None
if os.getenv("OPENAI_API_KEY"):
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name="text-embedding-3-small"
    )
else:
    # Use a default or inform the user
    openai_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

collection = client.get_or_create_collection(name="resumes", embedding_function=openai_ef)

def parse_resume(file_path: str) -> str:
    """Parses text from PDF, DOCX, or TXT files."""
    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    
    if ext == ".pdf":
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    elif ext == ".docx":
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
    elif ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    
    return text.strip()

def load_screenings(file_path: str = "screenings.txt") -> List[Dict[str, Any]]:
    """Parses the screenings.txt file into a structured list of roles."""
    if not os.path.exists(file_path):
        return []
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    roles = []
    # Split by empty lines which separate roles
    role_blocks = re.split(r'\n\s*\n', content.strip())
    
    for block in role_blocks:
        role_data = {}
        lines = block.strip().split('\n')
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                role_data[key.strip()] = value.strip()
        if role_data:
            roles.append(role_data)
            
    return roles

def add_resume_to_db(resume_id: str, text: str, metadata: Dict[str, Any]):
    """Adds a resume to ChromaDB."""
    collection.add(
        documents=[text],
        metadatas=[metadata],
        ids=[resume_id]
    )

def search_resumes(query: str, n_results: int = 5):
    """Semantic search in ChromaDB."""
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results
