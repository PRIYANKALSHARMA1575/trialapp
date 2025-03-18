import streamlit as st
from pdfminer.high_level import extract_text
from io import BytesIO
import spacy

# Load SpaCy Model
try:
    nlp = spacy.load("en_core_web_sm")
except Exception as e:
    st.error(f"Error loading SpaCy model: {e}")
    st.stop()

# PDF Extraction Function
def extract_text_from_pdf(pdf_bytes):
    """Extracts text from PDF bytes"""
    try:
        pdf_file = BytesIO(pdf_bytes)
        text = extract_text(pdf_file)
        return text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
        return ""

# Percentage Matching Function
def calculate_percentage_match(resume_text, job_description):
    """Calculates keyword match percentage between resume and job description"""
    try:
        resume_doc = nlp(resume_text)
        job_doc = nlp(job_description)

        resume_keywords = {token.text.lower() for token in resume_doc if token.is_alpha}
        job_keywords = {token.text.lower() for token in job_doc if token.is_alpha}

        if not resume_keywords or not job_keywords:
            return 0.0

        common_keywords = resume_keywords & job_keywords
        match_percentage = (len(common_keywords) / len(job_keywords)) * 100

        return round(match_percentage, 2)
    
    except Exception as e:
        st.error(f"Error calculating match percentage: {e}")
        return 0.0

# Streamlit UI
st.title("📄 Resume vs Job Description Matching")

# File Upload
uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")

# Job Description Input
job_description = st.text_area("Enter Job Description")

# ✅ "Enter" Button
if st.button("Enter"):
    if uploaded_file and job_description:
        pdf_bytes = uploaded_file.read()

        # Extract text from PDF
        resume_text = extract_text_from_pdf(pdf_bytes)

        if resume_text:
            st.subheader("📑 Extracted Resume Text:")
            st.write(resume_text)

            # Calculate matching percentage
            match_percentage = calculate_percentage_match(resume_text, job_description)

            st.subheader("✅ Matching Percentage:")
            st.success(f"{match_percentage}%")
        else:
            st.warning("Failed to extract text from the PDF.")
    else:
        st.warning("Please upload a resume and enter a job description before clicking Enter.")
