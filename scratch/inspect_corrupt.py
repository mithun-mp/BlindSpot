import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('BLINDSPOT_PROJECT_DOCUMENTATION.md', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
print('--- 550 to 566 ---')
[print(f'{i}: {lines[i]}', end='') for i in range(550, 566)]
print('--- 1045 to 1054 ---')
[print(f'{i}: {lines[i]}', end='') for i in range(1045, 1054)]
