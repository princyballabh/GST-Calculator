# GST Calculator

A web application to calculate GST rates for products by parsing PDF documents and using fuzzy matching.

## Tech Stack

- **Backend**: Python + FastAPI
- **PDF Parsing**: pdfplumber
- **Fuzzy Matching**: rapidfuzz
- **Database**: MongoDB
- **Frontend**: React/Next.js

## Project Structure

```
GST-Calculator/
├─ backend/
│  ├─ main.py            # FastAPI app (upload + parse + calc endpoints)
│  ├─ pdf_parser.py      # parsing helpers
│  ├─ db.py              # MongoDB connection + helper functions
│  ├─ requirements.txt   # Python dependencies
│  └─ uploads/           # saved uploaded PDFs
└─ frontend/
   ├─ pages/
   │  ├─ index.jsx      # user calculator page
   │  └─ admin.jsx      # admin upload page
   └─ package.json      # Node.js dependencies
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 16+
- MongoDB (local or Atlas)

### Backend Setup

1. Navigate to backend directory:

   ```bash
   cd backend
   ```

2. Create and activate virtual environment:

   ```bash
   python -m venv .venv
   .venv\Scripts\Activate.ps1  # Windows PowerShell
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start MongoDB (if running locally)

5. Run the FastAPI server:

   ```bash
   uvicorn main:app --reload
   ```

   Backend will be available at: http://localhost:8000

### Frontend Setup

1. Navigate to frontend directory:

   ```bash
   cd frontend
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Start the development server:

   ```bash
   npm run dev
   ```

   Frontend will be available at: http://localhost:3000

## API Endpoints

- `GET /` - API status
- `POST /upload-pdf` - Upload and parse GST PDF
- `GET /calculate/{product_name}` - Calculate GST rate for product
- `GET /rates` - Get all GST rates

## MongoDB Collections

### gst_rates

```json
{
  "_id": "ObjectId",
  "hsn": "0505",
  "description": "Skins and other parts of birds...",
  "keywords": ["bird", "feather", "powder"],
  "rate": 2.5,
  "last_updated": "2025-09-24T12:00:00Z",
  "source_pdf": "uploads/gst_2025_09_24.pdf"
}
```

### rate_history

```json
{
  "category": "0505",
  "old_rate": 5.0,
  "new_rate": 2.5,
  "changed_at": "2025-09-24T12:00:00Z",
  "source_pdf": "uploads/gst_2025_09_24.pdf"
}
```

### product_logs

```json
{
  "product_name": "bird feathers",
  "hsn_code": "0505",
  "rate": 2.5,
  "calculated_at": "2025-09-24T12:00:00Z",
  "ip_address": "localhost"
}
```

## Usage

1. Start both backend and frontend servers
2. Go to http://localhost:3000/admin to upload GST PDF files
3. Go to http://localhost:3000 to calculate GST rates for products
4. The system will use fuzzy matching to find the best rate for your product

## Environment Variables

- `MONGO_URL`: MongoDB connection string (default: mongodb://localhost:27017/)

## Notes

- The PDF parser is basic and may need adjustment based on your PDF format
- Fuzzy matching threshold is set to 70% - adjust as needed
- Make sure MongoDB is running before starting the backend
