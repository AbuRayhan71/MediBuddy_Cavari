import streamlit as st
from groq import Groq
import time
import os
from dotenv import load_dotenv
from database import SignupDatabase, validate_email

# Load environment variables from .env file
load_dotenv()

# Initialize Groq client with API key from environment
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    st.error("⚠️ GROQ_API_KEY not found in environment variables. Please check your .env file.")
    st.stop()

client = Groq(api_key=groq_api_key)

# Initialize database for signups
db = SignupDatabase()

# Page configuration
st.set_page_config(
    page_title="MediBuddy by Cavari", 
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Modern CSS with Cavari branding
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Early Access Banner */
    .early-access-banner {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        text-align: center;
        margin-bottom: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .early-access-form {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 1rem;
        margin-top: 1rem;
        flex-wrap: wrap;
    }
    
    .early-access-input {
        padding: 0.75rem 1.5rem;
        border: none;
        border-radius: 25px;
        font-size: 14px;
        min-width: 250px;
        outline: none;
    }
    
    .early-access-btn {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .early-access-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(240, 147, 251, 0.4);
    }
    
    /* Main Header with Cavari Branding */
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 3rem;
        box-shadow: 0 20px 40px rgba(30, 60, 114, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="rgba(255,255,255,0.1)"/><circle cx="75" cy="75" r="1" fill="rgba(255,255,255,0.1)"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
        opacity: 0.3;
    }
    
    .cavari-logo {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        position: relative;
        z-index: 1;
    }
    
    .cavari-c { color: #1e3c72; }
    .cavari-o1 { color: #f5576c; }
    .cavari-v { color: #667eea; }
    .cavari-a { color: #f5576c; }
    .cavari-r { color: #1e3c72; }
    .cavari-i { color: #1e3c72; }
    
    .main-header h1 {
        color: white;
        margin-bottom: 1rem;
        font-size: 3rem;
        font-weight: 700;
        position: relative;
        z-index: 1;
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        position: relative;
        z-index: 1;
    }
    
    /* Modern Form Container */
    .form-container {
        background: white;
        padding: 3rem;
        border-radius: 25px;
        box-shadow: 0 25px 50px rgba(0,0,0,0.1);
        margin: 2rem 0;
        border: 1px solid rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
    }
    
    .form-title {
        color: #1e3c72;
        font-size: 1.8rem;
        font-weight: 600;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    /* Cool Input Styling */
    .stTextArea > div > div > textarea {
        border: 2px solid #e1ecf4;
        border-radius: 15px;
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        color: #1e3c72;
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        line-height: 1.6;
        transition: all 0.3s ease;
        padding: 1rem;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
        background: white;
        transform: translateY(-2px);
    }
    
    /* Modern Button */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 1rem 3rem;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Output Container */
    .output-container {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        padding: 2.5rem;
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        border: 1px solid rgba(102, 126, 234, 0.1);
        color: #1e3c72;
        line-height: 1.8;
    }
    
    /* Success Message */
    .success-message {
        background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        box-shadow: 0 10px 25px rgba(86, 171, 47, 0.3);
        text-align: center;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Feature Cards */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
        margin: 3rem 0;
    }
    
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        text-align: center;
        transition: all 0.3s ease;
        border: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    .feature-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 25px 50px rgba(0,0,0,0.15);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        color: #1e3c72;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .feature-desc {
        color: #666;
        line-height: 1.6;
    }
    
    /* Footer */
    .footer {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin-top: 3rem;
    }
    
    /* Hide default Streamlit elements */
    .css-1d391kg {
        display: none;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Early Access Banner with functional signup
signup_count = db.get_signup_count()

st.markdown(f"""
<div class="early-access-banner">
    <h2>🚀 Early Access to MediBuddy by Cavari</h2>
    <p>Be among the first to experience the future of clinical documentation</p>
    <p style="margin-top: 1rem; font-size: 0.9rem; opacity: 0.8;">🎯 {signup_count} people have joined • 🔒 HIPAA Compliant • ⚡ AI-Powered</p>
</div>
""", unsafe_allow_html=True)

# Functional signup form
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    with st.form("signup_form", clear_on_submit=True):
        signup_email = st.text_input(
            "", 
            placeholder="Enter your email for early access",
            label_visibility="collapsed"
        )
        
        if st.form_submit_button("🚀 Join Waitlist", use_container_width=True):
            if signup_email:
                if validate_email(signup_email):
                    if not db.email_exists(signup_email):
                        # Get user info (basic)
                        user_ip = "webapp_user"  # Could get real IP if needed
                        
                        if db.add_signup(signup_email, user_ip):
                            st.success(f"🎉 Welcome to the waitlist! You're signup #{db.get_signup_count()}")
                            st.balloons()
                            time.sleep(2)
                            st.rerun()
                        else:
                            st.error("❌ Something went wrong. Please try again.")
                    else:
                        st.warning("📧 You're already on the waitlist! We'll be in touch soon.")
                else:
                    st.error("❌ Please enter a valid email address.")
            else:
                st.error("❌ Please enter your email address.")

# Main Header with Cavari Branding
st.markdown("""
<div class="main-header">
    <div class="cavari-logo">
        <span class="cavari-c">c</span><span class="cavari-o1">o</span><span class="cavari-v">v</span><span class="cavari-a">a</span><span class="cavari-r">r</span><span class="cavari-i">i</span>
    </div>
    <h1>🏥 MediBuddy</h1>
    <p>Transform raw clinical notes into professional, structured documentation</p>
    <p><em>Powered by Advanced AI • Trusted by Healthcare Professionals</em></p>
</div>
""", unsafe_allow_html=True)

# Feature Cards
st.markdown("""
<div class="feature-grid">
    <div class="feature-card">
        <div class="feature-icon">⚡</div>
        <div class="feature-title">Lightning Fast</div>
        <div class="feature-desc">Generate structured notes in seconds with our advanced AI</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🎯</div>
        <div class="feature-title">Medical Accuracy</div>
        <div class="feature-desc">Trained on medical terminology for precise documentation</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🔒</div>
        <div class="feature-title">HIPAA Compliant</div>
        <div class="feature-desc">Enterprise-grade security for patient data protection</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Main Form
st.markdown("""
<div class="form-container">
    <div class="form-title">📝 Clinical Note Generator</div>
""", unsafe_allow_html=True)

with st.form("clinical_form", clear_on_submit=False):
    raw_text = st.text_area(
        "",
        height=300,
        placeholder="Paste your raw clinical notes here...\n\nExample: 45yo M c/o chest pain x 2 days, worse w/ exertion, denies SOB, PMH HTN DM, takes lisinopril metformin, NKDA, vitals stable, chest clear, heart RRR no murmur, plan EKG troponins cardiology consult...",
        help="Enter unstructured clinical text that needs to be organized"
    )
    
    submit_button = st.form_submit_button("🚀 Generate Professional Note")

st.markdown("</div>", unsafe_allow_html=True)

# Processing and output
if submit_button and raw_text.strip():
    
    # Progress indication
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    status_text.text("🔄 Initializing AI processing...")
    progress_bar.progress(20)
    time.sleep(0.5)
    
    status_text.text("🧠 Analyzing clinical content...")
    progress_bar.progress(40)
    
    # System prompt
    system_prompt = """
You are an expert clinical documentation assistant powered by Cavari's advanced AI. Transform raw, unstructured clinical notes into professional, comprehensive medical documentation.

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
            ✅ <strong>Clinical note generated successfully by Cavari AI!</strong> 
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
st.markdown("""
<div class="footer">
    <div class="cavari-logo" style="font-size: 2rem; margin-bottom: 1rem;">
        <span class="cavari-c">c</span><span class="cavari-o1">o</span><span class="cavari-v">v</span><span class="cavari-a">a</span><span class="cavari-r">r</span><span class="cavari-i">i</span>
    </div>
    <p><strong>MediBuddy Clinical Assistant</strong> | Powered by Cavari AI</p>
    <p><em>⚠️ For educational and assistance purposes only. Always verify clinical documentation.</em></p>
    <p style="margin-top: 1rem; opacity: 0.8;">© 2024 Cavari. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
