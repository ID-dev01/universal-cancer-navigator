import streamlit as st
import requests
import anthropic

# --- APP CONFIGURATION ---
st.set_page_config(page_title="Neuro-Onco Navigator", layout="wide")

# Replace with your actual API key or use st.secrets for deployment
ANTHROPIC_API_KEY = "YOUR_CLAUDE_API_KEY"
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# --- APP HEADER ---
st.title("🧠 Neuro-Onco Navigator v1.0")
st.markdown("### Global Intelligence on Brain Cancer Mutations & Trials")
st.sidebar.header("🔍 Filters")

# --- FILTERS ---
cancer_type = st.sidebar.selectbox("Cancer Type", ["Glioblastoma", "Astrocytoma", "DIPG", "Oligodendroglioma"])
mutation = st.sidebar.text_input("Mutation (e.g., IDH1, H3K27M, EGFR)", value="IDH1")
region = st.sidebar.selectbox("Geography", ["Global", "United States", "Europe", "Asia"])

# --- DATA FETCHING ---
def fetch_trials(query_mutation, query_cond):
    """Fetches real-time data from ClinicalTrials.gov API v2"""
    url = "https://clinicaltrials.gov/api/v2/studies"
    params = {
        "query.cond": query_cond,
        "query.term": query_mutation,
        "pageSize": 5
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# --- AI SUMMARY LOGIC ---
def get_ai_analysis(data, mutation_name):
    prompt = f"""
    You are a medical concierge app. Based on this raw data from ClinicalTrials.gov regarding {mutation_name}, 
    create a highly scannable 'App Dashboard' update.
    
    For each trial, include:
    - 🏥 **Trial Name**
    - 📍 **Location & Top Center**
    - 📞 **Contact Info** (Email/Phone from data)
    - 🔗 **Direct Link** (Using the NCT ID: https://clinicaltrials.gov/study/[NCTID])
    
    Raw Data: {data}
    """
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

# --- APP EXECUTION ---
if st.sidebar.button("Update Dashboard"):
    with st.spinner("Fetching global research and trials..."):
        # 1. Get Live Data
        raw_data = fetch_trials(mutation, cancer_type)
        
        if "error" in raw_data:
            st.error(f"Error fetching data: {raw_data['error']}")
        else:
            # 2. Let Claude Process it
            report = get_ai_analysis(raw_data, mutation)
            
            # 3. Display the "App" UI
            st.markdown("---")
            st.markdown(report)
            
            # 4. Actionable Next Step
            st.success("Report Generated. Data is valid for the next 14 days.")
else:
    st.info("👈 Select a mutation and click 'Update Dashboard' to begin.")

# --- LEGAL FOOTER ---
st.markdown("---")
st.caption("**Disclaimer:** This is an AI-powered tool for informational purposes only. It does not provide medical advice. Consult with an oncologist before making any medical decisions.")
