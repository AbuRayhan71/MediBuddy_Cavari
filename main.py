import streamlit as st
from groq import Groq
import time
import os
from dotenv import load_dotenv
from database import SignupDatabase

# Load environment variables from .env file
load_dotenv()

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="MedAdmin Help", 
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- SESSION STATE ---
if "last_response" not in st.session_state:
    st.session_state.last_response = ""

# --- DATABASE SETUP ---
db = SignupDatabase()

# --- GROQ SETUP ---
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    st.error("⚠️ GROQ_API_KEY not found. Please set it in your .env file.")
    st.stop()
client = Groq(api_key=groq_api_key)

# --- STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    .stApp {
        background-color: white;
        font-family: 'Inter', sans-serif;
        color: black;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu, footer, header { visibility: hidden; }
    
    /* Header styling */
    .header {
        text-align: center;
        padding: 2rem 0 1rem 0;
        border-bottom: 1px solid #e0e0e0;
        margin-bottom: 2rem;
    }
    
    .header h1 {
        color: black;
        font-size: 2.5rem;
        font-weight: 600;
        margin: 0;
    }
    
    .header p {
        color: #666;
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
    }
    
    /* Early access banner */
    .early-access-banner {
        background-color: #f8f9fa;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0 2rem 0;
        text-align: center;
    }
    
    .early-access-banner h3 {
        color: black;
        margin: 0 0 0.5rem 0;
        font-size: 1.2rem;
    }
    
    .early-access-banner p {
        color: #666;
        margin: 0 0 1rem 0;
    }
    
    /* Input section */
    .input-section {
        margin: 2rem 0;
    }
    
    .input-section h2 {
        color: black;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .stTextArea textarea {
        border: 1px solid #ccc;
        border-radius: 8px;
        font-size: 1rem;
        color: black;
        font-family: 'Inter', sans-serif;
    }
    
    .stTextArea textarea:focus {
        border-color: #666;
        box-shadow: 0 0 0 1px #666;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: black;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 500;
        font-size: 1rem;
        transition: background-color 0.3s;
    }
    
    .stButton > button:hover {
        background-color: #333;
    }
    
    /* Output section */
    .output-section {
        margin: 2rem 0;
    }
    
    .output-section h2 {
        color: black;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .output-box {
        background-color: #f8f9fa;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1.5rem;
        min-height: 200px;
        color: black;
        font-family: 'Inter', sans-serif;
        line-height: 1.6;
    }
    
    .no-output {
        color: #666;
        font-style: italic;
        text-align: center;
        padding: 3rem;
    }
    
    /* Form styling */
    .signup-form {
        display: flex;
        gap: 1rem;
        align-items: end;
        margin-top: 1rem;
    }
    
    .stTextInput input {
        border: 1px solid #ccc;
        border-radius: 8px;
        color: black;
        font-family: 'Inter', sans-serif;
    }
    
    .stTextInput input:focus {
        border-color: #666;
        box-shadow: 0 0 0 1px #666;
    }
    
    /* Success/Error messages */
    .stSuccess, .stError, .stInfo {
        font-family: 'Inter', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
<div class="header">
    <h1>🩺 MedAdmin Help</h1>
    <p>AI-powered clinical documentation assistant</p>
</div>
""", unsafe_allow_html=True)

# --- EARLY ACCESS SIGNUP ---
with st.container():
    st.markdown("""
    <div class="early-access-banner">
        <h3>🚀 Get Early Access</h3>
        <p>Be among the first to experience our advanced medical documentation features</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("signup_form"):
            email = st.text_input("Enter your email address", placeholder="doctor@clinic.com")
            signup_submitted = st.form_submit_button("Join Early Access", use_container_width=True)
            
            if signup_submitted:
                if email and "@" in email:
                    try:
                        db.add_signup(email)
                        st.success("✅ Thank you! You've been added to our early access list.")
                    except Exception as e:
                        if "UNIQUE constraint failed" in str(e):
                            st.info("📧 You're already on our early access list!")
                        else:
                            st.error("❌ Something went wrong. Please try again.")
                else:
                    st.error("❌ Please enter a valid email address.")

# --- MAIN CONTENT ---
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown('<h2>📝 Your Clinical Text</h2>', unsafe_allow_html=True)
    
    with st.form("clinical_form"):
        raw_text = st.text_area(
            "Enter your clinical notes or dictation here...",
            value=st.session_state.get("raw_text_input", ""),
            height=300,
            label_visibility="collapsed",
            key="raw_text_input",
            placeholder="Example: Patient presents with chest pain, shortness of breath..."
        )
        
        submit_button = st.form_submit_button("Process with AI", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="output-section">', unsafe_allow_html=True)
    st.markdown('<h2>📄 Formatted Output</h2>', unsafe_allow_html=True)
    
    output_container = st.container()
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- PROCESSING ---
if submit_button and raw_text.strip():
    with output_container:
        with st.spinner("🤖 Processing your clinical notes..."):
            st.session_state.last_response = ""
            
            system_prompt = """You are an expert clinical documentation assistant. Your task is to convert raw, unstructured clinical notes into a well-formatted, professional medical summary.

Please structure your response with clear sections such as:
- Chief Complaint
- History of Present Illness
- Physical Examination
- Assessment
- Plan

Maintain medical accuracy and use proper medical terminology while ensuring the output is clear and well-organized."""

            try:
                completion = client.chat.completions.create(
                    model="meta-llama/llama-3.1-70b-versatile",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": raw_text}
                    ],
                    temperature=0.7,
                    max_tokens=1024,
                    top_p=1,
                    stream=True
                )
                
                response_placeholder = st.empty()
                full_response = ""
                
                for chunk in completion:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        response_placeholder.markdown(f'<div class="output-box">{full_response}</div>', unsafe_allow_html=True)
                
                st.session_state.last_response = full_response

            except Exception as e:
                st.error(f"❌ Error processing your request: {str(e)}")
                st.session_state.last_response = ""

# --- DISPLAY LAST RESPONSE OR PLACEHOLDER ---
with output_container:
    if st.session_state.last_response:
        st.markdown(f'<div class="output-box">{st.session_state.last_response}</div>', unsafe_allow_html=True)
    else:
        st.markdown('''
        <div class="output-box">
            <div class="no-output">
                Your formatted clinical documentation will appear here after processing...
            </div>
        </div>
        ''', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem 0;">
    <p><strong>MedAdmin Help</strong> - AI-powered clinical documentation</p>
    <p style="font-size: 0.9rem;">⚠️ Always review and verify all AI-generated medical content before use</p>
</div>
""", unsafe_allow_html=True)
