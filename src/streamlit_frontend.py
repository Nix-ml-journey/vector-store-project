# Streamlit Frontend Demo
import streamlit as st
import requests
import json
from typing import List, Dict, Any, Optional
import pandas as pd
from config import (
    API_BASE_URL,
    Streamlit_page_title,
    Streamlit_page_icon,
    Streamlit_layout,
    Streamlit_initial_sidebar_state,
    DEFAULT_RESULTS_COUNT,
    MAX_RESULTS_COUNT,
    MIN_RESULTS_COUNT,
    Card_columns_ratio,
    Display_settings
)

# Configure the page
st.set_page_config(
    page_title=Streamlit_page_title,
    page_icon=Streamlit_page_icon,
    layout=Streamlit_layout,
    initial_sidebar_state=Streamlit_initial_sidebar_state
)

def make_api_request(endpoint: str, method: str = "GET", data: Optional[Dict] = None) -> Optional[Dict]:
    """Make API request to FastAPI backend"""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None

def display_book_card(book: Dict[str, Any], index: int):
    """Display a book in a card format"""
    with st.container():
        col1, col2 = st.columns(Card_columns_ratio)
        
        with col1:
            st.markdown(f"**{index + 1}.**")
        
        with col2:
            st.markdown(f"### {book.get('title', 'Unknown Title')}")
            st.markdown(f"**Author:** {book.get('author', 'Unknown Author')}")
            st.markdown(f"**Language:** {book.get('language', 'Unknown Language')}")
            
            if Display_settings["show_similarity_score"] and book.get('similarity_score'):
                st.markdown(f"**Similarity Score:** {book.get('similarity_score'):.4f}")
            
            if Display_settings["show_preview_expander"] and book.get('document_preview'):
                with st.expander("Full Content"):
                    st.text_area("Book Content", book.get('document_preview', ''), height=300)
            
            st.divider()

def main():
    # Header
    st.title("📚 Vector Store Book Search")
    st.markdown("Search through thousands of books using semantic similarity")
    
    # Sidebar
    with st.sidebar:
        st.header("🔍 Search Options")
        
        # Search type selection
        search_type = st.selectbox(
            "Search Type",
            ["Text Search", "Author Search", "Language Search", "Advanced Search"]
        )
        
        # Number of results
        n_results = st.slider("Number of Results", MIN_RESULTS_COUNT, MAX_RESULTS_COUNT, DEFAULT_RESULTS_COUNT)
        
        # Collection stats
        if Display_settings["show_collection_stats"]:
            st.header("📊 Collection Statistics")
            stats = make_api_request("/stats")
            if stats:
                st.metric("Total Books", stats.get('total_books', 0))
                st.info(f"Collection: {stats.get('collection_name', 'Unknown')}")
    
    # Main content area
    if search_type == "Text Search":
        st.header("🔍 Text Search")
        
        # Search form
        with st.form("text_search_form"):
            query = st.text_input("Enter your search query", placeholder="e.g., adventure, love, mystery")
            submitted = st.form_submit_button("Search")
            
            if submitted and query:
                with st.spinner("Searching..."):
                    response = make_api_request("/search", method="POST", data={
                        "query": query,
                        "n_results": n_results
                    })
                    
                    if response:
                        st.success(f"Found {response.get('total_found', 0)} results for '{query}'")
                        
                        for i, book in enumerate(response.get('results', [])):
                            display_book_card(book, i)
    
    elif search_type == "Author Search":
        st.header("👤 Author Search")
        
        with st.form("author_search_form"):
            author = st.text_input("Enter author name", placeholder="e.g., Mark Twain, Shakespeare")
            submitted = st.form_submit_button("Search")
            
            if submitted and author:
                with st.spinner("Searching..."):
                    response = make_api_request(f"/search/author/{author}?n_results={n_results}")
                    
                    if response:
                        st.success(f"Found {response.get('total_found', 0)} books by '{author}'")
                        
                        for i, book in enumerate(response.get('results', [])):
                            display_book_card(book, i)
    
    elif search_type == "Language Search":
        st.header("🌍 Language Search")
        
        with st.form("language_search_form"):
            language = st.text_input("Enter language", placeholder="e.g., English, French, Spanish")
            submitted = st.form_submit_button("Search")
            
            if submitted and language:
                with st.spinner("Searching..."):
                    response = make_api_request(f"/search/language/{language}?n_results={n_results}")
                    
                    if response:
                        st.success(f"Found {response.get('total_found', 0)} books in '{language}'")
                        
                        for i, book in enumerate(response.get('results', [])):
                            display_book_card(book, i)
    
    elif search_type == "Advanced Search":
        st.header("⚙️ Advanced Search")
        
        with st.form("advanced_search_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                query = st.text_input("Search query", placeholder="e.g., adventure")
                author = st.text_input("Author (optional)", placeholder="e.g., Mark Twain")
            
            with col2:
                language = st.text_input("Language (optional)", placeholder="e.g., English")
            
            submitted = st.form_submit_button("Search")
            
            if submitted and query:
                with st.spinner("Searching..."):
                    response = make_api_request("/search", method="POST", data={
                        "query": query,
                        "n_results": n_results,
                        "author": author if author else None,
                        "language": language if language else None
                    })
                    
                    if response:
                        st.success(f"Found {response.get('total_found', 0)} results")
                        
                        for i, book in enumerate(response.get('results', [])):
                            display_book_card(book, i)
    
    # Book details section
    st.header("📖 Book Details")
    book_id = st.text_input("Enter Book ID to view details", placeholder="e.g., doc_0")
    
    if book_id:
        with st.spinner("Loading book details..."):
            book = make_api_request(f"/book/{book_id}")
            
            if book:
                st.markdown(f"### {book.get('title', 'Unknown Title')}")
                st.markdown(f"**Author:** {book.get('author', 'Unknown Author')}")
                st.markdown(f"**Language:** {book.get('language', 'Unknown Language')}")
                st.markdown(f"**Book ID:** {book.get('bookno', 'Unknown')}")
                
                with st.expander("Full Content"):
                    st.text_area("Book Content", book.get('document_preview', ''), height=400)
            else:
                st.error("Book not found")
    
    # API Documentation
    with st.expander("📚 API Documentation"):
        st.markdown("""
        ### Available Endpoints:
        
        - `POST /search` - Search books by text
        - `GET /search/author/{author}` - Search by author
        - `GET /search/language/{language}` - Search by language
        - `GET /book/{book_id}` - Get book details
        - `GET /stats` - Get collection statistics
        
        ### Example Usage:
        ```python
        # Search for books
        response = requests.post("http://localhost:8000/search", 
                               json={"query": "adventure", "n_results": 5})
        
        # Get book details
        book = requests.get("http://localhost:8000/book/doc_0")
        ```
        """)

if __name__ == "__main__":
    main() 