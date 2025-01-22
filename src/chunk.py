# Import required libraries
import json
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter

from src.config import FINAL_DIR, PROCESSED_DIR
from src.embed import get_embeddings


def chunk_articles(input_file: str) -> None:
    """
    Chunks articles from input JSON file into ~250 token chunks with overlap
    and saves to output directory in specified format.

    Args:
        input_file: Name of JSON file containing articles
    """
    articles_path = PROCESSED_DIR / "wikipedia" / input_file

    # Load input JSON
    with open(articles_path, "r") as f:
        data = json.load(f)

    # Pretend the geography_form_X_wikipedia is the textbook name
    textbook = data["metadata"]["source_topics_file"].replace("_topics.json", "")

    # Initialize text splitter with ~250 tokens per chunk
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # Approximate number of characters for 250 tokens
        chunk_overlap=200,  # Scaled overlap to match new chunk size
        length_function=len,
        separators=["\n\n", "\n", " ", ""],
    )

    # Process each article
    all_chunks = []
    all_texts = []
    chunk_metadata = []

    for section_id, article in data["articles"].items():
        print(f"Chunking {section_id}...")
        # Split content into chunks
        chunks = text_splitter.split_text(article["content"])

        # Store chunks and metadata
        for chunk in chunks:
            all_texts.append(chunk)
            chunk_metadata.append(
                {
                    "chapter": section_id,
                    "chapter_number": None,
                    "chunk_type": "text",
                    "textbook": f"{textbook}_wikipedia",
                }
            )

    # Get embeddings in bulk
    print("Getting embeddings for all chunks...")
    try:
        embeddings = get_embeddings(all_texts)
    except Exception as e:
        print(f"Error getting embeddings: {e}")
        embeddings = [[] for _ in all_texts]

    # Create final chunk objects
    for text, metadata, embedding in zip(all_texts, chunk_metadata, embeddings):
        chunk_data = {"chunk": text, "metadata": metadata, "embedding": embedding}
        all_chunks.append(chunk_data)

    # Save all chunks to output file
    output_file_path = FINAL_DIR / f"{os.path.splitext(input_file)[0]}_chunks.json"
    with open(output_file_path, "w") as f:
        json.dump(all_chunks, f, indent=2)
