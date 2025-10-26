"""
Database seeding script - Populates GST rates on app startup
This ensures the calculator works immediately without requiring PDF uploads
"""

from db import rates_col
from pdf_parser import parse_pdf_tables
import os
import glob

def seed_database():
    """
    Seeds the database with GST rates from pre-included PDFs
    Only runs if database is empty
    """
    try:
        # Check if database already has data
        existing_count = rates_col.count_documents({})
        if existing_count > 0:
            print(f"✅ Database already contains {existing_count} GST rates")
            return existing_count
        
        print("📊 Database is empty. Seeding with default GST rates...")
        
        # Look for seed PDFs in the seed_data folder
        seed_folder = "seed_data"
        if not os.path.exists(seed_folder):
            print("❌ No seed_data folder found. Skipping database seeding.")
            return 0
            
        pdf_files = glob.glob(os.path.join(seed_folder, "*.pdf"))
        if not pdf_files:
            print("❌ No PDF files found in seed_data folder.")
            return 0
            
        total_inserted = 0
        
        for pdf_file in pdf_files:
            print(f"📄 Processing: {os.path.basename(pdf_file)}")
            
            try:
                # Parse the PDF
                parsed_data = parse_pdf_tables(pdf_file)
                
                # Insert into database
                for hsn, description, rate in parsed_data:
                    if hsn and description and rate is not None:
                        # Check if entry already exists
                        existing = rates_col.find_one({"hsn": hsn, "description": description})
                        
                        if not existing:
                            rates_col.insert_one({
                                "hsn": hsn,
                                "description": description,
                                "rate": float(rate),
                                "source": f"seed_{os.path.basename(pdf_file)}",
                                "created_at": "seed_data"
                            })
                            total_inserted += 1
                            
            except Exception as e:
                print(f"❌ Error processing {pdf_file}: {str(e)}")
                continue
        
        print(f"✅ Database seeded with {total_inserted} GST rates")
        return total_inserted
        
    except Exception as e:
        print(f"❌ Error during database seeding: {str(e)}")
        return 0

def get_database_stats():
    """Returns current database statistics"""
    try:
        total_rates = rates_col.count_documents({})
        seed_rates = rates_col.count_documents({"source": {"$regex": "seed_"}})
        return {
            "total_rates": total_rates,
            "seed_rates": seed_rates,
            "user_uploaded": total_rates - seed_rates
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Run seeding when script is executed directly
    seed_database()
    stats = get_database_stats()
    print(f"📊 Final stats: {stats}")