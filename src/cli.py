import typer
import logging

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


if __name__ == "__main__":
    cli()
