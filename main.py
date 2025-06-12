import streamlit as st
from groq import Groq
import time
import os
from dotenv import load_dotenv
from database import SignupDatabase, validate_email

# Load environment variables from .env file
load_dotenv()

# Initialize database
db = SignupDatabase()

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="MedDoc Assistant by Cavari", 
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- SESSION STATE ---
if "early_access_clicked" not in st.session_state:
    st.session_state.early_access_clicked = False
if "last_response" not in st.session_state:
    st.session_state.last_response = ""
if "signup_success" not in st.session_state:
    st.session_state.signup_success = False
if "signup_error" not in st.session_state:
    st.session_state.signup_error = ""

# --- GROQ SETUP ---
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    st.error("⚠️ GROQ_API_KEY not found. Please set it in your .env file.")
    st.stop()
client = Groq(api_key=groq_api_key)

# --- STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* --- Base Styles --- */
    body {
        background-color: #f0f4f8;
    }
    .stApp {
        background-color: #f0f4f8; /* Light blue-gray background */
        font-family: 'Inter', sans-serif;
    }
    
    /* --- Header --- */
    .main-header {
        background-color: white;
        padding: 0.75rem 2rem;
        border-bottom: 1px solid #e0e6ed;
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 999;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }
    
    .logo-container {
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }
    
    .cavari-logo {
        font-weight: 700;
        font-size: 1.5rem;
        color: #1e293b;
    }
    
    .app-identifier {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .app-icon {
        background-color: #4f46e5;
        color: white;
        width: 40px;
        height: 40px;
        border-radius: 8px;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 1.5rem;
    }
    
    .app-title-group h1 {
        font-size: 1.25rem;
        font-weight: 600;
        color: #1e293b;
        margin: 0;
    }
    
    .app-title-group p {
        font-size: 0.875rem;
        color: #64748b;
        margin: 0;
    }
    
    .header-actions {
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }
    
    .ai-status {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: #16a34a; /* Green */
        font-weight: 500;
        font-size: 0.9rem;
    }
    
    .ai-status .status-dot {
        width: 8px;
        height: 8px;
        background-color: #16a34a;
        border-radius: 50%;
    }
    
    .stButton > button.early-access-btn {
        background-color: #4f46e5;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        transition: background-color 0.3s, transform 0.2s;
    }
    
    .stButton > button.early-access-btn:hover {
        background-color: #4338ca;
        transform: translateY(-2px);
    }
    
    /* --- Main Content --- */
    .main-content {
        padding: 100px 2rem 2rem 2rem;
        max-width: 950px;
        margin: 0 auto;
    }
    
    .input-card {
        background-color: white;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.07);
        padding: 2rem 2.5rem;
    }
    
    .card-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    
    .card-icon {
        font-size: 1.5rem;
        color: #4f46e5;
    }
    
    .card-header h2 {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1e293b;
        margin: 0;
    }
    
    .card-header p {
        color: #64748b;
        margin-left: 2.5rem;
        margin-top: -0.5rem;
        font-size: 0.9rem;
    }
    
    .stTextArea textarea {
        min-height: 250px;
        border: 1px solid #e0e6ed;
        border-radius: 8px;
        font-size: 1rem;
        color: white;
        background-color: #2d3748;
    }
    
    .stTextArea textarea:focus {
        border-color: #4f46e5;
        box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.2);
    }
    
    .stTextArea textarea::placeholder {
        color: #a0a0a0;
    }
    
    .card-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 1.5rem;
        padding-top: 1.5rem;
        border-top: 1px solid #f0f4f8;
    }
    
    .char-count {
        color: #64748b;
        font-size: 0.875rem;
    }
    
    .card-footer .stButton button {
        background-color: #334155; /* Dark gray */
    }
    
    .card-footer .stButton button:hover {
        background-color: #1e293b;
    }
    
    /* --- Output & Initial State --- */
    .output-container {
        width: 100%;
        max-width: 900px;
        margin: 2rem auto 0 auto;
    }

    .initial-state, .output-card {
        background-color: white;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.07);
        padding: 2rem 2.5rem;
        color: black;
    }
    
    .output-card * {
        color: black !important;
    }
    
    .output-card p, .output-card div, .output-card span, .output-card h1, .output-card h2, .output-card h3, .output-card h4, .output-card h5, .output-card h6 {
        color: black !important;
    }
    
    /* Target Streamlit markdown specifically */
    .output-card .stMarkdown {
        color: black !important;
    }
    
    .output-card .stMarkdown * {
        color: black !important;
    }

    .initial-state {
        text-align: center;
        padding: 4rem 2rem;
        border: 2px dashed #e0e6ed;
    }
    
    .initial-state h3 {
        font-size: 1.25rem;
        font-weight: 600;
        color: #334155;
        margin-bottom: 0.5rem;
    }
    
    .initial-state p {
        color: #64748b;
    }
    
    /* --- Disclaimer --- */
    .disclaimer {
        text-align: center;
        color: #64748b;
        font-size: 0.875rem;
        padding: 2rem;
        max-width: 900px;
        margin: 0 auto;
    }
    
    /* --- Footer --- */
    .main-footer {
        background-color: #0d1117; /* Very dark blue/black */
        color: #e6edf3;
        padding: 4rem 2rem 2rem 2rem;
        margin-top: 2rem;
    }
    
    .footer-content {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 3rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .footer-column .column-title {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        color: white;
    }
    
    .footer-column .cavari-logo-img {
        background-color: white;
        border-radius: 8px;
        width: 50px;
        height: 50px;
        margin-right: 1rem;
        /* In a real scenario, you'd use an <img> tag */
    }
    
    .footer-column p {
        color: #9ca3af;
        line-height: 1.6;
    }
    
    .contact-list {
        list-style: none;
        padding: 0;
    }
    
    .contact-list li {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    
    .contact-list .icon {
        color: #4f46e5;
        width: 20px;
        height: 20px;
    }
    
    .stButton > button.join-btn {
        background-color: #4f46e5;
        font-weight: 600;
        width: 100%;
        text-align: center;
        padding: 0.8rem 1rem;
    }
    
    .footer-bottom {
        border-top: 1px solid #30363d;
        text-align: center;
        padding-top: 2rem;
        margin-top: 3rem;
        font-size: 0.875rem;
        color: #9ca3af;
    }
    
    /* --- Early Access Text Color Fix --- */
    .signup-text h3 {
        color: #000000 !important;
        font-weight: 700 !important;
        font-size: 1.5rem !important;
        margin-bottom: 1rem !important;
    }
    
    .signup-text p {
        color: #000000!important;
        font-weight: 500 !important;
        font-size: 1rem !important;
    }
    
    /* Target Streamlit markdown specifically for signup section */
    .signup-text .stMarkdown h3 {
        color: #000000 !important;
        font-weight: 700 !important;
    }
    
    .signup-text .stMarkdown p {
        color: #000000 !important;
        font-weight: 500 !important;
    }
    
    /* --- Hide default Streamlit elements --- */
    #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
<div class="main-header">
    <div class="logo-container">
        <div class="cavari-logo">Cavari</div>
        <div class="app-identifier">
            <div class="app-icon">🩺</div>
            <div class="app-title-group">
                <h1>MedDoc Assistant</h1>
                <p>AI-Powered Clinical Documentation</p>
            </div>
        </div>
    </div>
    <div class="header-actions">
        <div class="ai-status">
            <div class="status-dot"></div>
            <span>AI Ready</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Removed header button - signup form moved to top

# --- EARLY ACCESS SIGNUP (TOP OF PAGE) ---
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Early Access Signup Form at the top
st.markdown('<div class="signup-text">', unsafe_allow_html=True)
st.markdown("")

if st.session_state.signup_success:
    st.success("🎉 Thank you! You've been successfully added to our early access list. We'll notify you when MedDoc Assistant launches!")
    if st.button("Close", key="close_signup_top"):
        st.session_state.signup_success = False
        st.session_state.signup_error = ""

elif st.session_state.signup_error:
    st.error(f"❌ {st.session_state.signup_error}")
    if st.button("Try Again", key="try_again_top"):
        st.session_state.signup_error = ""

else:
    with st.form("signup_form_top"):
        st.markdown('<p></p>', unsafe_allow_html=True)
        
        email = st.text_input(
            "Email Address",
            placeholder="Enter your email address",
            help="We'll only use this to notify you about the launch"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            submit_signup = st.form_submit_button("🚀 Join Early Access", use_container_width=True)
        with col2:
            cancel_signup = st.form_submit_button("Cancel", use_container_width=True)
        
        if submit_signup:
            if email and email.strip():
                try:
                    if validate_email(email.strip()):
                        if db.email_exists(email.strip()):
                            st.session_state.signup_error = "This email is already registered for early access"
                        else:
                            success = db.add_signup(email.strip())
                            if success:
                                st.session_state.signup_success = True
                                st.session_state.signup_error = ""
                            else:
                                st.session_state.signup_error = "Failed to save your email. Please try again."
                    else:
                        st.session_state.signup_error = "Please enter a valid email address"
                except Exception as e:
                    st.session_state.signup_error = f"An error occurred: {str(e)}"
            else:
                st.session_state.signup_error = "Please enter your email address"
        
        elif cancel_signup:
            # Clear any errors when canceling
            st.session_state.signup_error = ""

st.markdown('</div>', unsafe_allow_html=True)
st.markdown("---")

# --- MAIN CONTENT ---

with st.form("clinical_form"):
    st.markdown(
        """
        <div class="input-card">
            <div class="card-header">
                <span class="card-icon">📄</span>
                <h2>Raw Clinical Input</h2>
            </div>
            <p style="color: #64748b; margin-left: 2.5rem; margin-top: -1rem; margin-bottom: 1.5rem; font-size: 0.9rem;">
                Enter dictation or clinical notes for AI processing
            </p>
        """,
        unsafe_allow_html=True,
    )

    raw_text = st.text_area(
        "Enter clinical dictation here...",
        value=st.session_state.get("raw_text_input", ""),
        height=250,
        label_visibility="collapsed",
        key="raw_text_input"
    )

    st.markdown('<div class="card-footer">', unsafe_allow_html=True)
    char_count = len(raw_text)
    st.markdown(f'<div class="char-count">{char_count} characters</div>', unsafe_allow_html=True)
    submit_button = st.form_submit_button("Process with AI", use_container_width=False)
    st.markdown('</div></div>', unsafe_allow_html=True) # Close footer and card

# Early access form now at top of page

# --- PROCESSING AND OUTPUT ---
output_placeholder = st.container()

if submit_button and raw_text.strip():
    with output_placeholder:
        progress_bar = st.progress(0, text="Initializing AI processing...")
        st.session_state.last_response = "" # Clear previous response

        system_prompt = "You are an expert clinical documentation assistant. Convert the following raw clinical dictation or notes into a well-structured, professional clinical note. Format it with appropriate headings, organize the information logically, and ensure medical terminology is used correctly. Maintain all clinical accuracy while improving readability and structure."

        try:
            progress_bar.progress(30, text="🧠 Analyzing clinical content...")
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
            
            progress_bar.progress(60, text="📄 Generating professional note...")
            
            with st.container():
                output_stream_container = st.empty()
                
                full_response = ""
                for chunk in completion:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        output_stream_container.markdown(f'<div class="output-card" style="color: black;">{full_response}</div>', unsafe_allow_html=True)
                        
                st.session_state.last_response = full_response

            progress_bar.progress(100, text="✅ Processing complete!")
            time.sleep(1.5)
            progress_bar.empty()

        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.session_state.last_response = ""

elif st.session_state.last_response:
    # Display the last successful response if the form isn't submitted
    with output_placeholder:
        st.markdown(f'<div class="output-card" style="color: black;">{st.session_state.last_response}</div>', unsafe_allow_html=True)
else:
    # Initial State
    with output_placeholder:
        st.markdown("""
        <div class="initial-state">
            <h3>No processed note yet</h3>
            <p>Enter clinical text and click "Process with AI" to generate structured documentation</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True) # Close main-content

# --- DISCLAIMER & FOOTER ---
st.markdown('<div class="disclaimer">This AI-powered tool assists with clinical documentation formatting. Always review and verify all medical content before use.</div>', unsafe_allow_html=True)

st.markdown("""
<footer class="main-footer">
    <div class="footer-content">
        <div class="footer-column">
            <h3 class="column-title" style="display: flex; align-items: center;">
                <span class="cavari-logo-img"></span> <!-- Placeholder for image -->
                Cavari
            </h3>
            <p>Revolutionizing healthcare documentation with AI-powered clinical note generation and structured medical data processing.</p>
        </div>
        <div class="footer-column">
            <h3 class="column-title">Contact Information</h3>
            <ul class="contact-list">
                <li>
                    <span class="icon">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>
                    </span>
                    <span>mrayhan@cavari.com.au</span>
                </li>
                <li>
                    <span class="icon">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>
                    </span>
                    <span>0452 466 360</span>
                </li>
                <li>
                    <span class="icon">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
                    </span>
                    <span>Australia</span>
                </li>
            </ul>
        </div>
        <div class="footer-column">
            <h3 class="column-title">MedDoc Assistant</h3>
            <p>Advanced AI-powered clinical documentation platform designed for healthcare professionals to streamline medical record creation and improve patient care efficiency.</p>
            <div id="join-early-access-btn-container" style="margin-top: 1rem;">
                <!-- Join button will be rendered here by Streamlit -->
            </div>
        </div>
    </div>
    <div class="footer-bottom">
        © 2025 Cavari. All rights reserved. | AI-powered medical documentation platform for healthcare professionals.
    </div>
</footer>
""", unsafe_allow_html=True)

# Footer button removed - signup form moved to top
