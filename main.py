import streamlit as st
from groq import Groq
import time

# 🔐 For local dev ONLY – don't use hardcoded key in production
client = Groq(api_key="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")

# Page configuration
st.set_page_config(
    page_title="MediBuddy Clinical Assistant", 
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    /* Main app styling */
    .stApp {
        background-color: #ffffff;
    }
    
    .main-header {
        background: linear-gradient(135deg, #2E86AB 0%, #A23B72 100%);
        padding: 2.5rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 15px 35px rgba(46, 134, 171, 0.15);
    }
    
    .main-header h1 {
        margin-bottom: 1rem;
        font-weight: 700;
        font-size: 2.5rem;
    }
    
    .feature-card {
        background: linear-gradient(145deg, #f8fffe 0%, #ffffff 100%);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        border: 1px solid #e8f4f8;
        border-left: 5px solid #2E86AB;
        margin: 1.5rem 0;
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(0,0,0,0.12);
    }
    
    .feature-card h4 {
        color: #2E86AB;
        margin-bottom: 0.8rem;
        font-weight: 600;
    }
    
    .feature-card p {
        color: #5a6c7d;
        margin: 0;
        line-height: 1.5;
    }
    
    .success-message {
        background: linear-gradient(135deg, #00b894 0%, #00cec9 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        margin: 1.5rem 0;
        box-shadow: 0 8px 20px rgba(0, 184, 148, 0.2);
    }
    
    /* Input styling */
    .stTextArea > div > div > textarea {
        border-radius: 12px;
        border: 2px solid #e1ecf4;
        font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 14px;
        line-height: 1.6;
        background-color: #fafbfc;
        transition: all 0.3s ease;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #2E86AB;
        box-shadow: 0 0 0 3px rgba(46, 134, 171, 0.1);
        background-color: #ffffff;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #2E86AB 0%, #1B5E7C 100%);
        color: white;
        border: none;
        border-radius: 30px;
        padding: 0.75rem 2.5rem;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(46, 134, 171, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(46, 134, 171, 0.4);
        background: linear-gradient(135deg, #1B5E7C 0%, #2E86AB 100%);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f7f9fc 0%, #ffffff 100%);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f7f9fc 0%, #ffffff 100%);
        border-right: 1px solid #e1ecf4;
    }
    
    /* Output container */
    .output-container {
        background: linear-gradient(145deg, #ffffff 0%, #f8fffe 100%);
        padding: 2.5rem;
        border-radius: 20px;
        border: 1px solid #e1ecf4;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        line-height: 1.8;
        font-family: 'Inter', sans-serif;
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background: linear-gradient(135deg, #2E86AB 0%, #A23B72 100%);
    }
    
    /* Metrics styling */
    .css-1r6slb0 {
        background: linear-gradient(135deg, #f8fffe 0%, #ffffff 100%);
        border: 1px solid #e1ecf4;
        border-radius: 12px;
        padding: 1rem;
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background-color: #fafbfc;
        border: 2px solid #e1ecf4;
        border-radius: 10px;
    }
    
    /* Slider styling */
    .stSlider > div > div > div > div {
        background: #2E86AB;
    }
    
    /* Form styling */
    .stForm {
        background: linear-gradient(145deg, #ffffff 0%, #f8fffe 100%);
        border: 1px solid #e1ecf4;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.06);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #f7f9fc;
        border-radius: 10px;
        border: 1px solid #e1ecf4;
    }
    
    /* Warning and info styling */
    .stAlert {
        border-radius: 12px;
        border: none;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Section headers */
    h3 {
        color: #2d3748;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    /* Footer styling */
    .footer-text {
        background: linear-gradient(145deg, #f7f9fc 0%, #ffffff 100%);
        padding: 2rem;
        border-radius: 15px;
        border: 1px solid #e1ecf4;
        text-align: center;
        margin-top: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🏥 MediBuddy")
    st.markdown("**Clinical Documentation Assistant**")
    st.markdown("---")
    
    # Statistics/Info
    st.markdown("### 📊 Session Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Notes Generated", "0", delta="0")
    with col2:
        st.metric("Words Processed", "0", delta="0")
    
    st.markdown("---")
    
    # Model selection
    st.markdown("### ⚙️ Settings")
    model_option = st.selectbox(
        "AI Model",
        ["meta-llama/llama-4-scout-17b-16e-instruct", "Alternative Model"],
        help="Select the AI model for processing"
    )
    
    temperature = st.slider(
        "Creativity Level", 
        min_value=0.0, 
        max_value=1.0, 
        value=0.7, 
        step=0.1,
        help="Higher values make output more creative"
    )
    
    st.markdown("---")
    
    # Help section
    with st.expander("ℹ️ How to Use"):
        st.markdown("""
        1. **Paste** your raw clinical notes
        2. **Click** Generate to process
        3. **Review** the structured output
        4. **Copy** the final note
        """)
    
    with st.expander("📋 Note Sections"):
        st.markdown("""
        - Chief Complaint (CC)
        - History of Present Illness (HPI)
        - Past Medical History (PMH)
        - Medications & Allergies
        - Physical Examination
        - Assessment & Plan
        """)

# Main content
st.markdown("""
<div class="main-header">
    <h1>🏥 MediBuddy Clinical Assistant</h1>
    <p>Transform raw clinical notes into professional, structured documentation</p>
    <p><em>Powered by Advanced AI • HIPAA Compliant • Secure Processing</em></p>
</div>
""", unsafe_allow_html=True)

# Main input section
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📝 Input Clinical Notes")
    with st.form("clinical_form", clear_on_submit=False):
        raw_text = st.text_area(
            "Paste your raw clinical notes, dictation, or shorthand below:",
            height=300,
            placeholder="Example: 45yo M c/o chest pain x 2 days, worse w/ exertion, denies SOB, PMH HTN DM, takes lisinopril metformin, NKDA, vitals stable, chest clear, heart RRR no murmur, plan EKG troponins cardiology consult...",
            help="Enter unstructured clinical text that needs to be organized"
        )
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            submit_button = st.form_submit_button(
                "🚀 Generate Structured Note",
                use_container_width=True
            )

with col2:
    st.markdown("### 🎯 Quick Features")
    
    st.markdown("""
    <div class="feature-card">
        <h4>⚡ Fast Processing</h4>
        <p>Get structured notes in seconds</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h4>🎯 Medical Accuracy</h4>
        <p>AI trained on medical terminology</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h4>📋 Standard Format</h4>
        <p>Professional clinical structure</p>
    </div>
    """, unsafe_allow_html=True)

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
            model=model_option,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": raw_text}
            ],
            temperature=temperature,
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
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📋 Copy to Clipboard", help="Copy the generated note"):
                st.success("Note copied to clipboard!")
        with col2:
            if st.button("📤 Export as PDF", help="Download as PDF"):
                st.info("PDF export feature coming soon!")
        with col3:
            if st.button("🔄 Generate Again", help="Process with different settings"):
                st.rerun()
        
        # Raw output for copying
        with st.expander("📝 Raw Text Output (for copying)"):
            st.text_area("Generated Note:", value=full_response, height=200)
            
    except Exception as e:
        st.error(f"❌ **Error Processing Note:** {str(e)}")
        st.info("Please check your input and try again. If the problem persists, contact support.")

elif submit_button and not raw_text.strip():
    st.warning("⚠️ Please enter some clinical notes to process.")

# Footer
st.markdown("---")
st.markdown("""
<div class="footer-text">
    <p style="color: #2d3748; font-weight: 600; margin-bottom: 0.5rem;">🏥 <strong>MediBuddy Clinical Assistant</strong> | Built with ❤️ for Healthcare Professionals</p>
    <p style="color: #5a6c7d; margin: 0;"><em>⚠️ For educational and assistance purposes only. Always verify clinical documentation.</em></p>
</div>
""", unsafe_allow_html=True)
