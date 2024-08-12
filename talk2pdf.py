import streamlit as st
import fitz  # PyMuPDF
import google.generativeai as genai
import os

# Configure Genai API key
api_key = os.environ.get("GEMINI_API_KEY")  # Ensure you have set this in your environment
if not api_key:
    api_key = "AIzaSyCe1Q3jSavb0lTvUSNtSfJEdl15ZZ47oUk"  # Replace with your actual API key
genai.configure(api_key=api_key)

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Function to get response from Google Gemini
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([prompt, question])
    return response.text

# Streamlit interface
st.title('PDF Query Interface with Google Gemini')

# File uploader
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    # Extract text from the uploaded PDF
    pdf_text = extract_text_from_pdf(uploaded_file)

    # Display a text area for user query
    user_query = st.text_input("Enter your query about the PDF content:")

    if st.button("Submit Query"):
        if user_query:
            try:
                # Query the extracted text with Google Gemini
                response = get_gemini_response(user_query, pdf_text)
                st.write("Response from Gemini:")
                st.write(response)
            except Exception as e:
                st.error(f"Error querying text with Gemini: {e}")
        else:
            st.warning("Please enter a query.")
