# server.py - Research Assistant MCP Server with ChromaDB
# uv add chromadb langchain-chroma langchain-ollama

from fastmcp import FastMCP
from pathlib import Path
from typing import List, Set, Dict, Any, Optional
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import shutil
import hashlib
import json
import io
import PyPDF2
import docx2txt

from dotenv import load_dotenv
load_dotenv()

# Initialize MCP Server
mcp = FastMCP("Research Assistant")

# Configuration Defaults
DEFAULT_LLM_PROVIDER = "ollama"
DEFAULT_OLLAMA_URL = "http://localhost:11434"
DEFAULT_OLLAMA_EMBED = "nomic-embed-text"
DEFAULT_OLLAMA_CHAT = "llama3.2"

def get_config(overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Get configuration from env vars or overrides."""
    env = os.environ.copy()
    if overrides:
        env.update(overrides)
        
    return {
        "RESEARCH_DB_PATH": env.get("RESEARCH_DB_PATH"),
        "LLM_PROVIDER": env.get("LLM_PROVIDER", DEFAULT_LLM_PROVIDER).lower(),
        "OLLAMA_BASE_URL": env.get("OLLAMA_BASE_URL", DEFAULT_OLLAMA_URL),
        "OLLAMA_EMBED_MODEL": env.get("OLLAMA_EMBED_MODEL", DEFAULT_OLLAMA_EMBED),
        "OLLAMA_CHAT_MODEL": env.get("OLLAMA_CHAT_MODEL", DEFAULT_OLLAMA_CHAT),
        "OPENAI_API_KEY": env.get("OPENAI_API_KEY"),
    }

def get_db_path(config: Optional[Dict[str, Any]] = None) -> Path:
    """Get the database root path."""
    cfg = get_config(config)
    path_str = cfg.get("RESEARCH_DB_PATH")
    if not path_str:
        # Fallback for UI ease-of-use if not set
        return Path.home() / ".kavi_research_db"
    return Path(path_str) / "research_chroma_dbs"

def get_embeddings(config: Optional[Dict[str, Any]] = None):
    """Get embeddings model based on configuration."""
    cfg = get_config(config)
    provider = cfg["LLM_PROVIDER"]
    
    if provider == "ollama":
        return OllamaEmbeddings(
            model=cfg["OLLAMA_EMBED_MODEL"],
            base_url=cfg["OLLAMA_BASE_URL"]
        )
    else:
        # Default to OpenAI
        return OpenAIEmbeddings(model="text-embedding-3-small", api_key=cfg.get("OPENAI_API_KEY"))

def get_llm(config: Optional[Dict[str, Any]] = None):
    """Get Chat Model based on configuration."""
    cfg = get_config(config)
    provider = cfg["LLM_PROVIDER"]
    
    if provider == "ollama":
        return ChatOllama(
            model=cfg["OLLAMA_CHAT_MODEL"],
            base_url=cfg["OLLAMA_BASE_URL"],
            temperature=0
        )
    else:
        return ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            api_key=cfg.get("OPENAI_API_KEY")
        )

def get_content_hash(content: str) -> str:
    """Generate a hash for content to check for duplicates."""
    return hashlib.md5(content.encode('utf-8')).hexdigest()

def load_content_hashes(topic_path: Path) -> Set[str]:
    """Load existing content hashes from metadata file."""
    metadata_file = topic_path / "content_hashes.json"
    if metadata_file.exists():
        try:
            with open(metadata_file, 'r') as f:
                return set(json.load(f))
        except:
            return set()
    return set()

def save_content_hashes(topic_path: Path, hashes: Set[str]):
    """Save content hashes to metadata file."""
    metadata_file = topic_path / "content_hashes.json"
    with open(metadata_file, 'w') as f:
        json.dump(list(hashes), f)

def get_vectorstore(topic: str, config: Optional[Dict[str, Any]] = None) -> Chroma:
    """Get or create a ChromaDB vectorstore for a topic."""
    root_path = get_db_path(config)
    topic_path = root_path / topic
    topic_path.mkdir(parents=True, exist_ok=True)
    
    return Chroma(
        persist_directory=str(topic_path),
        embedding_function=get_embeddings(config),
        collection_name=f"research_{topic}"
    )

def parse_file(file_path: Path) -> str:
    """Extract text from supported file formats."""
    ext = file_path.suffix.lower()
    
    try:
        if ext == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        elif ext == ".pdf":
            text = ""
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            return text
        elif ext == ".docx":
            import docx2txt
            return docx2txt.process(str(file_path))
        else:
            return f"Unsupported file extension: {ext}"
    except Exception as e:
        return f"Error parsing {file_path.name}: {str(e)}"

# === Tools ===


# logic functions
def save_research_data_logic(content: List[str], topic: str = "default", config: Optional[Dict[str, Any]] = None) -> str:
    try:
        topic = topic.replace(' ', '_')
        root_path = get_db_path(config)
        topic_path = root_path / topic
        topic_path.mkdir(parents=True, exist_ok=True)
        
        # Load existing content hashes
        existing_hashes = load_content_hashes(topic_path)
        
        # Filter out duplicate content
        new_content = []
        new_hashes = set(existing_hashes)
        
        for text in content:
            content_hash = get_content_hash(text)
            if content_hash not in existing_hashes:
                new_content.append(text)
                new_hashes.add(content_hash)
        
        if not new_content:
            return f"No new content to save - all {len(content)} documents already exist in topic: {topic}"
        
        # Get vectorstore for this topic
        vectorstore = get_vectorstore(topic, config)
        
        # Initialize text splitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=600,
            chunk_overlap=50,
            length_function=len,
        )
        
        # Create documents with metadata
        documents = []
        doc_ids = []
        
        for text in new_content:
            content_hash = get_content_hash(text)
            chunks = text_splitter.split_text(text)
            
            for i, chunk in enumerate(chunks):
                doc_id = f"{topic}_{content_hash}_{i}"
                doc = Document(
                    page_content=chunk,
                    metadata={
                        "topic": topic,
                        "content_hash": content_hash,
                        "chunk_index": i,
                        "total_chunks": len(chunks)
                    }
                )
                documents.append(doc)
                doc_ids.append(doc_id)
        
        # Add documents/chunks to vectorstore in batches
        if documents:
            # Batching to avoid context limits in some embedding models/Ollama
            batch_size = 10
            for i in range(0, len(documents), batch_size):
                batch_docs = documents[i : i + batch_size]
                batch_ids = doc_ids[i : i + batch_size]
                vectorstore.add_documents(documents=batch_docs, ids=batch_ids)
        
        # Save updated content hashes
        save_content_hashes(topic_path, new_hashes)
        
        return f"Successfully processed {len(new_content)} documents into {len(documents)} chunks for topic: {topic} (skipped {len(content) - len(new_content)} duplicates)"
        
    except Exception as e:
        error_msg = str(e)
        if "model" in error_msg and "not found" in error_msg:
             return f"❌ Error: Model not found. The embedding model is missing.\n👉 Please run this command in your terminal:\n\n   ollama pull {config.get('OLLAMA_EMBED_MODEL', 'nomic-embed-text')}"
        return f"Error saving research data: {error_msg}"

@mcp.tool()
def save_research_data(content: List[str], topic: str = "default") -> str:
    """
    Save research content to vector database for future retrieval.
    Args:
        content: List of text content to save
        topic: Topic name for organizing the data (creates separate DB)
    """
    return save_research_data_logic(content, topic)

def save_research_files_logic(file_paths: List[str], topic: str = "default", config: Optional[Dict[str, Any]] = None) -> str:
    """
    Logic to parse and save text from files.
    """
    contents = []
    for path_str in file_paths:
        path = Path(path_str)
        if not path.exists():
            continue
        
        text = parse_file(path)
        if text.startswith("Error"):
            return text
        contents.append(text)
    
    if not contents:
        return "No valid files provided or files were empty."
        
    return save_research_data_logic(contents, topic, config=config)

@mcp.tool()
def save_research_files(file_paths: List[str], topic: str = "default") -> str:
    """
    Parse and save text from files (.pdf, .txt, .docx) to vector database.
    Args:
        file_paths: List of absolute paths to files
        topic: Topic name for organizing the data
    """
    return save_research_files_logic(file_paths, topic)

@mcp.tool()
def search_research_data(query: str, topic: str = "default", max_results: int = 5) -> str:
    """
    Search through saved research data using semantic similarity.
    Args:
        query: Search query
        topic: Topic database to search in
        max_results: Maximum number of results to return
    """
    try:
        topic_path = CHROMA_DB_ROOT / topic
        
        if not topic_path.exists():
            return f"No research data found for topic: {topic}"
        
        # Get vectorstore for this topic
        vectorstore = get_vectorstore(topic)
        
        # Check if collection has any documents
        try:
            collection = vectorstore._collection
            count = collection.count()
            if count == 0:
                return f"No documents found in topic: {topic}"
        except:
            return f"No research data found for topic: {topic}"
        
        # Search for similar documents
        results = vectorstore.similarity_search_with_score(query, k=max_results)
        
        if not results:
            return f"No relevant results found for query: '{query}' in topic: {topic}"
        
        # Format results
        formatted_results = []
        for i, (doc, score) in enumerate(results):
            similarity = 1 - score  # Convert distance to similarity
            result_text = f"Result {i+1} (Similarity: {similarity:.3f}):\n{doc.page_content}\n"
            formatted_results.append(result_text)
        
        return "\n" + "="*50 + "\n".join(formatted_results) + "="*50
        
    except Exception as e:
        return f"Error searching research data: {str(e)}"


def list_research_topics_logic(config: Optional[Dict[str, Any]] = None) -> str:
    try:
        root_path = get_db_path(config)
        if not root_path.exists():
            return "No research topics found"
        
        topics = []
        for path in root_path.iterdir():
            if path.is_dir():
                # Try to get document count from ChromaDB
                try:
                    vectorstore = get_vectorstore(path.name, config)
                    collection = vectorstore._collection
                    doc_count = collection.count()
                    topics.append(f"Topic: {path.name} ({doc_count} documents)")
                except Exception as e:
                    # Fallback to hash count if ChromaDB fails
                    try:
                        hashes = load_content_hashes(path)
                        doc_count = len(hashes)
                        topics.append(f"Topic: {path.name} ({doc_count} documents)")
                    except:
                        topics.append(f"Topic: {path.name}")
        
        if not topics:
            return "No research topics found"
        
        return "\n".join(topics)
        
    except Exception as e:
        return f"Error listing topics: {str(e)}"

@mcp.tool()
def list_research_topics() -> str:
    """
    List all available research topics (vector databases).
    """
    return list_research_topics_logic()

@mcp.tool()
def delete_research_topic(topic: str) -> str:
    """
    Delete a research topic and all its data.
    Args:
        topic: Topic name to delete
    """
    try:
        root_path = get_db_path()
        topic_path = root_path / topic
        
        if not topic_path.exists():
            return f"Topic '{topic}' does not exist"
        
        # Try to delete the ChromaDB collection first
        try:
            vectorstore = get_vectorstore(topic)
            vectorstore.delete_collection()
        except:
            pass  # Continue even if collection deletion fails
        
        # Remove the entire directory
        shutil.rmtree(topic_path)
        
        return f"Successfully deleted topic: {topic}"
        
    except Exception as e:
        return f"Error deleting topic: {str(e)}"

@mcp.tool()
def get_topic_info(topic: str) -> str:
    """
    Get detailed information about a research topic.
    Args:
        topic: Topic name to get info for
    """
    try:
        root_path = get_db_path()
        topic_path = root_path / topic
        
        if not topic_path.exists():
            return f"Topic '{topic}' does not exist"
        
        # Get vectorstore info
        vectorstore = get_vectorstore(topic)
        collection = vectorstore._collection
        doc_count = collection.count()
        
        # Get content hashes info
        hashes = load_content_hashes(topic_path)
        hash_count = len(hashes)
        
        info = f"""Topic Information: {topic}
                - ChromaDB Collection: research_{topic}
                - Document Count: {doc_count}
                - Hash Records: {hash_count}
                - Database Path: {topic_path}
                - Ollama URL: OpenAI API"""
        
        return info
        
    except Exception as e:
        return f"Error getting topic info: {str(e)}"


def ask_research_topic_logic(query: str, topic: str = "default", config: Optional[Dict[str, Any]] = None) -> str:
    try:
        root_path = get_db_path(config)
        topic_path = root_path / topic
        if not topic_path.exists():
            return f"Topic '{topic}' does not exist. Please save some research data first."

        # 1. Retrieve context
        vectorstore = get_vectorstore(topic, config)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
        
        # 2. Setup RAG chain
        llm = get_llm(config)
        
        template = """Answer the question based only on the following context:
        {context}

        Question: {question}
        
        Answer (if not in context, say so):"""
        
        prompt = ChatPromptTemplate.from_template(template)
        
        def format_docs(docs):
            return "\n\n".join([d.page_content for d in docs])

        chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        
        # 3. Invoke
        response = chain.invoke(query)
        return response

    except Exception as e:
        return f"Error asking research topic: {str(e)}"

@mcp.tool()
def ask_research_topic(query: str, topic: str = "default") -> str:
    """
    Ask a question about a specific research topic (RAG).
    The agent will search the topic database and use an LLM to answer.
    Args:
        query: Your question
        topic: Topic to ask about
    """
    return ask_research_topic_logic(query, topic)


def summarize_topic_logic(topic: str = "default", config: Optional[Dict[str, Any]] = None) -> str:
    try:
        root_path = get_db_path(config)
        topic_path = root_path / topic
        if not topic_path.exists():
            return f"Topic '{topic}' does not exist."

        vectorstore = get_vectorstore(topic, config)
        results = vectorstore.similarity_search("overview summary main concepts important facts", k=10)
        
        if not results:
            return "Not enough content to summarize."

        context_text = "\n\n".join([d.page_content for d in results])

        # 2. Summarize with LLM
        llm = get_llm(config)
        
        template = """You are a research assistant. Summarize the following research notes into a concise overview:
        
        {context}
        
        Summary:"""
        
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | llm | StrOutputParser()
        
        response = chain.invoke({"context": context_text})
        return f"Summary of '{topic}':\n\n{response}"

    except Exception as e:
        return f"Error summarizing topic: {str(e)}"

@mcp.tool()
def summarize_topic(topic: str = "default") -> str:
    """
    Generate a summary of the stored research for a topic.
    Args:
        topic: Topic to summarize
    """
    return summarize_topic_logic(topic)

def main():
    """Main entry point for the Research Assistant MCP server."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()