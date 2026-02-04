# Universal Cancer Navigator v3.0

An AI-powered clinical intelligence hub designed for patients and researchers to navigate cancer diagnoses, imaging (DICOM), and global clinical trials.

## 🚀 Key Features
- **MRI Analysis:** Direct DICOM (.dcm) file support with automated feature detection.
- **Multimodal AI:** Powered by Google Gemini 2.0-flash for visual and textual reasoning.
- **Privacy First:** AES-256 cryptographic scrubbing of PII before cloud processing.
- **Live Clinical Trials:** Real-time syncing with ClinicalTrials.gov API v2 (2026 standards).

## 🛠 Installation
To run locally, ensure you have Python 3.10+ installed:

1. Clone the repo: `git clone https://github.com/your-username/cancer-navigator.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Add your secrets to `.streamlit/secrets.toml`:
   ```toml
   GEMINI_API_KEY = "your_key"
   ENCRYPTION_KEY = "your_fernet_generated_key"
