# Streamlit + Sequential LangChain
import os
import streamlit as st
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# Load environment variables (optional)
load_dotenv()

st.set_page_config(
    page_title="GenAI Company Name & Catchphrase - GPT2-Medium",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_resource
def load_llm(max_new_tokens, temperature):
    model_name = "gpt2-medium"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    text_pipeline = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id  # To avoid HF warnings
    )
    llm = HuggingFacePipeline(pipeline=text_pipeline)
    return llm

# Sidebar
with st.sidebar:
    st.title("🤖 Company Naming Assistant - GPT2-Medium")
    max_tokens = st.slider("Max Tokens", 10, 100, 40)
    temperature = st.slider("Temperature", 0.0, 1.5, 0.7, 0.05)
    st.markdown("### About")
    st.info("Generates a company name and a slogan from your product idea (gpt2-medium, fast & lightweight).")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Chat session initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# Load the model
llm = load_llm(max_tokens, temperature)

# Prompts
name_prompt = PromptTemplate.from_template(
    "Suggest a creative name for a company that makes {product}."
)
catchphrase_prompt = PromptTemplate.from_template(
    "Create a catchy slogan for the company: {company_name}."
)

def sequential_chain(product: str):
    # Step 1: Company Name
    name_chain = name_prompt | llm
    company_name = name_chain.invoke({"product": product})
    if isinstance(company_name, list):
        company_name = company_name[0]['generated_text'].strip()
    elif isinstance(company_name, dict):
        company_name = company_name['generated_text'].strip()
    company_name = company_name.split("\n")[0].strip(".-– ")

    # Step 2: Slogan
    catchphrase_chain = catchphrase_prompt | llm
    catchphrase = catchphrase_chain.invoke({"company_name": company_name})
    if isinstance(catchphrase, list):
        catchphrase = catchphrase[0]['generated_text'].strip()
    elif isinstance(catchphrase, dict):
        catchphrase = catchphrase['generated_text'].strip()
    catchphrase = catchphrase.split("\n")[0].strip(".-– ")
    return company_name, catchphrase

# Main UI
st.title("🤖 Company Name & Catchphrase (GPT2-Medium)")
st.markdown("Describe a product to get a company name and a catchy slogan!")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if product := st.chat_input("Describe a product (e.g. eco-friendly shoes, foldable smartphone)"):

    st.session_state.messages.append({"role": "user", "content": product})
    with st.chat_message("user"):
        st.markdown(product)
    with st.chat_message("assistant"):
        with st.spinner("Generating name and slogan..."):
            try:
                company_name, catchphrase = sequential_chain(product)
                st.markdown(f"**Company Name:** {company_name}")
                st.markdown(f"**Slogan:** {catchphrase}")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"**Company Name:** {company_name}\n\n**Slogan:** {catchphrase}"
                })
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Error: {str(e)}"
                })

# Example starters for new users
if not st.session_state.messages:
    st.markdown("### 💡 Example ideas:")
    st.markdown("- eco-friendly shoes")
    st.markdown("- foldable smartphone")
    st.markdown("- solar-powered smart lamp")

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Powered by gpt2-medium, Hugging Face, and LangChain"
    "</div>",
    unsafe_allow_html=True
)
