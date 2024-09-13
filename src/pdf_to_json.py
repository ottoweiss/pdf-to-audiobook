import json
import re
import fitz
from ocrfixr import spellcheck
from tqdm import tqdm
import tiktoken

def split_into_chunks(text, word_limit=1200):
    """
    Split text into chunks by word limit.
    
    Parameters:
    - text (str): The input text.
    - word_limit (int, optional): The approximate number of words for each chunk. Defaults to 2700.
    
    Returns:
    - list: List of text chunks.
    """
    sentences = re.split(r'(?<=[.!?])\s+', text)

    chunks = []
    current_chunk = []
    current_word_count = 0

    for sentence in sentences:
        sentence_word_count = len(sentence.split())
        
        # If adding the next sentence doesn't exceed the word limit, add it to the current chunk
        if current_word_count + sentence_word_count <= word_limit:
            current_chunk.append(sentence)
            current_word_count += sentence_word_count
        else:
            # If the word limit is exceeded, finalize the current chunk and start a new one
            chunks.append(' '.join(current_chunk))
            current_chunk = [sentence]
            current_word_count = sentence_word_count

    # Add the last chunk if it's not empty
    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks


def extract_text_from_pdf(pdf_path, sections, page_difference=0):
    """
    Extracts the text from specified sections of a PDF file.

    Parameters:
    pdf_path (str): The file path to the PDF file.
    sections (dict): Dictionary specifying sections and their corresponding page ranges.

    Returns:
    dict: Dictionary where keys are section titles and values are extracted text for each section.
    """
    doc = fitz.open(pdf_path)
    section_ranges = [(title, (s + page_difference, e + page_difference)) for title, (s, e) in sections.items()]
    section_texts = {}
    for page_num in tqdm(range(1, len(doc) + 1)):
        page = doc[page_num - 1]
        cleaned_text = page.get_text()
        # Dictionary to store the extracted text for each section
        for title, (start, end) in section_ranges:
            if start <= page_num <= end:
                cleaned_text = cleaned_text.replace('–', '-').replace('—', '-')  # Replace en-dash and em-dash with hyphen
                cleaned_text = cleaned_text.replace("\x0c", "")  # Replace line breaks with spaces

                cleaned_text = spellcheck(cleaned_text).text
                
                # Append the processed text to the respective section
                if title in section_texts:
                    section_texts[title] += cleaned_text
                else:
                    section_texts[title] = cleaned_text
                break
    section_chunks = {}
    overall_count = 0
    total_text = ""
    for title, text in section_texts.items():
        total_text += text
        chunks = split_into_chunks(text)
        current_chunks = list()
        for i, chunk in enumerate(chunks):
            current_chunks.append(chunk)
            if i % 3 == 0 and i != 0:
                section_chunks[overall_count] = current_chunks
                overall_count += 1
                current_chunks = list()
        section_chunks[overall_count] = current_chunks

    encoding = tiktoken.encoding_for_model('gpt-3.5-turbo')
    total_tokens = len(encoding.encode(total_text))
    rewrite_cost = (total_tokens*1.8/1000000) * 0.35
    audio_cost = ((len(total_text) * 4/5)/1000000) * 15
    audio_time = (len(total_text) * 4/5) * 0.0014
    rewrite_time = (0.0145) * total_tokens
    total_time = audio_time + rewrite_time
    total_time_secs = str(int(total_time % 60))
    total_time_mins = str(int(total_time // 60))
    total_time_str = f"{total_time_mins} mins {total_time_secs} secs"
    total_cost = round(rewrite_cost + audio_cost, 2)
    total_cost_str = f"{total_cost} $"
    total_cost_good_audio = f"{round(rewrite_cost + (audio_cost * 2), 2)}"
    with open(pdf_path.replace(".pdf", ".json"), "w", encoding="utf-8") as sections_json:
        json.dump(section_chunks, sections_json, indent=2)
    return total_cost_str, total_time_str, total_cost_good_audio
