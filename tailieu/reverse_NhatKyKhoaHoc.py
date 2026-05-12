from PyPDF2 import PdfReader, PdfWriter
import os

input_path = "1969_NhatKyKhoaHoc_PDDieu.pdf"
output_path = "1969_NhatKyKhoaHoc_PDDieu_reversed.pdf"

if not os.path.exists(input_path):
    print(f"❌ File not found: {input_path}")
else:
    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reversed(reader.pages):
        writer.add_page(page)

    with open(output_path, "wb") as f:
        writer.write(f)

    print(f"✅ Reversed PDF saved as: {output_path}")
