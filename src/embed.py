import logging
import os
from langchain_together import TogetherEmbeddings
from typing import List
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


# Initialize Together AI embeddings
embeddings = TogetherEmbeddings(
    model="BAAI/bge-large-en-v1.5",
    together_api_key=os.getenv("TOGETHER_API_KEY"),
)


def get_embedding(text: str) -> List[float]:
    """
    Get embedding for a single text using Together AI.

    Args:
        text (str): Text to embed

    Returns:
        List[float]: Embedding vector
    """
    try:
        embedding = embeddings.embed_query(text)
        if embedding is None:
            raise ValueError("Failed to generate embedding")
        return embedding
    except Exception as e:
        logger.error(f"Error getting embedding: {str(e)}")
        raise


def get_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Get embeddings for multiple texts in bulk using Together AI.

    Args:
        texts (List[str]): List of texts to embed

    Returns:
        List[List[float]]: List of embedding vectors
    """
    try:
        embeddings_list = embeddings.embed_documents(texts)
        if embeddings_list is None:
            raise ValueError("Failed to generate embeddings")
        return embeddings_list
    except Exception as e:
        logger.error(f"Error getting embeddings in bulk: {str(e)}")
        raise
