# CLI Commands

> ![Note]
>
> By the way, the prompts in keyword_extraction.py can definitely be improved, just did it on a whim.

The pipeline processes curriculum documents into searchable chunks in 4 steps:

1. Process PDF curriculum documents:

   ```bash
   # Convert a PDF file into processable documents
   python -m src.cli process-pdf <pdf_file_name>
   ```

2. Extract curriculum topics:

   ```bash
   # Extract key topics for a specific form and subject
   python -m src.cli extract-topics --input-file <processed_json> --form <1-6> --subject <subject_name>
   ```

3. Fetch Wikipedia content:

   ```bash
   # Fetch Wikipedia articles for the extracted topics
   python -m src.cli fetch-wiki --topics-file <topics_json> --subject <subject_name> --form <1-6>
   ```

4. Chunk Wikipedia articles:
   ```bash
   # Split Wikipedia articles into smaller segments
   python -m src.cli chunk-wiki --input-file <wiki_content_json>
   ```

Additional utilities:

- Visualize document segmentation on a PDF page

```bash
python -m src.cli visualize --input-file <pdf_file> --page <page_number> [--text] [--save <output_file>]
```

### Command Details

#### `process-pdf`

- **Purpose**: Converts a PDF curriculum document into processable JSON format
- **Arguments**:
  - `pdf_file_name`: Name of the PDF file located in the `data/raw` directory

#### `extract-topics`

- **Purpose**: Extracts key topics from processed curriculum documents
- **Options**:
  - `--input-file`: Name of the processed JSON file
  - `--form`: Form number (1-6)
  - `--subject`: Subject name (e.g., 'Geography', 'Biology')
- **Output**: Saves topics to `processed/topics/<subject>_form_<number>_topics.json`

#### `fetch-wiki`

- **Purpose**: Retrieves Wikipedia content for extracted curriculum topics
- **Options**:
  - `--topics-file`: Name of the topics JSON file
  - `--subject`: Subject name
  - `--form`: Form number (1-6)

#### `chunk-wiki`

- **Purpose**: Splits Wikipedia articles into smaller, manageable segments
- **Options**:
  - `--input-file`: Name of the Wikipedia content JSON file

#### `visualize`

- **Purpose**: Visualizes document segmentation on a PDF page
- **Options**:
  - `--input-file`: Name of the PDF file in data/raw directory
  - `--page`: Page number to visualize (default: 1)
  - `--text`: Flag to print text content
  - `--save`: Optional path to save visualization instead of displaying
