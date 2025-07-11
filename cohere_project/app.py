import cohere
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize cohere client
co = cohere.ClientV2(os.getenv("COHERE_API_KEY"))

# Streamlit UI
st.title("Text Summarization with Cohere")

st.write("This app uses Cohere's API to summarize text. Enter the text you want to summarize below:")

# Text input from user
user_input = st.text_area("Enter text here:", height=300)

if st.button("Summarize"):
    if user_input.strip():
        with st.spinner("Summarizing..."):
            try:
                # Prepare the message for cohere
                message = f"Generate a concise summary of the following text\n{user_input}"
                
                # Call cohere API
                response = co.chat(
                    model="command-r-plus", 
                    messages=[{"role": "user", "content": message}]
                )
                
                # Display summarized text
                summary = response.message.content[0].text
                st.subheader("Summarized text:")
                st.write(summary)
            except Exception as e:
                st.error(f"An error occurred: {e}")
                
    else:
        st.warning("Please enter some text to summarize.")