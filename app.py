import streamlit as st
import google.generativeai as genai
import pydicom
from PIL import Image
import numpy as np
import io

# --- CONFIGURATION ---
st.set_page_config(page_title="Cancer Navigator V1", layout="wide")

# API Setup
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)
# We use Pro here because it is better at vision tasks
model = genai.GenerativeModel('gemini-1.5-pro') 

st.title("🧠 Neuro-Onco Navigator V1")
st.markdown("### Personalized MRI Analysis & Clinical Intelligence")

# --- MRI UPLOAD FEATURE ---
st.header("📂 Step 1: Upload Your Imaging")
uploaded_file = st.file_uploader("Upload an MRI Slice (.dcm or .jpg/.png)", type=['dcm', 'jpg', 'png'])

if uploaded_file is not None:
    # 1. Process the Image
    if uploaded_file.name.endswith('.dcm'):
        ds = pydicom.dcmread(uploaded_file)
        # Convert DICOM pixel data to an image
        pixel_array = ds.pixel_array
        rescaled_image = (np.maximum(pixel_array, 0) / pixel_array.max()) * 255
        final_image = Image.fromarray(rescaled_image.astype(np.uint8))
    else:
        final_image = Image.open(uploaded_file)

    st.image(final_image, caption="Uploaded Scan Preview", width=400)

    # 2. AI Analysis
    if st.button("Analyze Image Findings"):
        with st.spinner("AI is scanning for concerning features..."):
            # Prompting Gemini for medical image reasoning
            prompt = """
            Analyze this brain MRI image. Provide 3-4 bullets on what might look 'concerning' 
            (e.g., midline shift, enhancement, edema, mass effect). 
            Then, provide 5 specific questions the patient should ask their Neurologist 
            or Neuro-Oncologist based on this scan.
            
            DISCLAIMER: Start with a clear warning that you are an AI, not a doctor, 
            and this is for educational purposes only.
            """
            
            response = model.generate_content([prompt, final_image])
            
            st.markdown("---")
            st.markdown("### 🔍 Scan Insights")
            st.write(response.text)

# --- SEARCH & CHATBOT (Previously Built) ---
st.markdown("---")
st.header("💬 Ask the Patient Concierge")
user_q = st.text_input("Ask a follow-up about your MRI or diagnosis:")
if user_q:
    response = model.generate_content(f"Answer this medical question as a helpful assistant: {user_q}")
    st.info(response.text)
