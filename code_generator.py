import requests
import re

API_URL = "https://api-inference.huggingface.co/models/Salesforce/codegen-350M-mono"

def clean_code(raw: str) -> str:
    lines = raw.split('\n')
    cleaned = []
    for line in lines:
        if not re.search(r'^(Input|Output|>>>)', line.strip()):
            cleaned.append(line)
    return '\n'.join(cleaned).strip()

def generate_code(prompt: str, max_length: int = 512) -> str:
    headers = {"Content-Type": "application/json"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": max_length,
            "temperature": 0.7,
            "top_p": 0.9,
            "do_sample": True,
            "return_full_text": False
        }
    }
    response = requests.post(API_URL, json=payload, headers=headers)
    if response.status_code == 200:
        result = response.json()
        if isinstance(result, list) and len(result) > 0:
            generated = result[0].get("generated_text", "")
        else:
            generated = result.get("generated_text", "")
        return clean_code(generated)
    else:
        raise Exception(f"API error: {response.status_code} - {response.text}")

