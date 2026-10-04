import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
keys = [k for k in os.environ if 'GEMINI' in k or 'GOOGLE' in k]
print(f"Matching env vars ({len(keys)}):")
for k in keys:
    val = os.environ[k]
    print(f"  {k}: present (len={len(val)}, prefix={val[:6]}...)")

root_env = r"C:\Dev\Projects\Multimodel\Multimodel_Blindspot-main\.env"
print(f".env exists: {os.path.exists(root_env)}")
if os.path.exists(root_env):
    with open(root_env, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k = line.split("=", 1)[0].strip()
                print(f"  .env key: {k}")
