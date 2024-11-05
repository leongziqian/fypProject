
# import streamlit as st
# from transformers import pipeline

# # Load a pre-trained summarization model
# summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=0)

# def summarize_content(text):
#     summary = summarizer(text, max_length=130, min_length=50, do_sample=False, clean_up_tokenization_spaces=True)
#     return summary[0]['summary_text']

# # Set up the Streamlit app
# st.title("AI Marketing Copy Generator and Summarization Tool")



# # Content Summarization Tool
# st.header("Content Summarization Tool")
# long_content = st.text_area("Enter the content to summarize:")
# #summary_length = st.selectbox("Select summary length:", ["brief", "detailed"])

# if st.button("Summarize Content"):
#     summary = summarize_content(long_content)
#     st.write(summary)

############################################

import streamlit as st
import openai
import os
from transformers import pipeline
import fitz  # PyMuPDF

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load pre-trained summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    """Extracts text from each page of the uploaded PDF file."""
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Summarize content in manageable chunks
def summarize_content(text, max_chars=500):
    """Summarizes the extracted text in chunks."""
    summaries = []
    for i in range(0, len(text), max_chars):
        chunk = text[i:i + max_chars]
        summary = summarizer(chunk, max_length=130, min_length=50, do_sample=False)[0]['summary_text']
        summaries.append(summary)
    return " ".join(summaries)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.write(f"You: {message['content']}")
    else:
        st.write(f"Chatbot: {message['content']}")

# Chat interface
user_input = st.text_input("You:", key="user_input")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    # Bot's response
    response = f"I'm here to help! You said: {user_input}"
    st.session_state.messages.append({"role": "assistant", "content": response})

# File upload for document summarization
pdf_file = st.file_uploader("Upload a PDF document for summarization", type="pdf")

if pdf_file:
    with st.spinner("Extracting and summarizing text..."):
        # Extract text from the PDF file
        text = extract_text_from_pdf(pdf_file)
        # Summarize the extracted text
        summary = summarize_content(text)
        # Display the summarized content in chat history
        st.session_state.messages.append({"role": "assistant", "content": summary})
        st.write(f"Chatbot: {summary}")

# Reset chat history
if st.button("Reset Chat"):
    st.session_state.messages = []

