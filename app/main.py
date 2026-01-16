from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import shutil
import uuid
import os

from app.pso_parser import parse_pso_invoice
from app.excel_generator import generate_srb_excel

app = FastAPI()

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "FastAPI Invoice to SRB Service is running!"}

@app.post("/upload")
async def upload_invoice(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    pdf_path = f"{UPLOAD_DIR}/{file_id}.pdf"
    excel_path = f"{OUTPUT_DIR}/{file_id}.xlsx"

    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    invoice_data = parse_pso_invoice(pdf_path)
    generate_srb_excel(invoice_data, excel_path)

    return FileResponse(
        excel_path,
        filename="SRB-Import.xlsx"
    )
