# DocuGen

DocuGen is a Python-based tool that generates study materials from Wikipedia articles. It can create both Word documents (.docx) and PDF files, making it versatile for various educational needs.

## Features

- Generate study materials from random or specified Wikipedia articles
- Output in both .docx and .pdf formats
- Customize the number of documents and sentences per document
- Paraphrase content to avoid direct copying
- Add random student names and class names to documents

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/DocuGen.git
   cd DocuGen
   ```

2. Create and activate a virtual environment:
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
   python -m docugen.nltk_downloader
   ```

## Usage

After installation, you can use DocuGen directly from the command line:

```
docugen [options]
```

### Options

- `-n, --number`: Number of documents to generate (default: 10)
- `-t, --title`: Specific Wikipedia page title to use (optional)
- `-c, --class_names`: Custom class names to use (optional)
- `-s, --sentences`: Number of sentences per document chunk (default: 25)
- `-f, --format`: Output format, either "docx" or "pdf" (default: "docx")

### Examples

Generate 5 PDF documents:
```
docugen -n 5 -f pdf
```

Generate 10 documents about Python programming:
```
docugen -n 10 -t "Python (programming language)"
```

## Output

Generated documents are placed in an `output` folder in your current working directory. Each document's filename includes a number, the source Wikipedia page title, and the document title.

## Development

To set up the development environment:

1. Clone the repository
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

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.