import streamlit as st
from groq import Groq

# 🔐 For local dev ONLY – don't use hardcoded key in production
client = Groq(api_key="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")

st.set_page_config(page_title="Clinical Assistant", layout="centered")
st.title("🧠 Clinical Documentation Assistant")
st.caption("Built with Python + Groq + LLaMA 4")

# 📝 Text input from user
with st.form("input_form"):
    raw_text = st.text_area("Paste raw clinical note below:", height=250)
    submit = st.form_submit_button("Generate Structured Note")

if submit and raw_text.strip():
    st.info("⏳ Generating using LLaMA 4...")

    # Prompt to define assistant behavior
    system_prompt = """
You are a clinical admin assistant trained to help doctors convert raw clinical notes or dictation into professional, structured summaries.

Your task is to take raw text input (which may be messy, shorthand, or unstructured) and output a neatly formatted clinical note.

Use these sections in your output if relevant:

- Chief Complaint (CC)
- History of Present Illness (HPI)
- Past Medical History (PMH)
- Medications
- Allergies
- Physical Examination
- Assessment and Plan

Make the note clean, professional, and medically appropriate. Remove filler words or casual phrasing.
"""

    # Call Groq
    try:
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

        full_response = ""
        st.subheader("📄 Structured Note Output")
        for chunk in completion:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                st.write(chunk.choices[0].delta.content, end="")

        st.text_area("Full Output", value=full_response, height=300)

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
