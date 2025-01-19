import json
from typing import List
from langchain_unstructured import UnstructuredLoader
from langchain_core.documents import Document
from src.config import RAW_DIR, PROCESSED_DIR

file_path = "geo-o-level-curriculum.pdf"


def create_documents(file_name: str) -> List[Document]:
    """Create documents from a PDF file and save them as JSON files.

    Args:
        file_name (str): The name of the PDF file in the data/raw directory
    """

    assert file_name.endswith(".pdf")
    file_path = str(RAW_DIR / file_name)

    loader = UnstructuredLoader(
        file_path=file_path,
        strategy="hi_res",
        partition_via_api=True,
        coordinates=True,
    )

    docs: List[Document] = []
    for doc in loader.lazy_load():
        docs.append(doc)

    output_path = str(PROCESSED_DIR / "documents" / file_name.replace(".pdf", ".json"))
    with open(output_path, "w", encoding="utf-8") as f:
        docs_dict = [doc.model_dump() for doc in docs]
        json.dump(docs_dict, f, ensure_ascii=False, indent=2)

    return docs


# for doc in loader.lazy_load():
#     docs.append(doc)
#     doc_dict = {"page_content": doc.page_content, "metadata": doc.metadata}
#     docs_dict.append(doc_dict)

# with open(output_path, "w", encoding="utf-8") as f:
#     json.dump(docs_dict, f, ensure_ascii=False, indent=2)
