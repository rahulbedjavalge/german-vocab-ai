import streamlit as st
import json
import random
import httpx
import os

# -------------------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------------------
st.set_page_config(page_title="German Vocab AI", layout="centered")

# -------------------------------------------------------------------
# OPENROUTER API KEY + MODEL
# -------------------------------------------------------------------
# Read API key and model from environment. Do NOT hard-code keys in source.
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
# Allow overriding the model via env var; default to the requested model
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "x-ai/grok-4.1-fast:free")

# -------------------------------------------------------------------
# LOAD LOCAL VOCAB FILE
# -------------------------------------------------------------------
def load_vocab(level):
    try:
        with open(f"data/{level.lower()}.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

# -------------------------------------------------------------------
# AI MODE: GENERATE 5 WORDS USING OPENROUTER
# -------------------------------------------------------------------
def generate_ai_words():
    url = "https://openrouter.ai/api/v1/chat/completions"

    prompt = """
Generate 5 German words suitable for A1 or A2 level.

Return ONLY valid JSON in this format:

[
  {
    "word": "gehen",
    "type": "verb",
    "gender": null,
    "meaning": "to go",
    "example": "Ich gehe zur Arbeit."
  },
  {
    "word": "der Tisch",
    "type": "noun",
    "gender": "der",
    "meaning": "table",
    "example": "Der Tisch ist rund."
  }
]

Rules:
- Always return exactly 5 items.
- Use null for gender if not a noun.
- Use only A1 or A2 vocabulary.
- Keep examples short and simple.
- Return ONLY the JSON. No extra text.
"""

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }

    # Ensure API key is available
    if not OPENROUTER_API_KEY:
        return {"error": "OPENROUTER_API_KEY is not set. Set env var OPENROUTER_API_KEY."}

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        res = httpx.post(url, json=payload, headers=headers, timeout=20)
        data = res.json()
        content = data["choices"][0]["message"]["content"]
        return json.loads(content)
    except Exception as e:
        return {"error": str(e)}

# -------------------------------------------------------------------
# UI
# -------------------------------------------------------------------
st.title("🇩🇪 German Vocab AI")
st.write("Learn German with simple words, examples, and AI suggestions.")

# level selector for local mode
level = st.radio(
    "Choose your level:",
    ["A1", "A2", "B1"],
    horizontal=True
)

vocab = load_vocab(level)

# -------------------------------------------------------------------
# LOCAL MODE BUTTON
# -------------------------------------------------------------------
st.subheader("Local Mode (from your vocab list)")

if st.button("Generate 5 Words (Local Mode)"):
    if len(vocab) < 5:
        st.error("Not enough words in your local vocab file.")
    else:
        selected = random.sample(vocab, 5)
        for w in selected:
            st.subheader(w["word"])
            st.write(f"Meaning: {w['meaning']}")
            st.write(f"Example: {w['example']}")
            st.write(f"Type: {w['type']}")
            st.write("---")

# -------------------------------------------------------------------
# AI MODE BUTTON
# -------------------------------------------------------------------
st.subheader("AI Mode (OpenRouter)")

if st.button("Generate 5 Random AI Words"):
    # Quick UI-side check to avoid calling API without a key
    if not OPENROUTER_API_KEY:
        st.error("OPENROUTER_API_KEY is not set. Set the environment variable and restart the app.")
    else:
        with st.spinner("AI is generating words..."):
            ai_words = generate_ai_words()

            if isinstance(ai_words, dict) and "error" in ai_words:
                st.error(ai_words["error"])
            else:
                for w in ai_words:
                    st.subheader(w["word"])
                    st.write(f"Meaning: {w['meaning']}")
                    st.write(f"Example: {w['example']}")
                    st.write(f"Type: {w['type']}")
                    st.write(f"Gender: {w['gender']}")
                    st.write("---")

