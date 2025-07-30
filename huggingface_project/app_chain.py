# Complete Streamlit + LangChain HuggingFace Chaining Example
import os
import streamlit as st
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# Load environment variables (if any)
load_dotenv()

st.set_page_config(
    page_title="GenAI Company Name & QA",
    page_icon="🤖",
    layout="wide"
)

# --- Caching the model and pipeline ---
@st.cache_resource
def load_llm(max_new_tokens, temperature):
    """Load and cache Hugging Face FLAN-T5-base as LangChain LLM."""
    model_name = "google/flan-t5-base"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    hf_pipeline = pipeline(
        "text2text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
    )
    llm = HuggingFacePipeline(pipeline=hf_pipeline)
    return llm

# --- Sidebar configuration ---
with st.sidebar:
    st.title("🤖 GenAI Company Name & QA Assistant")
    st.markdown("### Model Settings")
    max_tokens = st.slider("Max Tokens", 50, 512, 128, 8)
    temperature = st.slider("Temperature", 0.0, 1.0, 0.1, 0.05)
    mode = st.radio(
        "Select Mode",
        ["Company Naming (with product)", "General Question Answering"],
        index=0
    )
    st.markdown("### About")
    st.info("This app uses Google's FLAN-T5-base model (HuggingFace). Powered by LangChain.")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# --- Session state initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Load (and cache) the model ---
llm = load_llm(max_tokens, temperature)

# --- Prompt Templates ---
naming_template = "You are a naming consultant for new companies. What is a good name for a company that makes {product}?"
qa_template = "{question}"

naming_prompt = PromptTemplate.from_template(naming_template)
qa_prompt = PromptTemplate.from_template(qa_template)

# --- Chains (modern operator syntax) ---
naming_chain = naming_prompt | llm
qa_chain = qa_prompt | llm

# --- UI ---
st.title("🤖 GenAI Company Name & QA Chatbot")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chat input ---
if mode == "Company Naming (with product)":
    prompt_label = "Describe the product (e.g. 'colorful socks')"
else:
    prompt_label = "Ask a question"

if user_input := st.chat_input(prompt_label):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                if mode == "Company Naming (with product)":
                    # Use naming_chain with the variable
                    result = naming_chain.invoke({"product": user_input})
                else:
                    # Use QA chain
                    result = qa_chain.invoke({"question": user_input})
                # result is a dict or string (depending on pipeline)
                response = result if isinstance(result, str) else result[0]['generated_text']
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Sorry, I encountered an error: {str(e)}")
                st.session_state.messages.append(
                    {"role": "assistant", "content": f"Sorry, I encountered an error: {str(e)}"}
                )

# --- Example Inputs for First-Time User ---
if not st.session_state.messages:
    st.markdown("### 💡 Example Prompts")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏷️ Suggest a name for a company that makes smart umbrellas"):
            st.session_state.messages.append({"role": "user", "content": "smart umbrellas"})
            st.session_state.mode = "Company Naming (with product)"
            st.rerun()
    with col2:
        if st.button("🧠 What are good fitness tips?"):
            st.session_state.messages.append({"role": "user", "content": "What are good fitness tips?"})
            st.session_state.mode = "General Question Answering"
            st.rerun()

# --- Footer ---
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Powered by Google FLAN-T5-base model via Hugging Face Transformers and LangChain"
    "</div>",
    unsafe_allow_html=True
)
