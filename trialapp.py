import streamlit as st
import io
from pdfminer.high_level import extract_text
import spacy
from collections import Counter
import base64

# Load SpaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except Exception as e:
    st.error(f"Error loading SpaCy model: {e}")
    nlp = None


# Function to extract text from PDF
def extract_text_from_pdf(pdf_bytes):
    try:
        pdf_file = io.BytesIO(pdf_bytes)  # Use BytesIO to read bytes
        text = extract_text(pdf_file)
        return text
    except Exception as e:
        st.error(f"Error extracting PDF text: {e}")
        return ""


# Function to tokenize words and remove stopwords
def word_tokenize(text):
    """Tokenizes and filters stopwords from the text."""
    if not text or not isinstance(text, str):
        return []  # Return empty list if invalid input

    try:
        doc = nlp(text)
        tokens = [token.text for token in doc if not token.is_stop and token.is_alpha]
        return tokens
    except Exception as e:
        st.error(f"Error during tokenization: {e}")
        return []


# Function to calculate keyword match percentage
def calculate_percentage_match(resume_text, job_description):
    try:
        # Tokenize and create sets of keywords
        resume_keywords = set(word_tokenize(resume_text))
        job_keywords = set(word_tokenize(job_description.lower()))

        # Ensure both have valid tokens
        if not resume_keywords or not job_keywords:
            return 0.0

        # Calculate match percentage
        common_keywords = resume_keywords.intersection(job_keywords)
        match_percentage = (len(common_keywords) / len(job_keywords)) * 100

        return round(match_percentage, 2)
    except Exception as e:
        st.error(f"Error calculating match percentage: {e}")
        return 0.0


# Streamlit App
st.title("Resume Match Percentage")

uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")
job_description = st.text_area("Enter job description")

if uploaded_file and job_description:
    try:
        # Extract text from uploaded PDF
        pdf_bytes = uploaded_file.read()
        resume_text = extract_text_from_pdf(pdf_bytes)

        # Ensure resume is not empty
        if not resume_text.strip():
            st.error("The PDF appears to be empty or unreadable.")
        else:
            # Calculate match percentage
            match_percentage = calculate_percentage_match(resume_text, job_description)

            # Display match percentage
            st.success(f"Match Percentage: {match_percentage:.2f}%")

    except Exception as e:
        st.error(f"Unexpected error: {e}")

