import pdfplumber
import re

def parse_pdf_tables(path):
    rows_out = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                for row in table:
                    row = [c.strip() if c else "" for c in row]
                    rate = None
                    hsn = None
                    desc = None

                    # Find rate (last numeric column with %)
                    for c in reversed(row):
                        if c and re.search(r"\d+(\.\d+)?\s*%?", c):
                            rate = re.sub(r"[^\d.]", "", c)
                            break

                    # Find HSN code (2-6 digits)
                    for c in row:
                        if c and re.search(r"\b\d{2,6}\b", c):
                            hsn = re.search(r"\b\d{2,6}\b", c).group(0)
                            break

                    # Description: longest text cell
                    lengths = [(i, len(c or "")) for i, c in enumerate(row)]
                    if lengths:
                        idx = max(lengths, key=lambda x: x[1])[0]
                        desc = row[idx]

                    if rate and desc:
                        try:
                            rows_out.append((hsn or "", desc, float(rate)))
                        except:
                            pass
            else:
                # fallback: text-based regex parsing if no tables
                txt = page.extract_text() or ""
                for line in txt.split("\n"):
                    m = re.search(r"(\d{2,6})\s+(.{10,200}?)\s+(\d+(\.\d+)?)\s*%?$", line)
                    if m:
                        rows_out.append((m.group(1), m.group(2).strip(), float(m.group(3))))

    return rows_out
