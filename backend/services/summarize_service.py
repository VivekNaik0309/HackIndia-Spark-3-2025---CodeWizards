from transformers import pipeline
from database import get_document_by_id


summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def split_text(text, chunk_size=1024):
    """Splits text into chunks of max length `chunk_size`."""
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i + chunk_size]))
    
    return chunks

async def summarize_document(doc_id: str):
    doc = await get_document_by_id(doc_id)  # Fetch document from DB
    
    if not doc:  # Check if document exists
        raise ValueError(f"Document with ID {doc_id} not found.")

    text_chunks = split_text(doc["content"])  # Split text into chunks
    return summarize_chunks(text_chunks)  # Summarize the document

