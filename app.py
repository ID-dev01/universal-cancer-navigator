import streamlit as st
import pandas as pd
import google.generativeai as genai
from google.api_core import exceptions
import time
import random

# --- 1. CONFIG & DATA (2026 BENCHMARKS) ---
st.set_page_config(page_title="Navigator v3.4", layout="wide")

CANCER_DATA = {
    "Brain": {
        "Stats": {"Incidence": "24,740 (US)", "5yr_Survival": "33% (Avg)", "Trend": "Stable"},
        "Types": {
            "Astrocytoma": {
                "Grades": ["Grade 2", "Grade 3", "Grade 4"],
                "Mutations": ["IDH-mutant", "IDH-wildtype"],
                "PFS": {"Grade 3": "53-59 months (IDH-mutant)", "Grade 4": "12-15 months"}
            },
            "Oligodendroglioma": {
                "Grades": ["Grade 2", "Grade 3"],
                "Mutations": ["1p/19q Co-deleted", "IDH-mutant"],
                "PFS": {"Grade 2": "10+ years"}
            }
        }
    },
    "Breast": {
        "Stats": {"Incidence": "324,580 (US)", "5yr_Survival": "91%", "Trend": "Rising in <50s"},
        "Types": {
            "Invasive Ductal": {
                "Grades": ["Grade 1", "Grade 2", "Grade 3"],
                "Mutations": ["HER2+", "Triple Negative", "ER/PR+"],
                "PFS": {"Grade 1": "Excellent (95%+)"}
            }
        }
    },
    "Colorectal": {
        "Stats": {"Incidence": "158,850 (US)", "5yr_Survival": "65%", "Trend": "#1 Killer in <50s"},
        "Types": {
            "Adenocarcinoma": {
                "Grades": ["Stage I", "Stage II", "Stage III", "Stage IV"],
                "Mutations": ["KRAS Mutant", "BRAF Mutant", "MSI-High"],
                "PFS": {"Stage IV": "Approx. 18-24 months"}
            }
        }
    }
}

# AI Setup
genai.configure(api_key=st.secrets["GEMINI_API_KEY"].strip())
model = genai.GenerativeModel('gemini-2.0-flash-lite')

def safe_ai(prompt):
    try:
        return model.generate_content(prompt)
    except exceptions.ResourceExhausted:
        st.error("Rate limit hit. Retrying...")
        time.sleep(2)
        return model.generate_content(prompt)

# --- 2. UNIVERSAL SEARCH LOGIC ---
st.title("🌐 Universal Cancer Navigator v3.4")

# Global Search Bar
search_query = st.text_input("🔍 Universal Search: Type a diagnosis, mutation, or symptom (e.g., 'What is Grade 3 Astrocytoma?')")

if search_query:
    with st.spinner("AI Mapping to Clinical Data..."):
        map_prompt = f"Identify the Organ, Cancer Type, and Grade from this: '{search_query}'. Return only: Organ: [Name], Type: [Name], Grade: [Name]"
        mapping = safe_ai(map_prompt)
        st.info(f"AI Detected Profile: {mapping.text}")

# --- 3. DYNAMIC TIERED FILTERS ---
st.divider()
with st.sidebar:
    st.header("Step 1: Clinical Profile")
    organ = st.selectbox("Select Organ", ["Select..."] + list(CANCER_DATA.keys()))
    
    if organ != "Select...":
        c_type = st.selectbox("Type", list(CANCER_DATA[organ]["Types"].keys()))
        grade = st.selectbox("Grade/Stage", CANCER_DATA[organ]["Types"][c_type]["Grades"])
        mutation = st.selectbox("Mutation", CANCER_DATA[organ]["Types"][c_type]["Mutations"])
    
    st.divider()
    st.header("Step 2: MRI/Imaging")
    uploaded_file = st.file_uploader("Upload Scan (.dcm, .jpg)", type=['dcm', 'jpg', 'png'])

# --- 4. DASHBOARD & CONCIERGE ---
if organ != "Select...":
    st.subheader(f"📊 {organ}: {c_type} {grade}")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("2026 Incidence", CANCER_DATA[organ]["Stats"]["Incidence"])
    m2.metric("5-Year Survival", CANCER_DATA[organ]["Stats"]["5yr_Survival"])
    m3.metric("Trend", CANCER_DATA[organ]["Stats"]["Trend"])

    # Chat Concierge
    st.divider()
    st.subheader("💬 Patient Concierge Chat")
    if "messages" not in st.session_state: st.session_state.messages = []
    
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if chat_in := st.chat_input("Ask about PFS or treatment options..."):
        st.session_state.messages.append({"role": "user", "content": chat_in})
        with st.chat_message("user"): st.markdown(chat_in)
        
        with st.chat_message("assistant"):
            p_context = f"Context: {organ}, {c_type}, {grade}, {mutation}."
            res = safe_ai(f"{p_context} {chat_in}")
            st.markdown(res.text)
            st.session_state.messages.append({"role": "assistant", "content": res.text})
else:
    st.write("### 👈 Start by selecting an Organ or using Universal Search.")
