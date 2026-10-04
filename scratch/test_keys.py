import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

root_env = r"C:\Dev\Projects\Multimodel\Multimodel_Blindspot-main\.env"
keys = {}
if os.path.exists(root_env):
    with open(root_env, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                if "KEY" in k and v:
                    keys[k] = v

print(f"Loaded {len(keys)} keys from .env:")
for alias, k in keys.items():
    print(f"  {alias}: prefix={k[:8]}... length={len(k)}")

from google import genai

for alias, k in keys.items():
    try:
        client = genai.Client(api_key=k)
        resp = client.models.generate_content(
            model="gemini-3.5-flash",
            contents="Say 'OK'"
        )
        print(f"Testing {alias} on gemini-3.5-flash: SUCCESS -> {resp.text.strip()}")
    except Exception as e:
        print(f"Testing {alias} on gemini-3.5-flash: FAILED -> {e}")
