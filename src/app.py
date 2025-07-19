import logging 
from typing import List, Dict, Optional, Any
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from search_engine import SearchEngine
import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Vector Store Search API",
    description="API FOR SEARCHING BOOKS IN THE 1002 BOOKS VECTOR STORE",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
)

search_engine = SearchEngine()

class SearchRequest(BaseModel):
    query:str
    n_results:int = 5
    author:Optional[str] = None
    language:Optional[str] = None

class BookResponse(BaseModel):
    id:Optional[str] = None
    title:Optional[str] = None
    author:Optional[str] = None
    language:Optional[str] = None
    similarity_score:Optional[float] = None
    document_preview:str

class SearchResponse(BaseModel):
    results:List[BookResponse]
    total_found:int
    query:str

class CollectionStats(BaseModel):
    total_books:int 
    collection_name:str
    database_path:str

@app.get("/",tags=["Root"])
async def root (): 
    """Root endpoint with API information"""
    return{
        "message": "Vector Store Search API",
        "version": "1.0.0",
        "endpoints":{
            "/search": "Search books by text",
            "/search/author": "Search books by author",
            "/search/language": "Search books by language",
            "/search/advanced": "Advanced search with filters",
            "/book/{book_id}": "Get book details by ID",
            "/stats": "Get collection statistics"
            }    
        }

@app.post("/search", response_model=SearchResponse, tags=["Search"])
async def search_books(request:SearchRequest):

    try:
        logger.info(f"Search request: {request.query}")

        if request.author or request.language:
            results = search_engine.advanced_search(
                query=request.query,
                author=request.author,
                language=request.language,
                n_results=request.n_results
            )
        else:
            results = search_engine.search_books(request.query, request.n_results)

        book_responses = []
        for result in results:
            book_responses.append(BookResponse(
                id=result.get('id'),
                title=result.get('title', 'Unknown Title'),
                author=result.get('author', 'Unknown Author'),
                language=result.get('language', 'Unknown Language'),
                similarity_score=result.get('similarity_score'),
                document_preview=result.get('document_preview', '')
            ))

        return SearchResponse(
            results=book_responses,
            total_found=len(book_responses),
            query=request.query
        )

    except Exception as e:
        logger.error(f"Error in search: {e}")
        raise HTTPException(status_code=500, detail="Search error: {str(e)}")

@app.get("/search/author/{author}", response_model=SearchResponse, tags=["Search"])
async def search_by_author(
    author:str,
    n_results:int = Query(default=5, ge=1, le=50)
):
    try:
        logger.info(f"Author search request:{author}")
        results = search_engine.search_by_author(author, n_results)

        book_responses = []

        for result in results:
            book_responses.append(BookResponse(
                id=result.get('id'),
                title=result.get('title', 'Unknown Title'),
                author=result.get('author', 'Unknown Author'),
                language=result.get('language', 'Unknown Language'),
                similarity_score=result.get('similarity_score'),
                document_preview=result.get('document_preview', '')
            ))

        return SearchResponse(
            results=book_responses,
            total_found=len(book_responses),
            query=f"author:{author}"
        )

    except Exception as e:
        logger.error(f"Error in author search: {e}")
        raise HTTPException(status_code = 500, detail=f"Author search error: {str (e)}")

@app.get("/search/language/{language}", response_model = SearchResponse, tags=["Search"])
async def search_by_language(
    language:str,
    n_results:int = Query(default=5, ge=1, le=50)
):

    try:
        logger.info(f"Language search request: {language}")
        results = search_engine.search_by_language(language, n_results)

        book_responses = []

        for result in results:
            book_responses.append(BookResponse(
                id=result.get('id'),
                title=result.get('title', 'Unknown Title'),
                author=result.get('author', 'Unknown Author'),
                language=result.get('language', 'Unknown Language'),
                similarity_score=result.get('similarity_score'),
                document_preview=result.get('document_preview', '')
            ))

        return SearchResponse(
            results=book_responses,
            total_found=len(book_responses),
            query=f"language:{language}"
        )

    except Exception as e:
        logger.error(f"Error in language search: {e}")
        raise HTTPException(status_code=500, detail=f"Language search error: {str(e)}")
    
@app.get("/search/advanced", response_model=SearchResponse, tags=["Search"])
async def advanced_search(
    query:str,
    author:Optional[str] = None,
    language:Optional[str] = None,
    n_results:int = Query(default=5, ge=1, le=50)
):

    try:
        logger.info(f"Advanced search request: {query}")
        results = search_engine.advanced_search(
            query=query,
            author=author,
            language=language,
            n_results=n_results
        )
    
        book_responses = []
        for result in results:
            book_responses.append(BookResponse(
                id=result.get('id'),
                title=result.get('title', 'Unknown Title'),
                author=result.get('author', 'Unknown Author'),
                language=result.get('language', 'Unknown Language'),
                similarity_score=result.get('similarity_score'),
                document_preview=result.get('document_preview', '')
            ))

        return SearchResponse(
            results=book_responses,
            total_found=len(book_responses),
            query=query
        )
    except Exception as e:
        logger.error(f"Error in advanced search:{e}")
        raise HTTPException(status_code=500, detail=f"Advanced search error: {str(e)}")

@app.get("/book/{book_id}", response_model=BookResponse, tags=["Books"])
async def get_book_by_id(book_id:str):
    try:
        logger.info(f"Getting book details for ID: {book_id}")
        book_details = search_engine.get_book_by_id(book_id)

        if not book_details:
            raise HTTPException(status_code=404, detail="Book not found")

        return BookResponse(
            id=book_details.get('id'),
            title=book_details.get('title', 'Unknown Title'),
            author=book_details.get('author', 'Unknown Author'),
            language=book_details.get('language', 'Unknown Language'),
            similarity_score=book_details.get('similarity_score'),
            document_preview=book_details.get('content', '')
        )

    except Exception as e:
        logger.error(f"Error getting book details: {e}")
        raise HTTPException(status_code=500, detail=f"Book details error: {str(e)}")    

@app.get("/stats", response_model=CollectionStats, tags=["Statistics"])
async def get_collection_stats():

    try:
        logger.info("Stats request")
        stats = search_engine.get_collection_stats()
        
        return CollectionStats(
            total_books=stats.get('total_books', 0),
            collection_name=stats.get('collection_name', 'Unknown'),
            database_path=stats.get('database_path', 'Unknown')
        )
    except Exception as e:
        logger.error(f"Error getting collection stats:{e}")
        raise HTTPException(status_code=500, detail=f"Collection stats error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0", port=8000)
