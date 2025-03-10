#Create a Virtual Environment
mkdir ai-doc-search
cd ai-doc-search
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)


#Install Required Packages
pip install fastapi uvicorn transformers torch faiss-cpu sentence-transformers pydantic pdfminer.six python-docx python-pptx pymupdf elasticsearch pymongo

#Extract Text from Different File Types
For PDFs
import fitz  # PyMuPDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = "\n".join([page.get_text() for page in doc])
    return text

For Word Documents
from docx import Document
def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    return "\n".join([p.text for p in doc.paragraphs])

For PowerPoint Slides
from pptx import Presentation

def extract_text_from_pptx(pptx_path):
    ppt = Presentation(pptx_path)
    text = "\n".join([shape.text for slide in ppt.slides for shape in slide.shapes if hasattr(shape, "text")])
    return text


#MongoDB for Metadata

#Using Hugging Face Transformer Models

#Set up API point
from fastapi import FastAPI, UploadFile, File

app = FastAPI()

@app.post("/upload/")
async def upload_document(file: UploadFile = File(...)):
    content = await file.read()
    text = extract_text_from_pdf(file.filename) if file.filename.endswith(".pdf") else extract_text_from_docx(file.filename)
    store_document(file.filename, text)
    return {"filename": file.filename, "message": "File uploaded successfully"}

@app.get("/search/")
async def search(query: str):
    results = search_documents(query, index, stored_texts)
    return {"results": results}

@app.get("/summarize/")
async def summarize(doc_id: str):
    doc = collection.find_one({"doc_id": doc_id})
    summary = summarize_text(doc["text"])
    return {"summary": summary}

#Run FastAPI Server
uvicorn main:app --reload

#Install React & Axios
npx create-react-app frontend
cd frontend
npm install axios


