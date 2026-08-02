import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from pypdf import PdfReader
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

llm = ChatGoogleGenerativeAI(
    api_key=GEMINI_API_KEY,
    model="gemini-flash-latest",
    temperature=0
)

st.title("📄 PDF Company Profile Summarizer")
st.write("Upload a PDF and get an instant AI-generated summary.")

uploaded_file = st.file_uploader("Upload your PDF", type="pdf")

if uploaded_file is not None:
    reader = PdfReader(uploaded_file)
    pdf_text = ""
    for page in reader.pages:
        pdf_text += page.extract_text()

    st.success(f"Extracted {len(pdf_text)} characters from the PDF.")

    if st.button("Summarize"):
        with st.spinner("Generating summary..."):
            prompt = f"""
            You are a professional business analyst.
            Summarize the following company profile in simple, clear English.
            Include: company purpose, key services, target audience, and unique strengths.

            COMPANY PROFILE TEXT:
            {pdf_text}
            """
            response = llm.invoke(prompt)
            st.subheader("Summary")
            st.write(response.content)