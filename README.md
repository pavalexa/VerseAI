# VerseVision

### *Turn any image into a voice-powered micro poem with AI*

---

## What is VerseVision?

**VerseVision** is a creative AI app that transforms user-uploaded images into tender poetic audio-visual experiences. 

The app:

- Generates a **caption** for the uploaded image using HuggingFace’s BLIP model.
- Uses a language model to write a **short poem** based on that caption.
- Converts the poem into **speech audio** using the ElevenLabs Text-to-Speech API.
- Presents the caption, poem, and audio in a simple **Streamlit** interface, optionally with background music.

---

## How to Set Up and Run

**1. Clone the repository**

git clone https://github.com/your-username/versevision.git
cd versevision

**2. Create and activate a virtual environment**

python -m venv .venv
source .venv/bin/activate        # On macOS/Linux
.venv\Scripts\activate           # On Windows

**3. Install dependencies**

pip install -r requirements.txt

4. **Set up your API keys**

Create a file named .env in the root folder with the following content:

HUGGINGFACE_API_TOKEN=your_huggingface_api_key_here

ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

**5. Run the app**

streamlit run app.py


Known Issues or Limitations
 - Requires stable internet connection due to reliance on external APIs
 - The HuggingFace BLIP model may take time to load on first use (503 delay)
 - ElevenLabs API may be rate-limited on free plans or during high load
 - Background music support is currently static, should be chosen by the user and may not sync perfectly with poem audio
 - Multi-language support is not yet implemented

Contributors

**Olga Mondrus** – Concept, Design, and Development
**Alex Braginsky** - Development
