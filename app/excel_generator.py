from openpyxl import Workbook
from app.srb_template import SRB_COLUMNS


def generate_srb_excel(invoice_data, output_path):
    wb = Workbook()
    ws = wb.active
    ws.title = "SRB"

    # Header
    ws.append(SRB_COLUMNS)

    # Single SRB row
    ws.append([
        1,
        invoice_data["buyer_ntn"],
        invoice_data["buyer_name"],
        invoice_data["invoice_number"],
        invoice_data["invoice_date"],
        invoice_data["district"],
        invoice_data["rate"],
        invoice_data["value_excl"],
        invoice_data["tax"],
        invoice_data["st_withheld"],
        invoice_data["total"]
    ])

    wb.save(output_path)
