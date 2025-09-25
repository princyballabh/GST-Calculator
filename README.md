# 🧮 GST Calculator Pro

A professional web application for calculating GST rates with elegant UI/UX, PDF parsing capabilities, and intelligent fuzzy matching for accurate tax calculations.

## ✨ Features

- 🎨 **Beautiful UI/UX**: Modern, responsive design with elegant color scheme
- 📄 **PDF Upload**: Parse GST rate PDFs and automatically update database
- 🔍 **Smart Matching**: Fuzzy matching to find best GST rates for products
- 🔐 **Admin Panel**: Secure admin interface for rate management
- 📱 **Mobile Responsive**: Works perfectly on all devices
- ⚡ **Real-time Calculations**: Instant GST calculations with detailed breakdowns

## 🛠 Tech Stack

- **Backend**: Python + FastAPI + uvicorn
- **PDF Parsing**: pdfplumber
- **Fuzzy Matching**: rapidfuzz (65% threshold)
- **Database**: MongoDB Atlas
- **Frontend**: React + Next.js
- **Styling**: Custom CSS with elegant color palette
- **Environment**: python-dotenv

## 📁 Project Structure

```
GST-Calculator/
├─ backend/
│  ├─ main.py            # Main FastAPI application
│  ├─ test_server.py     # Testing server (port 8003)
│  ├─ pdf_parser.py      # PDF parsing utilities
│  ├─ db.py              # MongoDB connection & collections
│  ├─ requirements.txt   # Python dependencies
│  ├─ .env              # Environment variables (not in repo)
│  └─ uploads/           # Uploaded PDF storage
└─ frontend/
   ├─ pages/
   │  ├─ index.jsx      # Main calculator page
   │  ├─ admin.jsx      # Admin upload interface
   │  ├─ 404.jsx        # Custom error page
   │  ├─ _app.js        # Next.js app wrapper
   │  └─ _document.js   # HTML document structure
   ├─ styles/
   │  └─ globals.css    # Global styling & theme
   └─ package.json      # Node.js dependencies
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- MongoDB Atlas account (or local MongoDB)

### 🔧 Setup Instructions

#### 1. Clone & Environment Setup

```bash
git clone https://github.com/princyballabh/GST-Calculator.git
cd GST-Calculator

# Create virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows PowerShell
# or
source .venv/bin/activate   # Linux/Mac
```

#### 2. Backend Setup

```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Create .env file with your MongoDB connection
echo "MONGO_URL=your_mongodb_connection_string" > .env
echo "ADMIN_KEY=your_admin_password" >> .env

# Start the server (recommended: use test_server.py)
python -m uvicorn test_server:app --reload --port 8003
```

#### 3. Frontend Setup

```bash
cd ../frontend

# Install Node.js dependencies
npm install

# Start development server
npm run dev
```

### 🌐 Access Points

- **Main Calculator**: http://localhost:3000
- **Admin Panel**: http://localhost:3000/admin
- **Backend API**: http://localhost:8003
- **API Docs**: http://localhost:8003/docs

## 🔌 API Endpoints

### Main Endpoints (port 8003)

- `GET /` - API health check
- `POST /api/calc` - Calculate GST for product
- `POST /api/upload` - Upload and parse GST PDF
- `GET /debug/{product}` - Debug product matching

### Request Examples

```javascript
// Calculate GST
POST /api/calc
{
  "description": "cheese",
  "price": 100,
  "inclusive": false
}

// Upload PDF
POST /api/upload
FormData: { file: gst_rates.pdf }
```

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

## 🎨 Color Palette & Design

The application uses a sophisticated color scheme:

- **Primary Dark**: `#6F1D1B` - Deep burgundy for headings
- **Secondary**: `#BB9457` - Warm gold for accents
- **Tertiary**: `#432818` - Rich brown for text
- **Accent**: `#99582A` - Medium brown for buttons
- **Light**: `#FFE6A7` - Cream for backgrounds

## 🔒 Environment Variables

Create `backend/.env` file (see `.env.example`):

```env
MONGO_URL=your_mongodb_connection_string
ADMIN_KEY=your_secure_admin_password
```

## 🗄️ Database Collections

### `rates_col` (GST Rates)

```json
{
  "hsn": "0406",
  "description": "Cheese, other than chena or paneer",
  "rate": 2.5,
  "keywords": ["cheese", "dairy"]
}
```

### `history_col` (Rate Changes)

```json
{
  "hsn": "0406",
  "old_rate": 5.0,
  "new_rate": 2.5,
  "changed_at": "2024-09-25T10:30:00Z"
}
```

## 📱 Screenshots

- **Calculator Page**: Elegant form with real-time GST calculations
- **Admin Panel**: Secure PDF upload with drag & drop
- **Results Display**: Detailed breakdown with CGST/SGST split
- **Mobile Responsive**: Perfect experience on all devices

## 🚀 Deployment

### Production Build

```bash
# Backend
cd backend
pip install -r requirements.txt
python -m uvicorn test_server:app --host 0.0.0.0 --port 8003

# Frontend
cd frontend
npm run build
npm start
```

### Docker (Optional)

```dockerfile
# See docker-compose.yml for containerized deployment
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📝 Notes

- **PDF Format**: Parser works with standard GST rate PDF formats
- **Fuzzy Matching**: 65% threshold for product name matching
- **Rate Storage**: CGST rates are doubled for total GST calculation
- **Security**: Admin panel requires password authentication
- **Performance**: MongoDB indexing for fast lookups

## 📄 License

This project is licensed under the ISC License.

## 👤 Author

**Princy Ballabh**

- GitHub: [@princyballabh](https://github.com/princyballabh)

---

⭐ **Star this repo if you found it helpful!** ⭐
