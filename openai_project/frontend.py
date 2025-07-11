import streamlit as st
import requests
import os

def run_streamlit():
    st.title("AI Content Generator")
    st.write("Enter a prompt to generate content.")
    
    # Use environment variable to determine backend URL
    # In Docker Compose, use service name "backend"
    # In local development, use "localhost"
    backend_host = os.getenv("BACKEND_HOST", "localhost")
    API_URL = f"http://{backend_host}:8001/generate"
    
    user_input = st.text_area("Enter your prompt:")
    
    if st.button("Generate"):
        if user_input.strip():
            with st.spinner("Generating..."):
                try:
                    response = requests.post(API_URL, json={"prompt": user_input}, timeout=30)
                    
                    if response.status_code == 200:
                        result = response.json()
                        if "response" in result:
                            st.subheader("Generated Content")
                            st.write(result["response"])
                        else:
                            st.error(f"Error: {result.get('error', 'Unknown error')}")
                    else:
                        st.error(f"Error: Unable to contact API. Status code {response.status_code}")
                        
                except requests.exceptions.ConnectionError as e:
                    st.error("❌ Connection Error: Unable to connect to the AI service. Please try again later.")
                    
                except requests.exceptions.Timeout as e:
                    st.error("⏱️ Timeout Error: The AI service is taking too long to respond. Please try again.")
                    
                except Exception as e:
                    st.error("❌ An unexpected error occurred. Please try again.")
        else:
            st.warning("Please enter a prompt before clicking Generate.")

if __name__ == "__main__":
    run_streamlit()