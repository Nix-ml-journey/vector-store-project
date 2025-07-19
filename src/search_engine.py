import logging 
from typing import List, Dict, Any, Optional
from vector_store import VectorStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SearchEngine:
    def __init__(self, collection_name:str = "books_story", db_path:str = "./chroma.db"):
        self.vector_store = VectorStore(collection_name)
        logger.info("Search engine initialized")

    def search_books(self, query:str, n_results: int = 5) -> List[Dict[str, Any]]:
        
        try:
            logger.info(f"Searching for books with query: '{query}'")
            result = self.vector_store.search_by_text(query, n_results)
        
            if not result or 'metadatas' not in result:
                return []
        
            formatted_results = []
            # ChromaDB returns metadatas as a list with one element containing all metadata objects
            metadata_list = result['metadatas'][0] if result['metadatas'] else []
            for i, metadata in enumerate(metadata_list):
                if metadata:
                    formatted_results.append({
                        'id': result.get('ids', [[]])[0][i] if result.get('ids') else f"doc_{i}",
                        'title': metadata.get('title', 'Unknown Title'),
                        'author': metadata.get('author', 'Unknown Author'),
                        'language': metadata.get('language', 'Unknown Language'),
                        'similarity_score': result.get('distances', [[]])[0][i] if result.get('distances') else None,
                        'document_preview': self._get_document_preview(result['documents'][0][i]) if result.get('documents') else ''
                    })
            logger.info(f"Found {len(formatted_results)}")
            return formatted_results
        
        except Exception as e:
            logger.error(f"Error searching books: {e}")
            return []

    def search_by_author(self, author:str, n_results:int = 5) -> List[Dict[str, Any]]:

        try:
            logger.info(f"Searching for books by author: '{author}'")
            metadata_filter = {'author' : author}
            results = self.vector_store.search_by_metadata(metadata_filter, n_results)
            return self._format_search_results(results)
        
        except Exception as e:
            logger.error(f"Error searching by author: {e}")
            return []
        
    def search_by_language(self, language:str, n_results:int = 5) -> List[Dict[str,Any]]:

        try:
            logger.info(f"Searching for books by language: '{language}'")
            metadata_filter = {'language' : language}
            results = self.vector_store.search_by_metadata(metadata_filter, n_results)
            return self._format_search_results(results)

        except Exception as e:
            logger.error(f"Error searching by language: {e}")
            return []

    def get_book_by_id(self, book_id:str) -> Optional[Dict[str,Any]]:

        try:
            logger.info(f"Getting book by ID: '{book_id}'")
            result = self.vector_store.get_document_by_id(book_id)
            if result:
                return {
                    'id': result['id'],
                    'title': result['metadata'].get('title', 'Unknown Title'),
                    'author': result['metadata'].get('author', 'Unknown Author'),
                    'bookno': result['metadata'].get('bookno', 'Unknown ID'),
                    'language': result['metadata'].get('language', 'Unknown Language'),
                    'content': result['document']
                }
            return None

        except Exception as e:
            logger.error(f"Error getting book by ID: {e}")
            return None

    def get_collection_stats(self) -> Dict[str,Any]:
        
        try:
            info = self.vector_store.get_collection_info()
            count = self.vector_store.get_document_count()
            
            return{
                'total_books' : count,
                'collection_name' : info.get('collection_name', 'Unknown'),
                'database_path' : info.get('db_path', 'Unknown')
            }
        
        except Exception as e:
            logger.error(f"Error getting collection stats: {e}")
            return {}
    
    def _format_search_results(self, results:Dict[str,Any]) -> List[Dict[str,Any]]:

        formatted_results = []

        if not results or 'metadatas' not in results:
            return formatted_results
        
        # ChromaDB returns metadatas as a list with one element containing all metadata objects
        metadata_list = results['metadatas'][0] if results['metadatas'] else []
        for i, metadata in enumerate(metadata_list):
            if metadata:
                formatted_results.append({
                    'id': results.get('ids', [[]])[0][i] if results.get('ids') else f"doc_{i}",
                    'title': metadata.get('title', 'Unknown Title'),
                    'author': metadata.get('author', 'Unknown Author'),
                    'bookno': metadata.get('bookno', 'Unknown ID'),
                    'language': metadata.get('language', 'Unknown Language'),
                    'similarity_score': results.get('distances', [[]])[0][i] if results.get('distances') else None,
                    'document_preview': self._get_document_preview(results['documents'][0][i]) if results.get('documents') else ''
                })
            
        return formatted_results

    def _get_document_preview(self, document:str, max_length:int = 200) -> str:

        if not document:
            return ""
        
        # Return full content instead of truncated preview
        return document.strip()
    
    def _get_book_details(self, book_id:str) -> Optional[Dict[str,Any]]:
        
        try:
            book = self.get_book_by_id(book_id)
            if book:
                return {
                    'id' : book['id'],
                    'title' : book['title'],
                    'author' : book['author'],
                    'bookno' : book['bookno'],
                    'language' : book['language'],
                    'content' : book['content'],
                }
            return None
        
        except Exception as e:
            logger.error(f'Error getting book detials: {e}') 
            return {}
    
    def advanced_search(self, query:str, author:Optional[str] = None, language:Optional[str] = None, n_results:int = 5) -> List[Dict[str,Any]]:

        try:
            logger.info(f"Advance search:query='{query}', author={author}, language={language}")

            results = self.search_books(query, n_results)
            
            if author:
                results = [r for r in results if author.lower() in r['author'].lower()]
            if language:
                results = [r for r in results if language.lower() in r['language'].lower()]
            
            return results[:n_results]

        except Exception as e:
            logger.error(f"Error in advance_search: {e}")
            return []

if __name__ == "__main__":
    search_engine = SearchEngine()

    stats = search_engine.get_collection_stats()
    print(f"Collection Statistics: {stats}")

    print("\n=== Searching for 'adventure' ===")
    adventure_results = search_engine.search_books("adventure", n_results=5)
    for i, book in enumerate(adventure_results, 1):
        print(f"{i}.{book['title']} by {book['author']} {(book['language'])}")
        print(f" Preview: {book['document_preview'][:100]}...")
        print ("\n")

    print("=== Searching for books by 'Mark Twain' ===")
    author_results = search_engine.search_by_author("Mark Twain", n_results=3)
    for i, book in enumerate(author_results, 1):
        print(f"{i}. {book['title']} ({book['language']})")
        print()
    
    print("=== Searching for English books ===")
    language_results = search_engine.search_by_language("English", n_results=3)
    for i, book in enumerate(language_results, 1):
        print(f"{i}. {book['title']} by {book['author']}")
        print()
    
    print("=== Advanced search for 'love' in English ===")
    advanced_results = search_engine.advanced_search("love", language="English", n_results=3)
    for i, book in enumerate(advanced_results, 1):
        print(f"{i}. {book['title']} by {book['author']}")
        print(f"   Preview: {book['document_preview'][:100]}...")
        print() 