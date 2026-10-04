import os
import sys

from blindspot.reporting.audit_compiler import UnifiedAuditData, FIGURE_DEFINITIONS
from blindspot.reporting.audit_pdf_generator import AuditPDFGenerator

# 1. Update FIGURE_DEFINITIONS sequentially for testing
for k, v in FIGURE_DEFINITIONS.items():
    print(k, v["title"])

audit_data = UnifiedAuditData("runs/exp_1790977223_6c3ec3")
print("Experiment ID:", audit_data.exp_id)
