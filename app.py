# app.py

import os
import streamlit as st
from poem_generator import generate_poem
from tts import text_to_speech
from PIL import Image
from dotenv import load_dotenv

# Hugging Face fallback for captioning
from transformers import BlipProcessor, BlipForConditionalGeneration

load_dotenv()

# Hugging Face API token
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

# BLIP model and processor (Hugging Face fallback)
blip_processor = None
blip_model = None


def primary_generate_caption(image_path):
    # Use your existing caption.py functionality
    try:
        print(f"Attempting to generate caption for: {image_path}")
        from caption import get_image_caption

        # Try with file path first
        caption = get_image_caption(image_path)
        if caption and caption != "Unable to generate caption.":
            return caption

        # If that fails, try reading the file as bytes
        print("Trying with image bytes...")
        with open(image_path, 'rb') as f:
            image_bytes = f.read()
        caption = get_image_caption(image_bytes)

        if caption and caption != "Unable to generate caption.":
            return caption

    except Exception as e:
        print(f"Primary caption generator error: {e}")
        import traceback
        traceback.print_exc()

    return None


def generate_caption(image_path):
    global blip_processor, blip_model

    try:
        # Try your existing caption generation first
        print("INFO: Trying primary caption generator...")
        caption = primary_generate_caption(image_path)
        if caption:
            print(f"Primary caption successful: {caption}")
            return caption
        else:
            print("Primary caption generator returned None or empty result")

    except Exception as e:
        print(f"WARNING: Primary caption generator failed: {e}")
        import traceback
        traceback.print_exc()

    try:
        # Fallback: Hugging Face BLIP
        print("INFO: Falling back to Hugging Face BLIP for captioning...")
        if blip_processor is None or blip_model is None:
            print("Loading BLIP model and processor...")
            blip_processor = BlipProcessor.from_pretrained(
                "Salesforce/blip-image-captioning-base",
                token=HUGGINGFACE_API_TOKEN
            )
            blip_model = BlipForConditionalGeneration.from_pretrained(
                "Salesforce/blip-image-captioning-base",
                token=HUGGINGFACE_API_TOKEN
            )
            print("BLIP model loaded successfully")

        print("Processing image with BLIP...")
        raw_image = Image.open(image_path).convert('RGB')
        inputs = blip_processor(raw_image, return_tensors="pt")
        print("Generated inputs for BLIP model")

        out = blip_model.generate(**inputs, max_length=50)
        caption = blip_processor.decode(out[0], skip_special_tokens=True)
        print(f"BLIP caption: {caption}")

        if caption:
            return caption

    except Exception as ex:
        print(f"ERROR: Hugging Face BLIP failed: {ex}")
        import traceback
        traceback.print_exc()

    # Final fallback - return a generic description
    return "A photograph or image that could not be automatically described."


# Streamlit UI
st.title("VerseVision: AI-Powered Poetic Captions")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image_path = f"temp_{uploaded_file.name}"
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.image(image_path, caption="Uploaded Image", use_container_width=True)

    caption = generate_caption(image_path)
    st.subheader("📝 Generated Caption")
    st.write(caption)

    poem = generate_poem(caption)
    st.subheader("🎨 Generated Poem")
    st.write(poem)

    # Optional: Generate TTS audio
    try:
        audio_path = text_to_speech(poem)
        if audio_path:
            st.subheader("🎵 Audio Poem")
            st.audio(audio_path, format="audio/mp3")
        else:
            st.info("Audio generation is currently unavailable.")
    except Exception as e:
        st.info(f"Audio generation failed: {str(e)}")

    # Clean up temp file
    os.remove(image_path)
else:
    st.info("Please upload an image to generate a caption and poem.")