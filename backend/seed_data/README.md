# Seed Data Folder

This folder contains PDF files with GST rates that will automatically populate the database when the application starts.

## How it works:
1. When the app starts, it checks if the database is empty
2. If empty, it processes all PDF files in this folder
3. GST rates are extracted and inserted into the database
4. Users can immediately use the calculator without uploading PDFs

## Adding seed data:
1. Place your GST schedule PDFs in this folder
2. Name them descriptively (e.g., `gst_schedule_2025.pdf`)
3. The app will automatically process them on startup

## Current seed files:
- Add your GST PDF files here before deployment