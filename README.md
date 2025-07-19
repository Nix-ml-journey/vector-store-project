# 📚 Vector Store Book Search

A powerful semantic search engine for books using ChromaDB and Sentence Transformers. Search through thousands of books using natural language queries.

## 🌟 Features

- **Semantic Search**: Find books using natural language queries
- **Multiple Search Types**: Text, Author, Language, and Advanced search
- **Real-time Results**: Fast search with instant results
- **Book Content Display**: View full book content in the interface
- **RESTful API**: Complete FastAPI backend
- **Modern UI**: Beautiful Streamlit frontend
- **Scalable**: Handles large datasets efficiently

## 🏗️ Architecture

```
Vector-Store/
├── src/                    # Main application code
│   ├── app.py             # FastAPI backend
│   ├── streamlit_frontend.py  # Streamlit UI
│   ├── search_engine.py   # Search logic
│   ├── vector_store.py    # ChromaDB integration
│   ├── data_loader.py     # Data processing
│   ├── embedding_generation.py  # Embedding creation
│   └── config.py          # Configuration
├── Data/                  # Data files
│   ├── db_books.csv       # Book metadata
│   └── stories.csv        # Book content
├── requirements.txt        # Python dependencies
└── README.md             # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Vector-Store
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Generate embeddings** (First time only)
   ```bash
   cd src
   python embedding_generation.py
   ```

## 🎯 Usage

### Terminal 1: Start the API Backend
```bash
cd src
python app.py
```
The API will be available at `http://localhost:8000`

### Terminal 2: Start the Web Interface
```bash
cd src
streamlit run streamlit_frontend.py
```
The web interface will open at `http://localhost:8501`

## 🔍 How to Use

### Web Interface
1. Open your browser to `http://localhost:8501`
2. Choose search type:
   - **Text Search**: Search by keywords or phrases
   - **Author Search**: Find books by specific authors
   - **Language Search**: Filter by language
   - **Advanced Search**: Combine multiple criteria
3. Enter your query and click "Search"
4. View results with book details and content

### API Usage
```bash
# Search for books
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "adventure", "n_results": 5}'

# Get collection stats
curl "http://localhost:8000/stats"

# Search by author
curl "http://localhost:8000/search/author/Mark%20Twain?n_results=3"
```

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/search` | POST | Text-based search |
| `/search/author/{author}` | GET | Search by author |
| `/search/language/{language}` | GET | Search by language |
| `/search/advanced` | GET | Advanced search |
| `/book/{book_id}` | GET | Get book details |
| `/stats` | GET | Collection statistics |

## 🛠️ Configuration

Edit `src/config.py` to customize:

```python
# Search settings
DEFAULT_RESULTS_COUNT = 5
MAX_RESULTS_COUNT = 20
MIN_RESULTS_COUNT = 1

# UI settings
Streamlit_page_title = "Vector Store Book Search"
API_BASE_URL = "http://localhost:8000"
```

## 📁 Project Structure

```
src/
├── app.py                 # FastAPI backend server
├── streamlit_frontend.py  # Streamlit web interface
├── search_engine.py       # Search engine logic
├── vector_store.py        # ChromaDB vector store
├── data_loader.py         # Data loading and cleaning
├── embedding_generation.py # Embedding generation
├── config.py             # Configuration settings
└── chroma_db/           # ChromaDB database files
```

## 🔧 Development

### Adding New Books
1. Add book metadata to `Data/db_books.csv`
2. Add book content to `Data/stories.csv`
3. Run `python embedding_generation.py` to regenerate embeddings

### Customizing Search
- Modify `search_engine.py` for search logic changes
- Edit `vector_store.py` for ChromaDB configuration
- Update `data_loader.py` for data processing changes

### Styling the UI
- Edit `streamlit_frontend.py` for UI changes
- Modify `config.py` for display settings

## 🐛 Troubleshooting

### Common Issues

**1. Port already in use**
```bash
# Kill existing processes
pkill -f "python app.py"
pkill -f "streamlit"
```

**2. ChromaDB collection not found**
```bash
# Regenerate embeddings
python embedding_generation.py
```

**3. Memory issues with large datasets**
- Reduce `CHUNK_SIZE` in `config.py`
- Use smaller embedding models

**4. Search returns few results**
- Try broader search terms
- Check if embeddings were generated correctly

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
python app.py
```

## 📈 Performance

- **Search Speed**: ~100ms per query
- **Memory Usage**: ~2GB for 1000 books
- **Storage**: ~500MB for embeddings
- **Concurrent Users**: 10+ simultaneous searches

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [ChromaDB](https://www.trychroma.com/) for vector storage
- [Sentence Transformers](https://www.sbert.net/) for embeddings
- [FastAPI](https://fastapi.tiangolo.com/) for the API
- [Streamlit](https://streamlit.io/) for the UI

## 📞 Support

If you encounter any issues:
1. Check the troubleshooting section
2. Review the logs in the terminal
3. Open an issue on GitHub

---

**Happy Searching! 📚✨**
