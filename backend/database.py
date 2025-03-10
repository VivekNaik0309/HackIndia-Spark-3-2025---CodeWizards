from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from bson import ObjectId

# Load environment variables
load_dotenv()

# MongoDB Atlas Connection
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "pdfscanner"  # Ensure this matches your MongoDB cluster database name

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
documents_collection = db["codewizards"]  # Collection to store uploaded documents



client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["your_database_name"]
collection = db["your_collection_name"]

async def get_document_by_id(doc_id: str):
    doc = await collection.find_one({"_id": ObjectId(doc_id)})
    return doc
