import fitz
from transformers import AutoTokenizer

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in range(len(doc)):
        content = doc.load_page(page)
        text += content.get_text()
    return text

def tokenize_trim_text(text, max_tokens=1000):
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B")
    tokens = tokenizer.encode(text)
    trimmed_tokens = tokens[:max_tokens]
    trimmed_text = tokenizer.decode(trimmed_tokens, skip_special_tokens=True)
    return trimmed_text

