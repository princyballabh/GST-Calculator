from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from rapidfuzz import process, fuzz
import os

# Load environment variables
load_dotenv()

# Import database connection
try:
    from db import rates_col
    DATABASE_CONNECTED = True
except ImportError:
    DATABASE_CONNECTED = False
    print("Warning: Database connection not available")

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CalcRequest(BaseModel):
    description: str
    price: float
    inclusive: bool = False

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/test")
def test():
    return {"status": "working"}

@app.get("/debug/{product_name}")
def debug_product(product_name: str):
    """Debug endpoint to see what's in the database for a product"""
    if not DATABASE_CONNECTED:
        return {"error": "Database not connected"}
    
    try:
        # Search for products containing the search term
        query = {"description": {"$regex": product_name, "$options": "i"}}
        results = list(rates_col.find(query, {"_id": 0}))
        
        # Also do fuzzy search like the main calc function
        all_docs = list(rates_col.find({}, {"description": 1, "hsn": 1, "rate": 1}))
        descriptions = [d["description"] for d in all_docs]
        fuzzy_matches = process.extract(product_name.lower(), descriptions, limit=5, scorer=fuzz.WRatio)
        
        fuzzy_results = []
        for desc, score, idx in fuzzy_matches:
            doc = all_docs[idx]
            fuzzy_results.append({
                "description": doc["description"],
                "hsn": doc.get("hsn"),
                "rate": doc["rate"],
                "score": score
            })
        
        return {
            "search_term": product_name,
            "exact_matches": results,
            "fuzzy_matches": fuzzy_results,
            "total_products_in_db": len(all_docs)
        }
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/calc")
def calc(request: CalcRequest):
    try:
        # Try to find the product in database
        if DATABASE_CONNECTED:
            # Search for matching product in database
            q = request.description.lower()
            all_docs = list(rates_col.find({}, {"description": 1, "hsn": 1, "rate": 1}))
            
            if all_docs:
                descriptions = [d["description"] for d in all_docs]
                match = process.extractOne(q, descriptions, scorer=fuzz.WRatio)
                
                if match and match[1] >= 65:  # If match score >= 65%
                    best_desc, score, idx = match
                    best_doc = all_docs[idx]
                    
                    # Get CGST rate from database and double it for total GST
                    cgst_rate = best_doc["rate"]
                    total_gst_rate = cgst_rate * 2  # CGST + SGST = Total GST
                    
                    # Debug logging
                    print(f"DEBUG - Search: '{q}' matched '{best_desc}' (score: {score})")
                    print(f"DEBUG - HSN: {best_doc.get('hsn')}, CGST Rate: {cgst_rate}%, Total GST: {total_gst_rate}%")
                    
                    price = request.price
                    
                    if request.inclusive:
                        # Price includes GST
                        base = price / (1 + total_gst_rate/100)
                        gst = price - base
                        total = price
                    else:
                        # Price excludes GST
                        gst = price * total_gst_rate/100
                        base = price
                        total = price + gst
                    
                    return {
                        "matched": True,
                        "score": score,
                        "match": {
                            "hsn": best_doc.get("hsn", "N/A"),
                            "description": best_doc["description"],
                            "rate": total_gst_rate,
                            "cgst_rate": cgst_rate,
                            "sgst_rate": cgst_rate
                        },
                        "calc": {
                            "base": round(base, 2),
                            "gst": round(gst, 2),
                            "total": round(total, 2),
                            "rate": total_gst_rate,
                            "cgst": round(gst/2, 2),
                            "sgst": round(gst/2, 2)
                        }
                    }
        
        # Fallback: No database connection or no match found
        # Use sample rate for demonstration
        cgst_rate = 9.0
        total_gst_rate = cgst_rate * 2  # CGST + SGST = Total GST
        
        price = request.price
        
        if request.inclusive:
            # Price includes GST
            base = price / (1 + total_gst_rate/100)
            gst = price - base
            total = price
        else:
            # Price excludes GST
            gst = price * total_gst_rate/100
            base = price
            total = price + gst
        
        return {
            "matched": False,
            "message": "No exact match found in database, using sample rate",
            "calc": {
                "base": round(base, 2),
                "gst": round(gst, 2),
                "total": round(total, 2),
                "rate": total_gst_rate,
                "cgst": round(gst/2, 2),
                "sgst": round(gst/2, 2)
            }
        }
        
    except Exception as e:
        print(f"Error in calc: {e}")
        return {"error": f"Calculation failed: {str(e)}"}
