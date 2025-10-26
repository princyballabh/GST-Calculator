import os
import re
import datetime
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rapidfuzz import process, fuzz
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from db import rates_col, history_col, logs_col
from pdf_parser import parse_pdf_tables
from seed_database import seed_database

app = FastAPI(title="GST Calculator Demo")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev, or ["http://localhost:3000"] for strict mode
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.on_event("startup")
async def startup_event():
    """Initialize database with seed data on startup"""
    print("🚀 Starting GST Calculator API...")
    seeded_count = seed_database()
    if seeded_count > 0:
        print(f"✅ Database initialized with {seeded_count} GST rates")
    else:
        print("📊 Database ready (no seeding required)")

@app.get("/")
async def root():
    return {"message": "GST Calculator API is running!", "version": "1.0.0", "endpoints": ["/docs", "/api/calc", "/admin/upload-pdf"]}

@app.get("/api/status")
async def get_status():
    """Get database and application status"""
    from seed_database import get_database_stats
    stats = get_database_stats()
    return {
        "status": "running",
        "database": stats,
        "message": "GST Calculator ready for use" if stats.get("total_rates", 0) > 0 else "Upload PDF to populate database"
    }

@app.get("/test")
async def test():
    try:
        count = rates_col.count_documents({})
        return {"status": "OK", "db_connection": "Success", "documents_count": count}
    except Exception as e:
        return {"status": "Error", "db_connection": "Failed", "error": str(e)}

@app.post("/admin/upload-pdf")
async def upload_pdf(file: UploadFile = File(...), admin_key: str = Form("")):
    save_path = os.path.join(
        UPLOAD_DIR,
        f"{datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{file.filename}"
    )
    with open(save_path, "wb") as f:
        f.write(await file.read())

    # Parse PDF file
    parsed = parse_pdf_tables(save_path)
    if not parsed:
        return JSONResponse({"ok": False, "message": "No rows parsed. Check PDF."})

    updates = []
    for hsn, desc, rate in parsed:
        keywords = [w.lower() for w in re.findall(r"\w+", desc) if len(w) > 2][:20]
        
        # Strategy 1: Try exact match first (HSN + description)
        existing = rates_col.find_one({"hsn": hsn, "description": desc})
        
        if existing:
            # Exact match found - update if rate changed
            if existing.get("rate") != rate:
                history_col.insert_one({
                    "hsn": hsn,
                    "description": desc,
                    "old_rate": existing.get("rate"),
                    "new_rate": rate,
                    "changed_at": datetime.datetime.utcnow(),
                    "source_pdf": save_path
                })
                rates_col.update_one(
                    {"_id": existing["_id"]},
                    {"$set": {"rate": rate, "last_updated": datetime.datetime.utcnow(), "source_pdf": save_path}}
                )
                updates.append({"hsn": hsn, "description": desc, "old": existing.get("rate"), "new": rate})
        else:
            # Strategy 2: Check if there's a primary entry for this HSN that should be updated
            # Look for entries with same HSN but different descriptions
            hsn_entries = list(rates_col.find({"hsn": hsn}))
            
            # If we find entries with the same HSN, we need to decide whether to update or create new
            # For known product categories, update the main entry
            main_entry = None
            
            # Check if this is a known product category that should update existing entries
            desc_lower = desc.lower()
            known_products = {
                'pan masala': '2106',
                'tissue': '168',
                'toilet paper': '168'
            }
            
            should_update_existing = False
            for product, product_hsn in known_products.items():
                if product in desc_lower and hsn == product_hsn:
                    should_update_existing = True
                    break
            
            if should_update_existing and hsn_entries:
                # Find the best entry to update (prefer entries with 14% for pan masala, 9% for tissues, etc.)
                target_rates = {'2106': 14.0, '168': 9.0}
                target_rate = target_rates.get(hsn)
                
                if target_rate:
                    main_entry = next((entry for entry in hsn_entries if entry.get('rate') == target_rate), None)
                
                # If no target rate match, pick the first entry
                if not main_entry and hsn_entries:
                    main_entry = hsn_entries[0]
            
            if main_entry and should_update_existing:
                # Update existing main entry
                if main_entry.get("rate") != rate:
                    history_col.insert_one({
                        "hsn": hsn,
                        "description": main_entry["description"],
                        "old_rate": main_entry.get("rate"),
                        "new_rate": rate,
                        "changed_at": datetime.datetime.utcnow(),
                        "source_pdf": save_path,
                        "update_reason": f"Updated via new PDF entry: {desc}"
                    })
                    rates_col.update_one(
                        {"_id": main_entry["_id"]},
                        {"$set": {"rate": rate, "last_updated": datetime.datetime.utcnow(), "source_pdf": save_path}}
                    )
                    updates.append({"hsn": hsn, "description": main_entry["description"], "old": main_entry.get("rate"), "new": rate})
            else:
                # Create new entry
                rates_col.insert_one({
                    "hsn": hsn,
                    "description": desc,
                    "keywords": keywords,
                    "rate": rate,
                    "last_updated": datetime.datetime.utcnow(),
                    "source_pdf": save_path
                })
                updates.append({"hsn": hsn, "description": desc, "old": None, "new": rate})

    return {"ok": True, "parsed_rows": len(parsed), "updates": updates}

