from webbrowser import get
import chromadb
import logging 
import numpy as np 
from typing import List, Dict, Optional, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VectorStore:

    def __init__(self, collection_name:str = "books_story", db_path:str = "./chroma_db"):
        self.db_path = db_path
        self.collection_name = collection_name
    
        logger.info(f"Initializing ChromDB client at {db_path}")
        self.client = chromadb.PersistentClient(path=db_path)

        try:
            self.collection = self.client.get_collection(collection_name)
            logger.info(f"Using exisiting collection: {collection_name}")
        except: 
            self.collection = self.client.create_collection(collection_name)
            logger.info(f"Created new collection:{collection_name}")

    def get_collection_info(self) -> Dict[str, Any]:
        try:
            count = self.collection.count()
            return{
            "collection_name": self.collection_name,
            "document_count": count,
            "db_path": self.db_path        
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {e}")
            return {}

    def search_by_text(self, query_text:str, n_results:int = 5) -> Dict[str, Any]:

        try:
            logger.info(f"Searching for: '{query_text}'")
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results
            )
            return results
        except Exception as e: 
            logger.error(f"Error searching by text: {e}")
            return {}

    def search_by_metadata(self, metadata_filter:Dict[str, str], n_results:int = 5) -> Dict[str, Any]:

        try:
            logger.info(f"Searching with metadata filter: {metadata_filter}")
            results = self.collection.query(
                query_texts=[""],
                n_results=n_results,
                where=metadata_filter
            )
            return results
        except Exception as e:
            logger.error(f"Error searching by metadata: {e}")
            return {}

    def get_document_by_id(self, doc_id:str) -> Optional[Dict[str, Any]]:
        
        try:
            results = self.collection.get(ids=[doc_id])
            if results['ids']:
                return{
                    'id': results['ids'][0],
                    'document': results['documents'][0],
                    'metadata': results['metadatas'][0],
                }
            return None
        except Exception as e:
            logger.error(f"Error getting document by ID:{e}")
            return None

    def get_all_documents(self, limit:Optional[int] = None) -> Dict[str, Any]:

        try:
            if limit:
                results = self.collection.get(limit=limit)
            else:
                results = self.collection.get()
            return results
        except Exception as e:
            logger.error(f"Error getting all documents:{e}")
            return {}
    
    def delete_document(self, doc_id:str) -> bool:

        try:
            self.collection.delete(ids=[doc_id])
            logger.info(f"Deleted document: {doc_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting document: {e}")
            return False
    
    def update_document(self, doc_id:str, document:str, metadata:Dict[str,str]) -> bool:

        try:
            self.collection.update(
                ids=[doc_id],
                documents=[document],
                metadatas=[metadata]
            )
            logger.info(f"Updated document: {doc_id}")
            return True
        except Exception as e:
            logger.error(f"Error updating document:{e}")
            return False

    def get_document_count(self) -> int:

        try:
            return self.collection.count()
        except Exception as e:
            logger.error(f"Error getting document count:{e}")
            return 0

if __name__ == "__main__":
    vector_store = VectorStore()

    info = vector_store.get_collection_info()
    print(f"Collection info: {info}")

    #results = vector_store.search_by_text("hunting", n_results = 5)
    #print(f"Search results: {results}")
    
    #count = vector_store.get_document_count()
    #print(f"Document count: {count}")