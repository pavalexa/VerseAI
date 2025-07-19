# caption.py

import requests
import base64
import os
import time
from dotenv import load_dotenv

load_dotenv()

HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

print("HF Token:", HUGGINGFACE_API_TOKEN[:10] + "..." if HUGGINGFACE_API_TOKEN else "Not found")


def get_image_caption(image_bytes, max_retries=3):
    api_url = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"
    }

    if not HUGGINGFACE_API_TOKEN:
        print("ERROR: HUGGINGFACE_API_TOKEN not found in environment variables")
        return None

    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt + 1}: Making request to Hugging Face API...")

            # If image_bytes is already bytes, use it directly
            if isinstance(image_bytes, bytes):
                files = {"inputs": image_bytes}
            else:
                # If it's a file path, read it
                with open(image_bytes, 'rb') as f:
                    files = {"inputs": f.read()}

            response = requests.post(api_url, headers=headers, files=files, timeout=30)

            print(f"Response status: {response.status_code}")
            print(f"Response headers: {dict(response.headers)}")

            if response.status_code == 200:
                try:
                    result = response.json()
                    print(f"API Response: {result}")

                    if isinstance(result, list) and len(result) > 0:
                        if "generated_text" in result[0]:
                            return result[0]["generated_text"]
                        elif "label" in result[0]:
                            return result[0]["label"]
                        else:
                            print("Unexpected response format:", result[0])
                            return None
                    else:
                        print("Unexpected response format:", result)
                        return None

                except Exception as json_error:
                    print(f"JSON parsing error: {json_error}")
                    print(f"Raw response: {response.text}")
                    return None

            elif response.status_code == 503:
                print("Model is loading, waiting 10 seconds...")
                time.sleep(10)
                continue

            elif response.status_code == 429:
                print("Rate limit exceeded, waiting 5 seconds...")
                time.sleep(5)
                continue

            else:
                print("Error:", response.status_code)
                print("Response text:", response.text)

                if attempt == max_retries - 1:
                    return None

        except requests.exceptions.RequestException as e:
            print(f"Request error on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            else:
                return None

    return None