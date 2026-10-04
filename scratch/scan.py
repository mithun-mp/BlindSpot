import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('BLINDSPOT_PROJECT_DOCUMENTATION.md', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
print(f'Total lines: {len(lines)}')
for i, l in enumerate(lines):
    if any(ord(c) in range(0x0500, 0x0700) or c in '\ufffd' for c in l):
        print(f'Corrupt line {i}: {l[:50]}')
