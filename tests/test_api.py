'''
Tests the API endpoint
'''
import os
import requests

# Load .env file (if needed)
from dotenv import load_dotenv
load_dotenv()

# Make a test request to OpenAI API
URL = "https://api.deepseek.com/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {os.getenv('OPENAI_KEY')}",
    "Content-Type": "application/json"
}

payload = {
    "model": "deepseek-chat",
    "messages": [{"role": "user", "content": "Generate a short poem about AI"}]
}

response = requests.post(URL, json=payload, headers=headers)

print(f"Response Code: {response.status_code}")
print(f"Response JSON: {response.json()}")
