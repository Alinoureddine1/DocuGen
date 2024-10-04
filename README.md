# DocuGen

DocuGen is a Python-based tool that generates study materials from Wikipedia articles. It can create both Word documents (.docx) and PDF files, making it versatile for various educational needs.

## Features

- Generate study materials from random or specified Wikipedia articles
- Output in both .docx and .pdf formats
- Customize the number of documents, batches, and sentences per document
- Paraphrase content to avoid direct copying
- Add random student names and class names to documents

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/Alinoureddine1/DocuGen.git
   cd DocuGen
   ```

2. (Optional) Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the package and its dependencies:
   ```
   pip install -e .
   ```

4. Download required NLTK data:
   ```
   python scripts/nltk_downloader.py
   ```

## Usage

You can use DocuGen in several ways:

### 1. As a command-line tool

After installation, you can use the `docugen` command directly:

```
docugen -n 5 -b 1 -f pdf -t "Artificial Intelligence"
```

### 2. Using Python scripts

Run the main script directly:

```
python -m docugen.docugen -n 10 -b 2 -f docx
```

### 3. Using provided batch scripts (Windows only)

For quick generation (5 documents in .docx format):
```
scripts\quick_generate.bat
```

For custom generation:
```
scripts\run_document_generator.bat -n 10 -b 2 -f pdf
```

### Arguments

- `-n, --number`: Number of documents to generate per batch (default: 10)
- `-b, --batch`: Number of batches to generate (default: 1)
- `-f, --format`: Output format, either "docx" or "pdf" (default: "docx")
- `-t, --title`: Specific Wikipedia page title to use (optional)
- `-c, --class_names`: Custom class names to use (optional)
- `-s, --sentences`: Number of sentences per document chunk (default: 25)

## Example

Generate 5 PDF documents about Python programming:

```
docugen -n 5 -f pdf -t "Python (programming language)"
```

This will create a folder in the `output` directory containing 5 PDF files, each with content derived from the Wikipedia page on Python programming.

## Development

To set up the development environment:

1. Clone the repository (if you haven't already)
2. Create and activate a virtual environment
3. Install the package in editable mode with development dependencies:
   ```
   pip install -e ".[dev]"
   ```
4. Run tests:
   ```
   python -m unittest discover tests
   ```

## Contributing

Contributions are welcome! Please see the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.