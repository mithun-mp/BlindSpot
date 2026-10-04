import os
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

root_env = r"C:\Dev\Projects\Multimodel\Multimodel_Blindspot-main\.env"
key = os.environ.get("GEMINI_API_KEY", "")
if not key and os.path.exists(root_env):
    with open(root_env, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("BLINDSPOT_GEMINI_API_KEY_1="):
                key = line.split("=", 1)[1].strip().strip('"').strip("'")
                break

from google import genai
from google.genai import types as genai_types

client = genai.Client(api_key=key)

schema = {
    "type": "OBJECT",
    "properties": {
        "annotations": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "sentence_id": {"type": "STRING"},
                    "negative_probability": {"type": "NUMBER"},
                    "neutral_probability": {"type": "NUMBER"},
                    "positive_probability": {"type": "NUMBER"},
                    "label": {"type": "STRING", "enum": ["NEGATIVE", "NEUTRAL", "POSITIVE"]},
                    "reason_short": {"type": "STRING"},
                },
                "required": ["sentence_id", "negative_probability", "neutral_probability", "positive_probability", "label"]
            }
        }
    },
    "required": ["annotations"]
}

prompt = """You are annotating semantic sentiment reference data for a linguistic research experiment.
Evaluate the semantic sentiment of each sentence independently.
For each sentence, output:
- sentence_id: exact ID matching input
- negative_probability: float between 0.0 and 1.0
- neutral_probability: float between 0.0 and 1.0
- positive_probability: float between 0.0 and 1.0
- label: the highest probability polarity (NEGATIVE, NEUTRAL, or POSITIVE)
The probabilities must sum to 1.0.

SENTENCES TO ANNOTATE:
- ID: baseline | Text: "The movie was great and the acting was top notch."
- ID: p1 | Text: "The movie was not great and the acting was top notch."
"""

try:
    config = genai_types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=schema,
        temperature=0.0,
    )
    resp = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
        config=config,
    )
    print("STRUCTURED RESPONSE:")
    print(resp.text)
    parsed = json.loads(resp.text)
    print("Parsed JSON successfully:", len(parsed.get("annotations", [])))
except Exception as e:
    print("Structured call failed:", e)
