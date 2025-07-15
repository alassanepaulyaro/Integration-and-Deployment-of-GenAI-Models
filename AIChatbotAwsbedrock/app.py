from langchain_aws import BedrockLLM  # Modern import
from langchain.prompts import PromptTemplate
import boto3
import streamlit as st

# Access AWS credentials from Streamlit secrets
try:
    aws_access_key = st.secrets["AWS_ACCESS_KEY_ID"]
    aws_secret_key = st.secrets["AWS_SECRET_ACCESS_KEY"]
except KeyError:
    st.error("AWS credentials not found. Please check your .streamlit/secrets.toml file.")
    st.stop()

# Debug: Check if credentials are loaded (remove this in production)
if not aws_access_key or not aws_secret_key:
    st.error("AWS credentials are empty. Please check your .streamlit/secrets.toml file.")
    st.stop()

bedrock_client = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1",
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key  
)

st.set_page_config(page_title="AI Chatbot", layout="centered")
st.title("Bedrock Chatbot")

model_id = st.sidebar.selectbox("Select Model", ["anthropic.claude-v2", "anthropic.claude-v3"])

llm = BedrockLLM(
    model_id=model_id,
    client=bedrock_client,
    model_kwargs={"max_tokens_to_sample": 2000, "temperature": 0.9}
)

def my_chatbot(freeform_text):
    prompt = PromptTemplate(
        input_variables=["freeform_text"],
        template="{freeform_text}"
    )
    # Use the modern approach: prompt | llm
    chain = prompt | llm
    response = chain.invoke({'freeform_text': freeform_text})
    return {"text": response}

st.sidebar.header("Chat Settings")
freeform_text = st.sidebar.text_area(
    label="Enter your question", 
    placeholder="Ask me anything...", 
    max_chars=300
)

if st.sidebar.button("Get Response") and freeform_text:
    with st.spinner("Generating response..."):
        try:
            response = my_chatbot(freeform_text)
            st.subheader("Response:")
            st.write(response['text'])
        except Exception as e:
            st.error(f"Error: {str(e)}")
else:
    st.info("Please enter a question in the sidebar to get started.")