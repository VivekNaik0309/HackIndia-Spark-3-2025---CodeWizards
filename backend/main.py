from fastapi import FastAPI, UploadFile, File
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware
import asyncio
asyncio.set_event_loop(asyncio.new_event_loop())


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from database import documents_collection
from services.upload_service import save_uploaded_file
from services.extract_service import extract_text_from_file
from services.search_service import search_documents, initialize_index
from services.summarize_service import summarize_document

### 📌 1. Run FAISS Index Initialization at Startup ###
@app.on_event("startup")
async def startup_event():
    await initialize_index()  # ✅ Initialize FAISS index


### 📌 2. Upload and Save Files ###
@app.post("/upload/")
async def upload_files(files: list[UploadFile]):
    saved_files = []
    for file in files:
        file_path = await save_uploaded_file(file)

        # Run text extraction in a separate thread (to avoid blocking)
        loop = asyncio.get_event_loop()
        text = await loop.run_in_executor(None, extract_text_from_file, file_path)

        if text:
            document = {"filename": file.filename, "content": text}
            await documents_collection.insert_one(document)

        saved_files.append(file.filename)

    return {"message": "Files uploaded successfully", "files": saved_files}


### 📌 3. AI-Based Search ###
@app.get("/search/")
async def search(query: str):
    return await search_documents(query)


### 📌 4. AI Summarization ###
@app.get("/summarize/")
async def summarize(doc_id: str):
    return await summarize_document(doc_id)


@app.get("/documents/")
async def get_documents():
    documents = await documents_collection.find().to_list(None)  # Fetch all documents
    return [
        {"id": str(doc["_id"]), "filename": doc["filename"]}
        for doc in documents
    ]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

