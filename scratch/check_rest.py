import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('BLINDSPOT_PROJECT_DOCUMENTATION.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()
[print(f'{i}: {lines[i].strip()}') for i in range(1082, len(lines)) if lines[i].startswith('#')]
