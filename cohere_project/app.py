import cohere
import streamlit as st

# Initialize cohere client - handles both local (secrets.toml) and Streamlit Cloud (secrets)
def get_cohere_client():
    # Try to get API key from Streamlit secrets (for both local and cloud deployment)
    try:
        api_key = st.secrets["COHERE_API_KEY"]
    except (KeyError, FileNotFoundError):
        st.error("⚠️ Cohere API key not found. Please configure your API key.")
        st.info("For local development: Add COHERE_API_KEY to .streamlit/secrets.toml")
        st.info("For Streamlit Cloud: Add COHERE_API_KEY to your app secrets")
        st.stop()
    
    return cohere.ClientV2(api_key=api_key)

# Initialize cohere client
co = get_cohere_client()

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