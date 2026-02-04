from cryptography.fernet import Fernet
import streamlit as st

# --- SECURITY SETUP ---
# In production, generate this once and save it in st.secrets["ENCRYPTION_KEY"]
if "ENCRYPTION_KEY" in st.secrets:
    cipher_suite = Fernet(st.secrets["ENCRYPTION_KEY"])
else:
    st.error("Security Error: Master Encryption Key not found.")
    st.stop()

def encrypt_data(plain_text):
    """Encrypts sensitive strings (Names, IDs) before any processing"""
    return cipher_suite.encrypt(plain_text.encode()).decode()

def scrub_dicom(ds):
    """De-identifies DICOM by removing PII but keeping Age/Sex for AI"""
    pii_tags = ['PatientName', 'PatientID', 'PatientAddress', 'InstitutionName']
    for tag in pii_tags:
        if hasattr(ds, tag):
            # Encrypt the original data just in case we need to recover it for a doctor
            encrypted_val = encrypt_data(str(getattr(ds, tag)))
            setattr(ds, tag, "PROTECTED_DATA") 
    return ds
