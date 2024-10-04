# Copyright (C) 2024 DocuGen
# This file is part of DocuGen.
#
# DocuGen is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import re
import random
import argparse
from typing import List, Optional
from tqdm import tqdm
import logging
import wikipedia
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import names
from .text_processor import paraphrase

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_title(title: str) -> str:
    """Clean and format the title."""
    # Remove special characters and extra whitespace
    cleaned = re.sub(r'[=(){}\[\]],', '', title)
    cleaned = re.sub(r'\s+', ' ', cleaned)
    # Capitalize the first letter of each word
    cleaned = ' '.join(word.capitalize() for word in cleaned.split())
    # Limit to first 50 characters and strip
    return cleaned.strip()[:50]

def get_wikipedia_page(title: Optional[str] = None) -> wikipedia.WikipediaPage:
    """Retrieve a Wikipedia page."""
    try:
        if not title:
            title = wikipedia.random(1)
        page = wikipedia.page(title, auto_suggest=False)
        logging.info(f"Retrieved page: {page.title} (URL: {page.url})")
        return page
    except wikipedia.DisambiguationError as e:
        title = random.choice(e.options)
        page = wikipedia.page(title, auto_suggest=False)
        logging.info(f"Disambiguation: using '{page.title}' (URL: {page.url})")
        return page
    except Exception as e:
        logging.error(f"Error retrieving Wikipedia page: {e}")
        raise

def chunk_content(content: str, chunk_size: int) -> List[str]:
    """Split content into chunks of specified sentence count."""
    sentences = sent_tokenize(content)
    chunks = []
    current_chunk = []
    
    for sentence in sentences:
        current_chunk.append(sentence)
        if len(current_chunk) >= chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks

def create_docx(text: str, title: str, folder: str, class_names: List[str], doc_no: int, file_title: str) -> None:
    """Create a Word document."""
    document = Document()
    
    # Name and Class
    for content in [names.get_full_name(), random.choice(class_names)]:
        paragraph = document.add_paragraph()
        run = paragraph.add_run(content)
        run.font.size = Pt(12)
        run.font.name = "Times New Roman"
    
    # Heading
    paragraph = document.add_paragraph()
    run = paragraph.add_run(title)
    run.font.size = Pt(16)
    run.font.name = "Times New Roman"
    run.bold = True
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Content
    document.add_paragraph(text)

    file_path = f"{folder}/{file_title}.docx"
    document.save(file_path)
    logging.info(f"Created document: {file_path}")

def create_pdf(text: str, title: str, folder: str, class_names: List[str], doc_no: int, file_title: str) -> None:
    """Create a PDF document."""
    file_path = f"{folder}/{file_title}.pdf"
    
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Name and Class
    for content in [names.get_full_name(), random.choice(class_names)]:
        story.append(Paragraph(content, styles['Normal']))
        story.append(Spacer(1, 12))

    # Heading
    title_style = ParagraphStyle(name='Title', parent=styles['Heading1'], alignment=TA_CENTER)
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 12))

    # Content
    story.append(Paragraph(text, styles['BodyText']))

    doc.build(story)
    logging.info(f"Created document: {file_path}")

def generate_documents(args: argparse.Namespace) -> None:
    """Generate documents based on the provided arguments."""
    amt = args.number
    wiki_title = args.title
    num_sentences = args.sentences
    class_names = args.class_names
    output_format = args.format
    generated = 0
    
    # Create a single output folder
    folder = "output"
    os.makedirs(folder, exist_ok=True)
    logging.info(f"Created directory: {folder}")

    while generated < amt:
        page = get_wikipedia_page(wiki_title)
        content = page.content.split("== See also ==")[0].strip()
        chunks = chunk_content(content, num_sentences)
        
        for chunk in tqdm(chunks, desc=f"Generating documents", unit="doc"):
            if generated >= amt:
                break
            paraphrased_chunk = paraphrase(chunk)
            title = clean_title(" ".join(word_tokenize(paraphrased_chunk)[:5]))
            
            # Include the Wikipedia page title in the document filename
            safe_page_title = re.sub(r'[\\/*?:"<>|]', "", page.title)
            file_title = f"{generated+1:03d}_{safe_page_title}_{title}"
            
            if output_format == "docx":
                create_docx(paraphrased_chunk, title, folder, class_names, doc_no=generated + 1, file_title=file_title)
            else:
                create_pdf(paraphrased_chunk, title, folder, class_names, doc_no=generated + 1, file_title=file_title)
            generated += 1

    logging.info(f"Successfully generated {generated} documents")

def main() -> None:
    """Main function to parse arguments and initiate document generation."""
    parser = argparse.ArgumentParser(description="Generate study documents from Wikipedia articles")
    parser.add_argument("-t", "--title", help="The Wikipedia page title to use for generating documents", type=str)
    parser.add_argument("-n", "--number", help="The number of documents to generate", default=10, type=int)
    parser.add_argument("-c", "--class_names", help="The class names to use for generating documents", 
                        nargs="+", type=str, default=["CS 101", "CS 202", "CS 303", "CS 404", "CS 505"])
    parser.add_argument("-s", "--sentences", help="The number of sentences to use for each chunk", default=25, type=int)
    parser.add_argument("-f", "--format", help="Output format (docx or pdf)", choices=["docx", "pdf"], default="docx")
    
    args = parser.parse_args()
    
    if os.path.exists("output"):
        import shutil
        shutil.rmtree("output")
        logging.info("Previous output deleted")
    os.makedirs("output", exist_ok=True)
    logging.info("Created output directory")
    
    generate_documents(args)

if __name__ == "__main__":
    main()