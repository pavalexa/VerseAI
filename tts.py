# tts.py

import requests
import os
from dotenv import load_dotenv

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")


def get_available_voices():
    """Get list of available voices from ElevenLabs"""
    url = "https://api.elevenlabs.io/v1/voices"
    headers = {"xi-api-key": ELEVENLABS_API_KEY}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            voices = response.json()["voices"]
            return [(voice["name"], voice["voice_id"]) for voice in voices]
        else:
            print("Could not fetch voices:", response.status_code, response.text)
            return []
    except Exception as e:
        print("Error fetching voices:", e)
        return []


def text_to_speech(poem_text, output_path="poem_audio.mp3", voice_id=None):
    if voice_id is None:
        voices = get_available_voices()
        if voices:
            voice_id = voices[0][1]  # Use first available voice ID
            print(f"Using voice: {voices[0][0]} (ID: {voice_id})")
        else:
            print("No voices available, using default voice ID")
            voice_id = "21m00Tcm4TlvDq8ikWAM"  # ElevenLabs default voice

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": poem_text,
        "voice_settings": {
            "stability": 0.75,
            "similarity_boost": 0.75
        }
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(response.content)
        return output_path
    else:
        print("TTS Error:", response.status_code, response.text)
        if voice_id != "21m00Tcm4TlvDq8ikWAM":
            print("Trying fallback voice...")
            return text_to_speech(poem_text, output_path, "21m00Tcm4TlvDq8ikWAM")
        return None