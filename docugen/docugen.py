import os
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
from nltk.tokenize import sent_tokenize
import names
from .text_processor import paraphrase

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_wikipedia_page(title: Optional[str] = None) -> wikipedia.WikipediaPage:
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

def create_docx(text: str, title: str, folder: str, class_names: List[str], doc_no: int) -> None:
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

    safe_title = "".join(c for c in title.strip() if c not in r'\/:*?"<>|')
    file_path = f"{folder}/{doc_no} {safe_title}.docx"
    document.save(file_path)
    logging.info(f"Created document: {file_path}")

def create_pdf(text: str, title: str, folder: str, class_names: List[str], doc_no: int) -> None:
    safe_title = "".join(c for c in title.strip() if c not in r'\/:*?"<>|')
    file_path = f"{folder}/{doc_no} {safe_title}.pdf"
    
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
    amt = args.number
    wiki_title = args.title
    num_sentences = args.sentences
    class_names = args.class_names
    output_format = args.format
    batch = args.batch
    generated = 0
    
    for i in range(batch):
        while generated < amt:
            page = get_wikipedia_page(wiki_title)
            content = page.content.split("== See also ==")[0].strip()
            chunks = chunk_content(content, num_sentences)
            
            folder = f"output/{i+1} {page.title}"
            os.makedirs(folder, exist_ok=True)
            logging.info(f"Created directory: {folder}")

            for j, chunk in enumerate(tqdm(chunks, desc=f"Generating documents (Batch {i+1})", unit="doc")):
                if generated >= amt:
                    break
                paraphrased_chunk = paraphrase(chunk)
                title = " ".join(nltk.word_tokenize(paraphrased_chunk)[:3])
                if output_format == "docx":
                    create_docx(paraphrased_chunk, title, folder, class_names, doc_no=generated + 1)
                else:
                    create_pdf(paraphrased_chunk, title, folder, class_names, doc_no=generated + 1)
                generated += 1

        logging.info(f"Successfully generated {generated} documents in batch {i+1}")

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate study documents from Wikipedia articles")
    parser.add_argument("-t", "--title", help="The Wikipedia page title to use for generating documents", type=str)
    parser.add_argument("-n", "--number", help="The number of documents to generate in a batch", default=10, type=int)
    parser.add_argument("-b", "--batch", help="The number of batches to generate", default=1, type=int)
    parser.add_argument("-c", "--class_names", help="The class names to use for generating documents", 
                        nargs="+", type=str, default=["CS 1", "CS 2", "CS 3", "CS 4", "CS 5"])
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