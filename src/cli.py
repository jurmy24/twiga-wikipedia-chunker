import typer
from src.pdf_to_docs import create_documents
import logging

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


# TODO: Implement this
@cli.command()
def visualize(
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


if __name__ == "__main__":
    cli()
