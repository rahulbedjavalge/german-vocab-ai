import streamlit as st
import json
import random

st.set_page_config(page_title="German Vocab AI", layout="centered")

# choose level
st.title("🇩🇪 German Vocab AI")
st.write("Select your level and generate vocab")

level = st.radio(
    "Choose your level",
    ["A1", "A2", "B1"],
    horizontal=True
)

# load correct file
def load_vocab(level):
    try:
        with open(f"data/{level.lower()}.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

vocab = load_vocab(level)

if st.button("Generate 5 Words"):
    if len(vocab) < 5:
        st.error("Not enough words in your JSON file yet.")
    else:
        selected = random.sample(vocab, 5)
        st.subheader(f"Level: {level} words")
        for w in selected:
            st.write(f"**{w['word']}**  meaning: {w['meaning']} example: {w['example']}")
            st.write("---")
