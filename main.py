import streamlit as st
from groq import Groq
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Groq client with API key from environment
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    st.error("⚠️ GROQ_API_KEY not found in environment variables. Please check your .env file.")
    st.stop()

client = Groq(api_key=groq_api_key)

# Page configuration
st.set_page_config(
    page_title="MediBuddy Clinical Assistant", 
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Simple CSS for clean black text on white background
st.markdown("""
<style>
    .stApp {
        background-color: white;
        color: black;
    }
    
    .main-header {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
        border: 1px solid #dee2e6;
    }
    
    .main-header h1 {
        color: black;
        margin-bottom: 1rem;
    }
    
    .main-header p {
        color: #333;
    }
    
    .stTextArea > div > div > textarea {
        border: 1px solid #ccc;
        border-radius: 5px;
        background-color: white;
        color: black;
    }
    
    .stButton > button {
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
    }
    
    .stButton > button:hover {
        background-color: #0056b3;
    }
    
    .output-container {
        background-color: white;
        padding: 1.5rem;
        border: 1px solid #ccc;
        border-radius: 5px;
        margin: 1rem 0;
        color: black;
    }
    
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    
    /* Hide sidebar */
    .css-1d391kg {
        display: none;
    }
    
    /* Make sure all text is black */
    h1, h2, h3, h4, h5, h6, p, div, span {
        color: black !important;
    }
    
    .stMarkdown {
        color: black;
    }
</style>
""", unsafe_allow_html=True)

# Main content
st.markdown("""
<div class="main-header">
    <h1>🏥 MediBuddy Clinical Assistant</h1>
    <p>Transform raw clinical notes into professional, structured documentation</p>
</div>
""", unsafe_allow_html=True)

# Input section
st.markdown("### 📝 Input Clinical Notes")
with st.form("clinical_form", clear_on_submit=False):
    raw_text = st.text_area(
        "Paste your raw clinical notes, dictation, or shorthand below:",
        height=300,
        placeholder="Example: 45yo M c/o chest pain x 2 days, worse w/ exertion, denies SOB, PMH HTN DM, takes lisinopril metformin, NKDA, vitals stable, chest clear, heart RRR no murmur, plan EKG troponins cardiology consult...",
        help="Enter unstructured clinical text that needs to be organized"
    )
    
    submit_button = st.form_submit_button("🚀 Generate Structured Note")

# Processing and output
if submit_button and raw_text.strip():
    
    # Progress indication
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    status_text.text("🔄 Processing...")
    progress_bar.progress(20)
    time.sleep(0.5)
    
    status_text.text("🧠 Analyzing clinical content...")
    progress_bar.progress(40)
    
    # System prompt
    system_prompt = """
You are an expert clinical documentation assistant. Transform raw, unstructured clinical notes into professional, comprehensive medical documentation.

Create a well-organized note with these sections (include only relevant sections):

**CHIEF COMPLAINT (CC):**
Brief primary reason for visit

**HISTORY OF PRESENT ILLNESS (HPI):**
Detailed narrative of current symptoms/condition

**PAST MEDICAL HISTORY (PMH):**
Relevant medical history, chronic conditions

**MEDICATIONS:**
Current medications with dosages if available

**ALLERGIES:**
Known drug allergies and reactions

**PHYSICAL EXAMINATION:**
Organized system-by-system findings

**ASSESSMENT AND PLAN:**
Clinical impression and treatment plan

Guidelines:
- Use proper medical terminology
- Maintain professional tone
- Organize information logically
- Remove filler words and casual language
- Include relevant negatives when mentioned
- Use standard medical abbreviations appropriately
"""

    try:
        status_text.text("🤖 Generating structured documentation...")
        progress_bar.progress(60)
        
        # Call Groq API
        completion = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": raw_text}
            ],
            temperature=0.7,
            max_completion_tokens=1024,
            top_p=1,
            stream=True
        )

        progress_bar.progress(80)
        status_text.text("📄 Formatting clinical note...")
        
        # Create output container
        st.markdown("---")
        st.markdown("## 📄 Generated Clinical Documentation")
        
        # Stream the response properly
        output_container = st.empty()
        full_response = ""
        
        for chunk in completion:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                # Display the accumulated response
                output_container.markdown(f"""
                <div class="output-container">
                {full_response}
                </div>
                """, unsafe_allow_html=True)
        
        progress_bar.progress(100)
        status_text.empty()
        progress_bar.empty()
        
        # Success message
        st.markdown("""
        <div class="success-message">
            ✅ <strong>Clinical note generated successfully!</strong> 
            Review the documentation above and copy as needed.
        </div>
        """, unsafe_allow_html=True)
        
        # Raw output for copying
        with st.expander("📝 Raw Text Output (for copying)"):
            st.text_area("Generated Note:", value=full_response, height=200)
            
    except Exception as e:
        st.error(f"❌ **Error Processing Note:** {str(e)}")
        st.info("Please check your input and try again.")

elif submit_button and not raw_text.strip():
    st.warning("⚠️ Please enter some clinical notes to process.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem; background-color: #f8f9fa; border-radius: 5px; margin-top: 2rem;">
    <p style="color: black; margin: 0;"><strong>MediBuddy Clinical Assistant</strong> | Built for Healthcare Professionals</p>
    <p style="color: #666; margin: 0;"><em>For educational and assistance purposes only. Always verify clinical documentation.</em></p>
</div>
""", unsafe_allow_html=True)
