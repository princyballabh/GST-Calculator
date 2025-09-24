import pdfplumber
import re
from rapidfuzz import fuzz
from typing import List, Dict, Optional
from datetime import datetime

def parse_pdf_for_gst_rates(pdf_path: str) -> List[Dict]:
    """
    Parse PDF and extract GST rates with HSN codes
    Returns list of dictionaries with rate information
    """
    rates = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    # Basic pattern matching for HSN codes and rates
                    # This is a simplified version - you'll need to adjust based on actual PDF format
                    lines = text.split('\n')
                    
                    for line in lines:
                        # Look for patterns like: HSN_CODE DESCRIPTION RATE%
                        hsn_match = re.search(r'(\d{4,8})\s+(.+?)\s+(\d+\.?\d*)%?', line)
                        if hsn_match:
                            hsn_code = hsn_match.group(1)
                            description = hsn_match.group(2).strip()
                            rate = float(hsn_match.group(3))
                            
                            # Extract keywords from description for fuzzy matching
                            keywords = extract_keywords(description)
                            
                            rate_info = {
                                "hsn": hsn_code,
                                "description": description,
                                "keywords": keywords,
                                "rate": rate,
                                "last_updated": datetime.now().isoformat(),
                                "page_number": page_num + 1
                            }
                            rates.append(rate_info)
    
    except Exception as e:
        print(f"Error parsing PDF: {e}")
        return []
    
    return rates

def extract_keywords(description: str) -> List[str]:
    """
    Extract keywords from product description for fuzzy matching
    """
    # Remove common words and split into keywords
    stop_words = {'and', 'or', 'the', 'of', 'in', 'on', 'at', 'to', 'for', 'with', 'by'}
    
    # Clean and split description
    words = re.findall(r'\b\w+\b', description.lower())
    keywords = [word for word in words if len(word) > 2 and word not in stop_words]
    
    return keywords[:10]  # Limit to top 10 keywords

def search_product_rate(db, product_name: str, threshold: int = 70) -> Optional[Dict]:
    """
    Search for product GST rate using fuzzy matching
    """
    try:
        # Get all rates from database
        all_rates = list(db.gst_rates.find({}))
        
        best_match = None
        best_score = 0
        
        product_lower = product_name.lower()
        
        for rate in all_rates:
            # Check direct description match
            desc_score = fuzz.partial_ratio(product_lower, rate['description'].lower())
            
            # Check keyword matches
            keyword_scores = []
            for keyword in rate.get('keywords', []):
                keyword_score = fuzz.partial_ratio(product_lower, keyword)
                keyword_scores.append(keyword_score)
            
            # Take the best keyword score
            max_keyword_score = max(keyword_scores) if keyword_scores else 0
            
            # Combined score (weighted)
            combined_score = max(desc_score * 0.7 + max_keyword_score * 0.3, max_keyword_score)
            
            if combined_score > best_score and combined_score >= threshold:
                best_score = combined_score
                best_match = rate
        
        return best_match
    
    except Exception as e:
        print(f"Error searching product rate: {e}")
        return None
