from pymongo import MongoClient
from datetime import datetime
from typing import Dict, Optional
import os

# MongoDB connection settings
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/")
DATABASE_NAME = "gst_calculator"

def get_database():
    """Get MongoDB database connection"""
    try:
        client = MongoClient(MONGO_URL)
        db = client[DATABASE_NAME]
        return db
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

def save_gst_rate(db, rate_data: Dict) -> bool:
    """
    Save or update GST rate in database
    """
    try:
        collection = db.gst_rates
        
        # Check if HSN already exists
        existing = collection.find_one({"hsn": rate_data["hsn"]})
        
        if existing:
            # Save old rate to history
            save_rate_history(db, existing, rate_data)
            
            # Update existing rate
            collection.update_one(
                {"hsn": rate_data["hsn"]},
                {"$set": rate_data}
            )
        else:
            # Insert new rate
            collection.insert_one(rate_data)
        
        return True
    
    except Exception as e:
        print(f"Error saving GST rate: {e}")
        return False

def save_rate_history(db, old_rate: Dict, new_rate: Dict):
    """
    Save rate change history
    """
    try:
        collection = db.rate_history
        
        history_record = {
            "category": old_rate["hsn"],
            "old_rate": old_rate["rate"],
            "new_rate": new_rate["rate"],
            "changed_at": datetime.now().isoformat(),
            "source_pdf": new_rate.get("source_pdf", ""),
            "old_description": old_rate.get("description", ""),
            "new_description": new_rate.get("description", "")
        }
        
        collection.insert_one(history_record)
    
    except Exception as e:
        print(f"Error saving rate history: {e}")

def get_gst_rate(db, hsn_code: str) -> Optional[Dict]:
    """
    Get GST rate by HSN code
    """
    try:
        collection = db.gst_rates
        rate = collection.find_one({"hsn": hsn_code}, {"_id": 0})
        return rate
    
    except Exception as e:
        print(f"Error getting GST rate: {e}")
        return None

def log_calculation(db, product_name: str, rate: float, hsn_code: str):
    """
    Log product calculation for audit
    """
    try:
        collection = db.product_logs
        
        log_record = {
            "product_name": product_name,
            "hsn_code": hsn_code,
            "rate": rate,
            "calculated_at": datetime.now().isoformat(),
            "ip_address": "localhost"  # You can add actual IP tracking
        }
        
        collection.insert_one(log_record)
    
    except Exception as e:
        print(f"Error logging calculation: {e}")

def get_calculation_logs(db, limit: int = 100):
    """
    Get recent calculation logs
    """
    try:
        collection = db.product_logs
        logs = list(collection.find({}, {"_id": 0}).sort("calculated_at", -1).limit(limit))
        return logs
    
    except Exception as e:
        print(f"Error getting calculation logs: {e}")
        return []
