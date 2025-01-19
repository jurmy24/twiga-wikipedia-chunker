# src/visualize.py
import fitz
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from PIL import Image
import json
from pathlib import Path
from src.config import RAW_DIR, PROCESSED_DIR


def plot_pdf_with_boxes(pdf_path: Path, pdf_page, segments):
    pix = pdf_page.get_pixmap()
    pil_image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)  # type: ignore
    fig, ax = plt.subplots(1, figsize=(10, 10))
    ax.imshow(pil_image)

    categories = set()
    category_to_color = {
        "Title": "orchid",
        "Image": "forestgreen",
        "Table": "tomato",
    }

    for segment in segments:
        points = segment["coordinates"]["points"]
        layout_width = segment["coordinates"]["layout_width"]
        layout_height = segment["coordinates"]["layout_height"]
        scaled_points = [
            (x * pix.width / layout_width, y * pix.height / layout_height)
            for x, y in points
        ]
        box_color = category_to_color.get(segment["category"], "deepskyblue")
        categories.add(segment["category"])
        rect = patches.Polygon(
            scaled_points, linewidth=1, edgecolor=box_color, facecolor="none"
        )
        ax.add_patch(rect)

    # Make legend
    legend_handles = [patches.Patch(color="deepskyblue", label="Text")]
    for category in ["Title", "Image", "Table"]:
        if category in categories:
            legend_handles.append(
                patches.Patch(color=category_to_color[category], label=category)
            )

    ax.set_title(f"Page Visualization - {pdf_path.name}")
    ax.axis("off")
    ax.legend(handles=legend_handles, loc="upper right")
    plt.tight_layout()
    return fig


def visualize_page(
    pdf_name: str,
    page_number: int,
    print_text: bool = False,
    save_path: str | None = None,
):
    """Visualize a specific page of a PDF with its document segments"""
    pdf_path = RAW_DIR / pdf_name
    json_path = PROCESSED_DIR / "documents" / f"{pdf_path.stem}.json"

    # Load the processed documents
    with open(json_path, "r") as f:
        docs = json.load(f)

    # Open PDF
    pdf = fitz.open(str(pdf_path))
    pdf_page = pdf[page_number - 1]

    # Filter documents for the specific page
    page_docs = [
        doc for doc in docs if doc["metadata"].get("page_number") == page_number
    ]
    segments = [doc["metadata"] for doc in page_docs]

    # Create visualization
    fig = plot_pdf_with_boxes(pdf_path, pdf_page, segments)

    # Print text if requested
    if print_text:
        print("\nText content:")
        for doc in page_docs:
            print(f"{doc['page_content']}\n")

    # Save or show
    if save_path:
        save_location = Path(save_path)
        save_location.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_location)
        plt.close(fig)
        print(f"Visualization saved to {save_location}")
    else:
        plt.show()

    pdf.close()
