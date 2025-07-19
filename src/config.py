
CSV_PATH1 = '/home/user/my_env/VectorStore/Vector-Store/Data/db_books.csv'
CSV_PATH2 = '/home/user/my_env/VectorStore/Vector-Store/Data/stories.csv'

#ChromaDB
Chroma_db_path = '/home/user/my_env/VectorStore/Vector-Store/Data/chroma_db'
Chroma_collection_name = 'books_story'
Chroma_embedding_path = '/home/user/my_env/VectorStore/Vector-Store/Data/embeddings.npy'

#Streamlit Ui
Streamlit_page_title = "Vector Store Book Search"
Streamlit_page_icon = "📚"
Streamlit_layout = "wide"
Streamlit_initial_sidebar_state = "expanded"

#Search Settings
DEFAULT_RESULTS_COUNT = 5
MAX_RESULTS_COUNT = 20
MIN_RESULTS_COUNT = 1

#UI Layout Settings
Card_columns_ratio = [1,3]
Book_display_columns = ['title', 'author', 'language', 'similarity_score', 'document_preview']
Display_settings = {
    "show_similarity_score": True,
    "show_preview_expander": True,
    "show_collection_stats": True,
    "sidebar_width": 300,
    "main_content_padding": 20,
    "card_columns_ratio": [1,3],
    "card_width": 300,
    "card_height": 200,
    "card_padding": 10,
    "card_border_radius": 10,
    "card_border_color": "#e0e0e0",
    "card_background_color": "#f0f0f0",
    "card_text_color": "#333333",
    "card_font_size": 14,
    "card_font_family": "Arial, sans-serif"
}

#API Configuration 
API_BASE_URL= "http://localhost:8000"
API_TIMEOUT = 30

#Data Processing Settings 
CHUNK_SIZE = 1000
MAX_MEMORY_USAGE = 1024
CLEAN_CONTENT = True
REMOVE_GUTENBERG_HEADERS = True