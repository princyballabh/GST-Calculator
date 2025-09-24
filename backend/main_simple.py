import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="GST Calculator Demo")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "GST Calculator API is running!", "version": "1.0.0"}

@app.get("/test")
async def test():
    return {"status": "OK", "message": "Server is working"}

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
        # For now, return a sample calculation without database
        # This will help us test if CORS is working
        sample_rate = 18.0  # 18% GST
        calc = calculate_gst(req.price, sample_rate, req.inclusive)
        
        return {
            "matched": True, 
            "score": 100, 
            "match": {
                "hsn": "sample", 
                "description": f"Sample match for: {req.description}", 
                "rate": sample_rate
            }, 
            "calc": calc
        }
    
    except Exception as e:
        print(f"Error in api_calc: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
