"""
Script to copy a good GST PDF from previous uploads to seed_data
Run this to prepare your seed data before deployment
"""

import shutil
import os

# You should manually copy your best GST PDF to seed_data folder
print("📋 To set up seed data:")
print("1. Copy your best GST PDF file to backend/seed_data/")
print("2. Rename it to 'default_gst_rates.pdf'")
print("3. This will automatically populate the database on startup")
print()
print("Example command:")
print("copy 'path_to_your_best_gst_pdf.pdf' 'backend/seed_data/default_gst_rates.pdf'")
print()
print("✅ After this, users can immediately use the calculator without uploading PDFs!")