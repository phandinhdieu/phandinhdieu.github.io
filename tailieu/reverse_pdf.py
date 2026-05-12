from PyPDF2 import PdfReader, PdfWriter
import sys
import os

def reverse_pdf(input_path, output_path=None):
    if not os.path.exists(input_path):
        print(f"❌ File not found: {input_path}")
        return

    if output_path is None:
        base, ext = os.path.splitext(input_path)
        output_path = base + "_reversed.pdf"

    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reversed(reader.pages):
        writer.add_page(page)

    with open(output_path, "wb") as f:
        writer.write(f)

    print(f"✅ Reversed PDF saved as: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 reverse_pdf.py <input.pdf> [output.pdf]")
    else:
        reverse_pdf(*sys.argv[1:])
