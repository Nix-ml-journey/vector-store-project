import logging
import pandas as pd
from config import CSV_PATH1, CSV_PATH2
import re
import psutil

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def load_data():
    logging.info(f"Loading data from {CSV_PATH1} and {CSV_PATH2}")  
    try:
        df1 = pd.read_csv(CSV_PATH1)
        logging.info(f"Loaded db_books.csv: {len(df1)} rows")
        return df1, None
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        return None, None

def clean_merged_data(df):
    """Clean the merged dataframe"""
    logging.info("Cleaning merged data")
    
    df_cleaned = df.drop_duplicates(subset=['bookno', 'Title'])
    df_cleaned.columns = df_cleaned.columns.str.strip()
    
    if 'Title' in df_cleaned.columns:
        df_cleaned['Title'] = df_cleaned['Title'].str.strip()
    if 'Author' in df_cleaned.columns:
        df_cleaned['Author'] = df_cleaned['Author'].str.strip()
    if 'Language' in df_cleaned.columns:
        df_cleaned['Language'] = df_cleaned['Language'].str.strip()
    
    df_cleaned = df_cleaned.dropna(subset=['Title', 'Author', 'Language'])
    
    logging.info(f"Cleaned merged data: {len(df_cleaned)} rows")
    return df_cleaned

def process_stories_in_chunks(chunk_size=1000):
    """Process large stories.csv in chunks"""
    logging.info("Processing stories.csv in chunks")
    
    cleaned_stories = []
    chunk_count = 0
    
    try:
        for chunk in pd.read_csv(CSV_PATH2, chunksize=chunk_size):
            chunk_count += 1
            logging.info(f"Processing chunk {chunk_count}")
            
            cleaned_chunk = clean_stories_chunk(chunk)
            cleaned_stories.append(cleaned_chunk)
            
            if chunk_count % 10 == 0:
                logging.info(f"Processed {chunk_count} chunks")
        
        final_stories = pd.concat(cleaned_stories, ignore_index=True)
        logging.info(f"Completed processing stories.csv: {len(final_stories)} rows")
        return final_stories
    
    except Exception as e:
        logging.error(f"Error processing stories.csv: {e}")
        return None

def clean_stories_chunk(chunk):
    """Clean individual chunks of stories data"""
    chunk_cleaned = chunk.drop_duplicates()
    
    if 'bookno' in chunk_cleaned.columns:
        chunk_cleaned['bookno'] = chunk_cleaned['bookno'].str.strip()
    
    if 'content' in chunk_cleaned.columns:
        chunk_cleaned['content'] = chunk_cleaned['content'].apply(clean_book_content)
    
    chunk_cleaned = chunk_cleaned.dropna(subset=['bookno', 'content'])
    return chunk_cleaned

def clean_book_content(content):
    """Clean individual book content"""
    if pd.isna(content):
        return ''
    
    content_str = str(content)
    content_str = remove_gutenberg_header(content_str)
    content_str = ' '.join(content_str.split())
    content_str = re.sub(r'\s+', ' ', content_str)
    
    return content_str.strip()

def remove_gutenberg_header(content_str):
    """Remove Project Gutenberg headers and footers"""
    start_patterns = [
        r'\*\*\* START OF THIS PROJECT GUTENBERG EBOOK.*?\*\*\*',
        r'START OF THE PROJECT GUTENBERG EBOOK.*?',
        r'THE FULL PROJECT GUTENBERG EBOOK.*?',
    ]
    
    end_patterns = [
        r'\*\*\* END OF THIS PROJECT GUTENBERG EBOOK.*?\*\*\*',
        r'END OF THE PROJECT GUTENBERG EBOOK.*?',
        r'END of PROJECT GUTENBERG EBOOK.*?',
    ]
    
    for pattern in start_patterns + end_patterns:
        content_str = re.sub(pattern, ' ', content_str, flags=re.IGNORECASE | re.DOTALL)
    
    return content_str

def merge_cleaned_data(cleaned_df, cleaned_stories):
    """Merge the cleaned dataframes"""
    logging.info("Merging cleaned data")
    
    try:
        final_df = cleaned_df.merge(cleaned_stories, on='bookno', how='inner')
        final_df = final_df.drop_duplicates()
        final_df = final_df.dropna(subset=['bookno', 'Title', 'content'])
        
        logging.info(f"Final merged dataset: {len(final_df)} rows")
        return final_df
    
    except Exception as e:
        logging.error(f"Error merging cleaned data: {e}")
        return None

def clean_data(df):
    """Clean the dataframe efficiently"""
    logging.info("Starting data cleaning process")
    
    try:
        # Step 1: Clean the loaded dataframe
        cleaned_df = clean_merged_data(df)
        
        # Step 2: Process large stories.csv in chunks
        cleaned_stories = process_stories_in_chunks()
        
        # Step 3: Merge cleaned data
        final_df = merge_cleaned_data(cleaned_df, cleaned_stories)
        
        logging.info("Data cleaning completed successfully")
        return final_df
    
    except Exception as e:
        logging.error(f"Error cleaning data: {e}")
        return None

def get_memory_usage():
    """Get current memory usage in MB"""
    process = psutil.Process()
    memory_info = process.memory_info()
    return memory_info.rss / (1024 * 1024)

def log_memory_usage(stage):
    """Log memory usage at different stages"""
    memory_mb = get_memory_usage()
    logging.info(f"Memory usage at {stage}: {memory_mb:.2f} MB")

# Main execution
if __name__ == "__main__":
    df1, df2 = load_data()
    
    if df1 is not None:
        cleaned_df = clean_data(df1)
        if cleaned_df is not None:
            logging.info("Data cleaning completed successfully")
            print("Cleaned data shape:", cleaned_df.shape)
            print(cleaned_df.head())
        else:
            logging.error("Data cleaning failed")
    else:
        logging.error("Data loading failed")






