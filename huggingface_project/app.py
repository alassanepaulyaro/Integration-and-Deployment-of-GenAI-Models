import os
import streamlit as st
from dotenv import load_dotenv
from langchain_community.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="GenAI Question Answering",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cache model loading for better performance
@st.cache_resource
def load_model():
    """Load and cache the Hugging Face model and tokenizer"""
    with st.spinner("Loading AI model... This may take a few minutes on first run."):
        model_name = "google/flan-t5-base"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        
        # Create pipeline
        text_pipeline = pipeline(
            "text2text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=128,
            temperature=0.1
        )
        
        # Wrap with LangChain
        llm = HuggingFacePipeline(pipeline=text_pipeline)
        return llm

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "model_loaded" not in st.session_state:
    st.session_state.model_loaded = False

# Sidebar
with st.sidebar:
    st.title("🤖 GenAI Assistant")
    st.markdown("### Settings")
    
    # Model parameters
    max_tokens = st.slider("Max Tokens", min_value=50, max_value=512, value=128)
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.1, step=0.1)
    
    st.markdown("### About")
    st.info(
        "This application uses Google's FLAN-T5-base model "
        "to answer your questions. Ask anything!"
    )
    
    # Clear chat history
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Main content
st.title("🤖 GenAI Question Answering")
st.markdown("Ask me anything! I'm powered by FLAN-T5-base model.")

# Load model
try:
    if not st.session_state.model_loaded:
        llm = load_model()
        st.session_state.llm = llm
        st.session_state.model_loaded = True
    else:
        llm = st.session_state.llm
except Exception as e:
    st.error(f"Error loading model: {str(e)}")
    st.stop()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to know?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Update pipeline parameters
                llm.pipeline.task_kwargs = {
                    "max_new_tokens": max_tokens,
                    "temperature": temperature
                }
                
                response = llm.invoke(prompt)
                st.markdown(response)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Example questions
if not st.session_state.messages:
    st.markdown("### 💡 Example Questions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🏃‍♂️ What are good fitness tips?"):
            st.session_state.messages.append({"role": "user", "content": "What are good fitness tips?"})
            st.rerun()
    
    with col2:
        if st.button("🍽️ How to cook pasta?"):
            st.session_state.messages.append({"role": "user", "content": "How to cook pasta?"})
            st.rerun()
    
    with col3:
        if st.button("🧠 Explain machine learning"):
            st.session_state.messages.append({"role": "user", "content": "Explain machine learning in simple terms"})
            st.rerun()

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Powered by Google FLAN-T5-base model via Hugging Face Transformers"
    "</div>", 
    unsafe_allow_html=True
)