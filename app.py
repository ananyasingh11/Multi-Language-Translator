import streamlit as st
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
import torch
import os
import sys

# Set page config
st.set_page_config(
    page_title="AI Language Translator",
    page_icon="🌐",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stTextArea textarea {
        font-size: 16px;
    }
    .stSelectbox div[data-baseweb="select"] {
        font-size: 16px;
    }
    h1 {
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton button {
        width: 100%;
        background-color: #1E88E5;
        color: white;
        font-size: 18px;
        padding: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

def combine_model_parts():
    """Combines split model files if the combined file doesn't exist."""
    base_dir = r"c:\Users\HP\vscode\projects\ai lang translator\model"
    parts_dir = os.path.join(base_dir, "model")
    output_file = os.path.join(base_dir, "model.safetensors")
    
    # Check if combined file already exists and is significant in size (e.g. > 100MB as a sanity check)
    if os.path.exists(output_file) and os.path.getsize(output_file) > 100 * 1024 * 1024:
        # st.info("Combined model file found.") # Optional logging
        return output_file

    st.warning("Combined model file not found. Starting combination process... This only happens once.")
    
    # List all parts
    parts = []
    if not os.path.exists(parts_dir):
         st.error(f"Parts directory not found: {parts_dir}")
         return None

    for filename in os.listdir(parts_dir):
        if filename.startswith("model.safetensors.part"):
            parts.append(filename)
    
    if not parts:
        st.error("No model parts found.")
        return None

    # Sort parts numerically by part number
    try:
        parts.sort(key=lambda x: int(x.split('part')[-1]))
    except ValueError:
        st.error("Error sorting model parts. Ensure filenames end with 'partN'.")
        return None
    
    progress_bar = st.progress(0, text="Combining model files...")
    total_parts = len(parts)

    try:
        with open(output_file, 'wb') as outfile:
            for i, part in enumerate(parts):
                part_path = os.path.join(parts_dir, part)
                progress_bar.progress((i) / total_parts, text=f"Processing {part}...")
                with open(part_path, 'rb') as infile:
                    outfile.write(infile.read())
        
        progress_bar.progress(1.0, text="Combination complete!")
        st.success(f"Successfully created {output_file}")
        return output_file
    except Exception as e:
        st.error(f"Failed to combine model files: {e}")
        return None

@st.cache_resource
def load_model():
    # Ensure model is combined
    model_file_path = combine_model_parts()
    if not model_file_path:
        return None, None

    model_path = r"c:/Users/HP/vscode/projects/ai lang translator/model"
    try:
        tokenizer = MBart50TokenizerFast.from_pretrained(model_path)
        model = MBartForConditionalGeneration.from_pretrained(model_path)
        return tokenizer, model
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None, None

def main():
    st.title("🌐 AI Language Translator")
    
    st.markdown("### Translate English to Multiple Languages")
    
    # Load model
    with st.spinner("Loading model... This might take a minute."):
        tokenizer, model = load_model()
    
    if tokenizer is None or model is None:
        st.warning("Model could not be loaded. Please ensure the model files are correctly placed.")
        return

    # Language mapping
    lang_codes = {
        "Hindi": "hi_IN",
        "Italian": "it_IT",
        "Portuguese": "pt_XX",
        "French": "fr_XX",
        "Spanish": "es_XX"
    }

    # Layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Source Text (English)")
        source_text = st.text_area("Enter text to translate:", height=200, placeholder="Type here...")
        
    with col2:
        st.subheader("Target Language")
        target_lang = st.selectbox("Select language:", list(lang_codes.keys()))
        
        st.subheader("Translation")
        if st.button("Translate"):
            if source_text:
                try:
                    with st.spinner("Translating..."):
                        # specialized logic for mBART
                        tokenizer.src_lang = "en_XX"
                        encoded_hi = tokenizer(source_text, return_tensors="pt")
                        
                        target_code = lang_codes[target_lang]
                        generated_tokens = model.generate(
                            **encoded_hi,
                            forced_bos_token_id=tokenizer.lang_code_to_id[target_code]
                        )
                        translation = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
                        
                        st.success(translation)
                except Exception as e:
                    st.error(f"Translation error: {str(e)}")
            else:
                st.warning("Please enter some text to translate.")

if __name__ == "__main__":
    main()
