from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
from datetime import datetime
from db import get_database, save_gst_rate, get_gst_rate, log_calculation
from pdf_parser import parse_pdf_for_gst_rates, search_product_rate

app = FastAPI(title="GST Calculator API", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure uploads directory exists
os.makedirs("uploads", exist_ok=True)

@app.get("/")
async def root():
    return {"message": "GST Calculator API"}

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload and parse GST PDF for rate extraction"""
    try:
        # Save uploaded file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"gst_{timestamp}_{file.filename}"
        file_path = os.path.join("uploads", filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Parse PDF and extract rates
        rates = parse_pdf_for_gst_rates(file_path)
        
        # Save rates to database
        db = get_database()
        saved_count = 0
        for rate in rates:
            rate["source_pdf"] = file_path
            save_gst_rate(db, rate)
            saved_count += 1
        
        return {
            "message": f"PDF processed successfully. {saved_count} rates saved.",
            "filename": filename,
            "rates_count": saved_count
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

@app.get("/calculate/{product_name}")
async def calculate_gst(product_name: str):
    """Calculate GST rate for a product"""
    try:
        db = get_database()
        rate_info = search_product_rate(db, product_name)
        
        if not rate_info:
            return {"error": "Product not found", "rate": None}
        
        # Log the calculation
        log_calculation(db, product_name, rate_info["rate"], rate_info["hsn"])
        
        return {
            "product": product_name,
            "hsn": rate_info["hsn"],
            "description": rate_info["description"],
            "rate": rate_info["rate"],
            "matched": True
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating GST: {str(e)}")

@app.get("/rates")
async def get_all_rates(limit: int = 100):
    """Get all GST rates"""
    try:
        db = get_database()
        rates = list(db.gst_rates.find({}, {"_id": 0}).limit(limit))
        return {"rates": rates, "count": len(rates)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching rates: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
