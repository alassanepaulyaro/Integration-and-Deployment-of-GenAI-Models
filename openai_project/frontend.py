import streamlit as st
import requests

def run_streamlit():
    st.title("AI Content Generator")
    st.write("Enter a prompt to generate content.")

    API_URL = "http://localhost:8001/generate"  # Le port doit correspondre à FastAPI

    user_input = st.text_area("Enter your prompt:")

    if st.button("Generate"):
        if user_input.strip():
            with st.spinner("Generating..."):
                try:
                    response = requests.post(API_URL, json={"prompt": user_input})
                    if response.status_code == 200:
                        result = response.json()
                        if "response" in result:
                            st.subheader("Generated Content")
                            st.write(result["response"])
                        else:
                            st.error(f"Error: {result.get('error', 'Unknown error')}")
                    else:
                        st.error(f"Error: Unable to contact API. Status code {response.status_code}")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter a prompt before clicking Generate.")

if __name__ == "__main__":
    run_streamlit()
