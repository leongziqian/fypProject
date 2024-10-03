
import streamlit as st
from transformers import pipeline

# Load a pre-trained summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)

def summarize_content(text):
    summary = summarizer(text, max_length=130, min_length=50, do_sample=False, clean_up_tokenization_spaces=True)
    return summary[0]['summary_text']

# Set up the Streamlit app
st.title("AI Marketing Copy Generator and Summarization Tool")



# Content Summarization Tool
st.header("Content Summarization Tool")
long_content = st.text_area("Enter the content to summarize:")
#summary_length = st.selectbox("Select summary length:", ["brief", "detailed"])

if st.button("Summarize Content"):
    summary = summarize_content(long_content)
    st.write(summary)
