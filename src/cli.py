import typer
import logging

from src.config import PROCESSED_DIR
from src.keyword_extraction import extract_keywords
from src.pdf_to_docs import create_documents
from src.visualize import visualize_page

logger = logging.getLogger(__name__)
cli = typer.Typer()


@cli.command()
def process_pdf(
    file_name: str = typer.Argument(..., help="Name of PDF file in data/raw directory")
) -> None:
    """Process a PDF file into Documents and save as JSON"""
    try:
        docs = create_documents(file_name)
        typer.echo(f"Successfully processed {file_name} into {len(docs)} documents")
    except AssertionError:
        typer.echo("Error: File must be a PDF")
    except FileNotFoundError:
        typer.echo(f"Error: Could not find {file_name} in data/raw directory")
    except Exception as e:
        typer.echo(f"Error processing file: {str(e)}")


@cli.command()
def visualize(
    input_file: str = typer.Option(
        ..., "--input-file", help="Name of PDF file in data/raw directory"
    ),
    page: int = typer.Option(1, "--page", "-p", help="Page number to visualize"),
    show_text: bool = typer.Option(False, "--text", "-t", help="Print text content"),
    save: str = typer.Option(
        None, "--save", "-s", help="Save visualization to file instead of displaying"
    ),
) -> None:
    """Visualize document segments on a PDF page"""
    try:
        visualize_page(input_file, page, show_text, save)
    except FileNotFoundError:
        typer.echo(
            "Error: Could not find required files. Make sure both PDF and processed JSON exist."
        )
    except Exception as e:
        typer.echo(f"Error visualizing page: {str(e)}")


@cli.command()
def extract_topics(
    input_file: str = typer.Option(
        ..., "--input-file", help="Name of processed JSON file"
    ),
    form: int = typer.Option(..., "--form", help="Form number (1-6)"),
    subject: str = typer.Option(
        ..., "--subject", help="Subject name (e.g., 'Geography', 'Biology')"
    ),
) -> None:
    """Extract key topics from curriculum for a specific form"""
    try:
        typer.echo(f"Extracting topics for Form {form} {subject}...")
        keywords = extract_keywords(form, input_file, subject)
        typer.echo(f"\nExtracted {len(keywords)} topics:")
        for keyword in keywords:
            typer.echo(f"  • {keyword}")
        typer.echo(
            f"\nTopics saved to: {PROCESSED_DIR}/topics/{subject}_form_{form}_topics.json"
        )
    except ValueError as e:
        typer.echo(f"Error: {str(e)}")
    except FileNotFoundError:
        typer.echo(f"Error: Could not find file {input_file}")
    except Exception as e:
        typer.echo(f"Error extracting topics: {str(e)}")


if __name__ == "__main__":
    cli()
