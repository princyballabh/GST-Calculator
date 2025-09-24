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

app = FastAPI(title="GST Calculator Demo")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
async def root():
    return {"message": "GST Calculator API is running!", "version": "1.0.0", "endpoints": ["/docs", "/api/calc", "/admin/upload-pdf"]}

@app.get("/test")
async def test():
    try:
        # Test database connection
        count = rates_col.count_documents({})
        return {"status": "OK", "db_connection": "Success", "documents_count": count}
    except Exception as e:
        return {"status": "Error", "db_connection": "Failed", "error": str(e)}

@app.post("/admin/upload-pdf")
async def upload_pdf(file: UploadFile = File(...), admin_key: str = Form("")):
    # Optional simple admin auth - disabled for testing
    # expected_key = os.getenv("ADMIN_KEY")
    # if expected_key and admin_key != expected_key:
    #     raise HTTPException(status_code=403, detail=f"Invalid admin key. Expected: {expected_key}, Got: {admin_key}")

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
        existing = rates_col.find_one({"hsn": hsn, "description": desc})
        if existing:
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
                updates.append({"hsn": hsn, "old": existing.get("rate"), "new": rate})
        else:
            rates_col.insert_one({
                "hsn": hsn,
                "description": desc,
                "keywords": keywords,
                "rate": rate,
                "last_updated": datetime.datetime.utcnow(),
                "source_pdf": save_path
            })
            updates.append({"hsn": hsn, "old": None, "new": rate})

    return {"ok": True, "parsed_rows": len(parsed), "updates": updates}

# Calculator API Model
class CalcRequest(BaseModel):
    description: str
    price: float
    inclusive: bool = False
    top_k: int = 3

def calculate_gst(price, rate, inclusive=False):
    r = float(rate)
    if inclusive:
        base = price / (1 + r/100)
        gst = price - base
        total = price
    else:
        gst = price * r/100
        base = price
        total = price + gst
    return {"base": round(base,2), "gst": round(gst,2), "total": round(total,2)}

@app.post("/api/calc")
def api_calc(req: CalcRequest):
    try:
        q = req.description.lower()
        
        # Check if database has any documents
        all_docs = list(rates_col.find({}, {"description":1, "hsn":1, "rate":1}))
        
        if not all_docs:
            return {"matched": False, "error": "No GST rates found in database. Please upload a PDF first.", "suggestions": []}
        
        descriptions = [d["description"] for d in all_docs]

        match = process.extractOne(q, descriptions, scorer=fuzz.WRatio)
        if match:
            best_desc, score, idx = match
            best_doc = all_docs[idx]
        else:
            best_doc = None
            score = 0

        if best_doc and score >= 65:
            rate = best_doc["rate"]
            calc = calculate_gst(req.price, rate, req.inclusive)
            
            # Log the calculation
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
            
            return {"matched": True, "score": score, "match": best_doc, "calc": calc}
        else:
            suggestions = process.extract(q, descriptions, limit=req.top_k, scorer=fuzz.WRatio)
            sug = [{"description": s[0], "score": s[1]} for s in suggestions]
            return {"matched": False, "suggestions": sug}
    
    except Exception as e:
        print(f"Error in api_calc: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
