# Streamlit app for RAG (Retrieval-Augmented Generation) using OpenAI, and LangChain 
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader, PDFPlumberLoader, UnstructuredWordDocumentLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
import os
import tempfile

load_dotenv()

st.set_page_config(page_title="Multi-Document RAG with GPT-4.1-nano", layout="wide")
st.title("📄🔎 Multi-Document Retrieval QA (TXT, PDF, DOCX) with GPT-4.1-nano")

# Multi-file upload
uploaded_files = st.file_uploader(
    "Upload one or more files (.txt, .pdf, .docx) to build your QA knowledge base:",
    type=["txt", "pdf", "docx"], accept_multiple_files=True
)

def load_document(file_path, ext):
    """Return LangChain document object from file and extension"""
    if ext == ".txt":
        return TextLoader(file_path).load()
    elif ext == ".pdf":
        return PDFPlumberLoader(file_path).load()
    elif ext == ".docx":
        return UnstructuredWordDocumentLoader(file_path).load()
    else:
        raise ValueError(f"Unsupported file extension: {ext}")

# Prepare the pipeline only when 'Start' is pressed
if st.button("Start QA System"):
    with st.spinner("Loading, chunking & embedding your documents..."):
        temp_files = []
        all_docs = []
        # Save each file to a temp location and load content
        for up_file in uploaded_files:
            suffix = os.path.splitext(up_file.name)[-1].lower()
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tf:
                tf.write(up_file.read())
                temp_files.append(tf.name)
                docs = load_document(tf.name, suffix)
                all_docs.extend(docs)
        if not all_docs:
            st.error("No valid documents loaded.")
            st.stop()
        # Split all docs
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents(all_docs)
        # Embeddings & vectorstore
        embeddings = OpenAIEmbeddings()
        store = Chroma.from_documents(texts, embeddings, collection_name="multi-doc-rag")
        # LLM: GPT-4.1-nano
        llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0)
        # RetrievalQA chain
        chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=store.as_retriever()
        )
        st.session_state.chain = chain
        st.session_state.temp_files = temp_files  # to clean up later
        st.success("Ready! Ask your question below:")

if "chain" in st.session_state:
    user_query = st.text_input("Your question:", "")
    if st.button("Ask"):
        with st.spinner("Searching..."):
            answer = st.session_state.chain.run(user_query)
        st.markdown(f"**Answer:**\n\n{answer}")

    if st.button("Reset QA System"):
        del st.session_state.chain
        if "temp_files" in st.session_state:
            for f in st.session_state.temp_files:
                try:
                    os.remove(f)
                except Exception:
                    pass
            del st.session_state.temp_files
        st.experimental_rerun()

st.caption("Supports TXT, PDF, DOCX. Uses Chroma, OpenAI GPT-4.1-nano, and your .env for API key.")
