import re
from app.pdf_parser import extract_text


def find(pattern, text):
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else ""


def parse_pso_invoice(pdf_path):
    text = extract_text(pdf_path)

    # -------------------------
    # HEADER
    # -------------------------
    invoice_number = find(r"ST invoice number\s*:\s*([0-9\-]+)", text)
    invoice_date = find(r"Date\s*:\s*(\d{2}-\d{2}-\d{4})", text)

    buyer_ntn = re.search(
    r"Service Recipient:.*?NTN NO:\s*([\d\-]+)",
    text,
    re.IGNORECASE | re.DOTALL
    ).group(1)
    
    buyer_name = "PAKISTAN STATE OIL"

    rate = 15

    # -------------------------
    # INVOICE TOTALS
    # -------------------------
    value_excl = float(find(r"Value exclusive of ST\s+([\d,]+\.\d+)", text).replace(",", ""))
    tax_amount = float(find(r"SALES TAX AMOUNT\s+([\d,]+\.\d+)", text).replace(",", ""))
    total_amount = float(find(r"TOTAL\s+([\d,]+\.\d+)", text).replace(",", ""))

    st_withheld = tax_amount / 2

    # -------------------------
    # DISTRICT FROM ORIGIN
    # -------------------------
    origin_match = re.search(r"\b(SINDH|PUNJAB|KPK|BALOCHISTAN)\b", text)
    district = "KARACHI" if origin_match and origin_match.group(1) == "SINDH" else ""

    # -------------------------
    # RETURN SINGLE SRB ROW
    # -------------------------
    return {
        "buyer_ntn": buyer_ntn,
        "buyer_name": buyer_name,
        "invoice_number": invoice_number,
        "invoice_date": invoice_date,
        "district": district,
        "rate": rate,
        "value_excl": value_excl,
        "tax": tax_amount,
        "st_withheld": st_withheld,
        "total": total_amount
    }
