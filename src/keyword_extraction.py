from typing import List
import json
from src.config import PROCESSED_DIR
import re
from langchain_openai import ChatOpenAI


def locate_form_pages(form: int, json_name: str) -> List[int]:
    """Find the pages of a specific form in the curriculum PDF

    Args:
        form (int): Form number (1-4)
        json_name (str): Name of the processed JSON file (without path)

    Returns:
        List[int]: List of page numbers containing content for the specified form
    """
    # Validate input
    if not 1 <= form <= 6:
        raise ValueError("Form must be between 1 and 6")

    # Load processed documents
    json_path = PROCESSED_DIR / "documents" / json_name
    with open(json_path, "r") as f:
        docs = json.load(f)

    # Convert form number to text representation
    form_texts = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six"}
    form_text = form_texts[form]

    pages = []
    current_form = None

    for doc in docs:
        page_num = doc["metadata"].get("page_number")
        text = doc["page_content"].strip()

        # Look for form indicators or bibliography at the start of text
        form_match = re.match(r"^Form\s+(One|Two|Three|Four|Five|Six)", text)
        biblio_match = re.match(r"^Bibliograph[y|ies]", text)

        if form_match:
            matched_form = form_match.group(1)
            if matched_form == form_text:
                current_form = form
            elif matched_form != form_text:
                if current_form == form:  # If we were in our target form, stop
                    break
                current_form = None
        elif biblio_match and current_form == form:
            # If we hit bibliography while in our target form, stop
            break

        if current_form == form and page_num not in pages:
            pages.append(page_num)

    return sorted(pages)


def get_tabular_data(pages: List[int], json_name: str) -> List[str]:
    """Extract tabular data from the specified form pages

    Args:
        pages (List[int]): List of page numbers containing content for the specified form
        form (int): Form number (1-6)
        json_name (str): Name of the processed JSON file (without path)

    Returns:
        List[str]: List of tabular data extracted from the specified form pages
    """
    # Load processed documents
    json_path = PROCESSED_DIR / "documents" / json_name
    with open(json_path, "r") as f:
        docs = json.load(f)

    tabular_data = []

    for doc in docs:
        page_num = doc["metadata"].get("page_number")

        # Only process pages that belong to the specified form
        if page_num not in pages:
            continue

        doc_text = doc["page_content"]
        if doc["metadata"].get("category") == "Table":
            tabular_data.append(doc_text)
            continue

    return tabular_data


def extract_keywords(form: int, json_name: str, subject: str) -> List[str]:
    """Extract key topics from tabular data for a specific form using LLM

    Args:
        form (int): Form number (1-6)
        json_name (str): Name of the processed JSON file (without path)

    Returns:
        List[str]: List of unique keywords/topics extracted from the tables
    """
    llm = ChatOpenAI(
        model="gpt-4o", model_kwargs={"response_format": {"type": "json_object"}}
    )

    # Get relevant pages for the form
    pages = locate_form_pages(form, json_name)

    # Get tabular data from those pages
    tables = get_tabular_data(pages, json_name)

    # Extract keywords from each table using LLM
    all_keywords = []
    for table in tables:
        # Remove HTML tags for cleaner input
        clean_text = re.sub(r"<[^>]+>", " ", table)

        # Use LLM to extract keywords
        response = llm.invoke(
            f"Identify key academic topics in the field of {subject} from this table content and return it as a json object with key 'topics' and a value of a list containing the topic strings: {clean_text}",
        )

        json_response = json.loads(response.content)  # type: ignore

        # Parse the response and add to keywords
        try:
            all_keywords.extend(json_response["topics"])
        except Exception as e:
            print(
                f"Error parsing json response for all keywords: {json_response} \nError: {e}"
            )
            continue

    # Use LLM to merge similar topics
    if all_keywords:
        keywords_str = ", ".join(all_keywords)
        response = llm.invoke(
            f"Remove duplicate topics and return a json object with key 'topics' and a value of a list containing the topic strings. Also rewrite the strings to be similar to Wikipedia article headings, meaning each contains only one topic/keyword. The strings should be maximum 3 words long.: {keywords_str}",
        )

        try:
            final_keywords = json.loads(response.content)["topics"]  # type: ignore
        except Exception as e:
            print(
                f"Error parsing json response for final keywords: {response} \nError: {e}"
            )
            final_keywords = all_keywords
    else:
        final_keywords = []

    # Save keywords to file
    output_dir = PROCESSED_DIR / "topics"
    output_path = output_dir / f"{subject}_form_{form}_topics.json"

    with open(output_path, "w") as f:
        json.dump(final_keywords, f, indent=2)

    return final_keywords


if __name__ == "__main__":
    form = 1
    json_name = "geo-o-level-curriculum.json"
    pages = locate_form_pages(form, json_name)
    print(f"Pages containing Form {form}: {pages}")

    # Test tabular data extraction
    tables = get_tabular_data(pages, json_name)
    print(f"\nFound {len(tables)} tables:")
    for i, table in enumerate(tables, 1):
        print(f"\nTable {i}:")
        print(table)
