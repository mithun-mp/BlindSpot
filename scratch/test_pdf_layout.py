import os
import sys
import pypdf

from blindspot.reporting.audit_compiler import UnifiedAuditData
from blindspot.reporting.audit_pdf_generator import AuditPDFGenerator

sys.stdout.reconfigure(encoding='utf-8')

exp_dir = "runs/exp_1790977223_6c3ec3"
audit_data = UnifiedAuditData(exp_dir)
pdf_gen = AuditPDFGenerator(audit_data)
raw_bytes = pdf_gen.generate_bytes()

out_path = "scratch/current_output.pdf"
with open(out_path, "wb") as f:
    f.write(raw_bytes)

print(f"Generated PDF size: {len(raw_bytes)} bytes")

reader = pypdf.PdfReader(out_path)
print(f"Total pages: {len(reader.pages)}")

for idx, page in enumerate(reader.pages, 1):
    txt = page.extract_text()
    lines = [l.strip() for l in txt.splitlines() if l.strip()]
    content_lines = [
        l for l in lines 
        if not l.startswith("CONFIDENTIAL & PROPRIETARY") 
        and not l.startswith("Page ") 
        and not l.startswith("BlindSpot Multimodel Robustness Audit")
        and not l.startswith("Run: exp_")
    ]
    first_few = content_lines[:4]
    last_few = content_lines[-4:] if len(content_lines) >= 4 else content_lines
    print(f"\n================ PAGE {idx} ================")
    print("TOP:")
    for l in first_few:
        print("  ", l)
    print("BOTTOM:")
    for l in last_few:
        print("  ", l)
