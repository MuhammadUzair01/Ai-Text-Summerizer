from motor.motor_asyncio import AsyncIOMotorClient
MOGO_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MOGO_URL)
db = client.sumerizer_db
summary_collection = db.get_collection("summaries")
