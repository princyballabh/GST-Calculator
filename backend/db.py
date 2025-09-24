import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = MongoClient(MONGO_URL)
db = client['gstdb']
rates_col = db['gst_rates']
history_col = db['rate_history']
logs_col = db['product_logs']