# Calculator API Model
class CalcRequest(BaseModel):
    description: str
    price: float
    inclusive: bool = False
    top_k: int = 3

def calculate_gst(price, rate, inclusive=False):
    """
    Calculate GST where 'rate' is the CGST rate from database.
    Total GST = CGST + SGST = 2 * CGST rate
    """
    cgst_rate = float(rate)  # Rate from DB is CGST rate
    sgst_rate = cgst_rate    # SGST rate is same as CGST rate
    total_gst_rate = cgst_rate + sgst_rate  # Total GST rate
    
    if inclusive:
        # Price includes total GST
        base = price / (1 + total_gst_rate/100)
        total_gst_amount = price - base
        cgst_amount = total_gst_amount / 2
        sgst_amount = total_gst_amount / 2
        total = price
    else:
        # Price is base price, add GST
        base = price
        cgst_amount = price * cgst_rate/100
        sgst_amount = price * sgst_rate/100
        total_gst_amount = cgst_amount + sgst_amount
        total = price + total_gst_amount
    
    return {
        "base": round(base, 2),
        "cgst": round(cgst_amount, 2),
        "sgst": round(sgst_amount, 2), 
        "gst": round(total_gst_amount, 2),  # Total GST amount
        "total": round(total, 2),
        "rate": total_gst_rate  # Total GST rate for display
    }

def improved_matching(query, all_docs):
    query_lower = query.lower()
    query_words = set(query_lower.split())
    
    # Product-specific mappings for known categories
    product_mappings = {
        'pan masala': {'hsn': '2106', 'rate': 14.0},
        'facial tissue': {'hsn': '168', 'rate': 9.0},
        'tissue paper': {'hsn': '168', 'rate': 9.0},
        'toilet paper': {'hsn': '168', 'rate': 9.0},
    }
    
    # Check if query matches any known product mapping
    for product_key, mapping in product_mappings.items():
        if product_key in query_lower:
            # Find the best matching entry with this HSN and rate
            hsn_matches = [doc for doc in all_docs if doc.get('hsn') == mapping['hsn'] and doc.get('rate') == mapping['rate']]
            if hsn_matches:
                return hsn_matches[0], 100.0, all_docs.index(hsn_matches[0])
    
    # Original improved matching logic
    best_score = 0
    best_doc = None
    best_idx = None

    for idx, doc in enumerate(all_docs):
        desc = doc["description"].lower()
        desc_words = set(desc.split())
        exact_matches = len(query_words.intersection(desc_words))
        if exact_matches >= 2:
            fuzzy_score = fuzz.WRatio(query_lower, desc)
            combined_score = fuzzy_score + (exact_matches * 10)
            if combined_score > best_score:
                best_score = combined_score
                best_doc = doc
                best_idx = idx

    if best_score < 70:
        descriptions = [d["description"] for d in all_docs]
        match = process.extractOne(query_lower, descriptions, scorer=fuzz.WRatio)
        if match:
            best_desc, fuzzy_score, idx = match
            best_doc = all_docs[idx]
            best_score = fuzzy_score
            best_idx = idx

    return best_doc, best_score, best_idx

def sanitize_doc(doc):
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc

@app.post("/api/calc")
def api_calc(req: CalcRequest):
    try:
        q = req.description.lower()
        all_docs = list(rates_col.find({}, {"description":1, "hsn":1, "rate":1}))
        if not all_docs:
            return {"matched": False, "error": "No GST rates found in database. Please upload a PDF first.", "suggestions": []}
        best_doc, score, best_idx = improved_matching(q, all_docs)
        if best_doc is None:
            score = 0

        if best_doc and score >= 65:
            rate = best_doc["rate"]
            calc = calculate_gst(req.price, rate, req.inclusive)
            try:
                logs_col.insert_one({
                    "input_description": req.description,
                    "matched_description": best_doc["description"],
                    "hsn": best_doc.get("hsn"),
                    "rate": rate,
                    "price": req.price,
                    "inclusive": req.inclusive,
                    "result": calc,
                    "created_at": datetime.datetime.utcnow()
                })
            except Exception as log_error:
                print(f"Failed to log calculation: {log_error}")

            best_doc = sanitize_doc(best_doc)
            return {"matched": True, "score": score, "match": best_doc, "calc": calc}
        else:
            descriptions = [d["description"] for d in all_docs]
            suggestions = process.extract(q, descriptions, limit=req.top_k, scorer=fuzz.WRatio)
            sug = [{"description": s[0], "score": s[1]} for s in suggestions]
            return {"matched": False, "suggestions": sug}
    except Exception as e:
        print(f"Error in api_calc: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
