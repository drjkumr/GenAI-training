import os
import shutil
from typing import List, Dict, Any
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
import dotenv

dotenv.load_dotenv()

DB_DIR = "./chroma_db"
TEMP_PDF_DIR = "./temp_pdfs"

os.makedirs(TEMP_PDF_DIR, exist_ok=True)

# System prompt for clinical trial context
system_prompt = (
    "You are an expert Clinical Trial Assistant for site coordinators. "
    "Use the specific clinical trial protocol excerpts provided below to answer the user's question. "
    "If the answer is not contained in the provided protocol, say 'I cannot find the answer in the provided protocol document.' "
    "Do not hallucinate or use outside medical knowledge to answer questions about the specific trial's rules. "
    "\n\n"
    "Context:\n{context}"
)

qa_prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

class RAGService:
    def __init__(self):
        # We will initialize the LLM lazily in case the API key is not ready yet
        self.embeddings = None
        self.llm = None
        self.vectorstore = None
        self.retriever = None
        self.qa_chain = None
        self._initialized_llm = False

    def _ensure_llm(self):
        if not self._initialized_llm:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key or api_key == "your_openai_api_key_here":
                raise ValueError("OpenAI API Key not found in .env file.")
            
            self.embeddings = OpenAIEmbeddings()
            self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
            self._initialized_llm = True
            self._init_vectorstore()

    def _init_vectorstore(self):
        if os.path.exists(DB_DIR):
            self.vectorstore = Chroma(persist_directory=DB_DIR, embedding_function=self.embeddings)
            self._setup_chain()

    def _setup_chain(self):
        if self.vectorstore:
            self.retriever = self.vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
            document_chain = create_stuff_documents_chain(self.llm, qa_prompt)
            self.qa_chain = create_retrieval_chain(self.retriever, document_chain)

    def ingest_pdf(self, file_path: str, filename: str) -> int:
        """Processes a PDF, splits it, and ingests it into ChromaDB."""
        self._ensure_llm()
        loader = PyPDFLoader(file_path)
        docs = loader.load()

        # Add filename metadata
        for doc in docs:
            doc.metadata['source_file'] = filename

        # Keep context together for medical documents
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", ".", " ", ""]
        )
        splits = text_splitter.split_documents(docs)

        # Re-initialize DB from scratch for MVP simplicity
        if os.path.exists(DB_DIR):
            try:
                shutil.rmtree(DB_DIR)
            except Exception:
                pass # Windows file lock might prevent full deletion sometimes in dev

        self.vectorstore = Chroma.from_documents(
            documents=splits, 
            embedding=self.embeddings, 
            persist_directory=DB_DIR
        )
        self._setup_chain()
        return len(splits)

    def answer_question(self, question: str) -> Dict[str, Any]:
        """Answers a question using the RAG chain and returns citations."""
        self._ensure_llm()
        if not self.qa_chain:
            return {"answer": "Error: No protocol document has been uploaded yet.", "citations": []}

        response = self.qa_chain.invoke({"input": question})
        
        # Extract metadata for citations
        citations = []
        for doc in response.get("context", []):
            citations.append({
                "page": doc.metadata.get("page", "Unknown"),
                "source": doc.metadata.get("source_file", "Unknown"),
                "content": doc.page_content[:200] + "..." # snippet
            })

        return {
            "answer": response["answer"],
            "citations": citations
        }

# Singleton instance
rag_service = RAGService()
