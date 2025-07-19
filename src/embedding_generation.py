import logging 
import pandas as pd 
import numpy as np
from sentence_transformers import SentenceTransformer
import chromadb
from data_loader import clean_data, load_data

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def main():

    # Step 1: Load and clean data
    logger.info('Loading data...')
    df1, df2 = load_data()
    if df1 is None:
        logger.error("Data loading failed")
        return False
    
    df3 = clean_data(df1)
    if df3 is None:
        logger.error("Data cleaning failed")
        return False
    
    logger.info(f"Loaded {len(df3)} books")

    # Step 2: Initialize ChromaDB
    logger.info("Initializing ChromaDB...")
    client = chromadb.PersistentClient(path="./chroma_db")
    
    try:
        collection = client.get_collection("books_story")
        logger.info("Using existing collection")
    except:
        collection = client.create_collection("books_story")
        logger.info("Created new collection")

    # Step 3: Create embeddings
    logger.info("Creating embeddings...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    texts = df3['content'].tolist()

    if not texts:
        logger.error("No text content available")
        return False

    embeddings = model.encode(texts, show_progress_bar=True)
    logger.info(f"Generated embeddings: {embeddings.shape}")

    # Step 4: Prepare metadata
    logger.info("Preparing metadata...")
    metadatas = []
    for i in range(len(df3)):
        metadata = {
            "bookno": str(df3.iloc[i]['bookno']),
            "title": str(df3.iloc[i]['Title']),
            "author": str(df3.iloc[i]['Author']),
            "language": str(df3.iloc[i]['Language'])
        }
        metadatas.append(metadata)

    # Step 5: Generate document IDs
    logger.info("Generating document IDs...")
    ids = [f"doc_{i}" for i in range(len(texts))]

    # Step 6: Add to collection
    logger.info("Adding documents to collection...")
    try:
        collection.add(
            documents=texts,
            embeddings=embeddings.tolist(),
            metadatas=metadatas,
            ids=ids
        )
        logger.info(f"Successfully added {len(df3)} documents to collection")
    except Exception as e:
        logger.error(f"Error adding documents to collection: {e}")
        return False

    # Step 7: Verification
    final_count = collection.count()
    logger.info(f"Final collection count: {final_count}")

    # Step 8: Save embeddings backup
    np.save('embeddings.npy', embeddings)
    logger.info("Embeddings saved as backup")
    logger.info("Embedding generation completed successfully")
    return True
    
if __name__ == "__main__":
    success = main()
    if not success:
        exit(1)

