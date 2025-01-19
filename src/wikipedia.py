import json
import wikipedia
from typing import Dict, Any
import logging
from src.config import PROCESSED_DIR

logger = logging.getLogger(__name__)


def get_wikipedia_content(search_term: str) -> Dict[str, Any]:
    """
    Search Wikipedia for a term and return the article content with metadata.

    Args:
        search_term (str): The topic to search for on Wikipedia

    Returns:
        Dict[str, Any]: Dictionary containing article content and metadata
    """
    try:

        # Try to get the most relevant page
        search_term = wikipedia.search(search_term, results=1)[0]

        page = wikipedia.page(search_term, auto_suggest=False)

        return {
            "title": page.title,
            "content": page.content,
            "url": page.url,
            "top_level_section_id": search_term,
            "summary": page.summary,
        }
    except wikipedia.DisambiguationError as e:
        # If we get a disambiguation page, try the first suggestion
        try:
            page = wikipedia.page(e.options[0], auto_suggest=False)
            logger.warning(
                f"Used first disambiguation option for {search_term}: {e.options[0]}"
            )
            return {
                "title": page.title,
                "content": page.content,
                "url": page.url,
                "top_level_section_id": search_term,
                "references": page.references,
                "summary": page.summary,
                "disambiguation_options": e.options,
            }
        except:  # noqa: E722
            logger.error(
                f"Failed to get content for disambiguation option: {e.options[0]}"
            )
            raise Exception(
                f"Failed to get content for disambiguation option: {e.options[0]}"
            )
    except wikipedia.PageError:
        logger.error(f"No Wikipedia page found for: {search_term}")
        raise Exception(f"No Wikipedia page found for: {search_term}")
    except Exception as e:
        logger.error(f"Error fetching Wikipedia content for {search_term}: {str(e)}")
        raise Exception(f"Error fetching Wikipedia content for {search_term}: {str(e)}")


def store_wikipedia_content(topics_file: str, subject: str, form: int) -> None:
    """
    Fetch Wikipedia content for topics and store in a JSON file.

    Args:
        topics_file (str): Name of the JSON file containing topics
        subject (str): Subject name (e.g., 'Geography')
        form (int): Form number (1-6)
    """
    # Load topics
    topics_path = PROCESSED_DIR / "topics" / topics_file
    try:
        with open(topics_path, "r") as f:
            topics = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Topics file not found: {topics_file}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON in topics file: {topics_file}")

    # Create output directory if it doesn't exist
    wiki_dir = PROCESSED_DIR / "wikipedia"

    # Fetch content for each topic
    wiki_data = {
        "metadata": {
            "subject": subject,
            "form": form,
            "source_topics_file": topics_file,
        },
        "articles": {},
    }

    for topic in topics:
        print(f"Fetching Wikipedia content for: {topic}")
        data = get_wikipedia_content(topic)
        if data:
            wiki_data["articles"][topic] = data

    # Save to file
    output_file = f"{subject.lower()}_form_{form}_wiki_content.json"
    output_path = wiki_dir / output_file

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(wiki_data, f, ensure_ascii=False, indent=2)

    logger.info(f"Saved Wikipedia content to {output_path}")
    logger.info(
        f"Successfully fetched {len(wiki_data['articles'])} out of {len(topics)} topics"
    )


if __name__ == "__main__":
    # Example usage
    res = get_wikipedia_content("Landforms")
    print(res)
