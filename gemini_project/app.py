import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
# Import new chain components
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate # More modern prompt template
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
# Ensure the API key is loaded and configured
google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    st.error("GOOGLE_API_KEY not found in environment variables. Please set it.")
    # Stop the app if API key is missing
    st.stop() 
genai.configure(api_key=google_api_key)

# Function to extract text from PDF files
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# Function to split text into chunks of specified size
def get_text_chunks(text):
    # Use a large chunk size and overlap suitable for PDF documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

# Function to create a vector database from text chunks
def get_vector_store(text_chunks):
    # Initialize Google Generative AI Embeddings model
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    # Create FAISS vector store from text chunks and embeddings
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    # Save the vector store locally for later use
    vector_store.save_local("faiss_index")
    st.success("Vector store created and saved locally.")


# Function to set up a question-answer chain with an AI model
def get_conversational_chain():
    # Use ChatPromptTemplate for a more robust and flexible prompt structure
    prompt = ChatPromptTemplate.from_messages([
        ("system", """
        Answer the question with detail from the context provided, make sure to give all the details.
        If the answer is not in the context, please say "I don't know", do not provide a wrong answer.\n\n
        Context: \n{context}\n
        """),
        # Changed {question} to {input} to match the key passed by create_retrieval_chain
        ("human", "Question: \n{input}\n") 
    ])

    # Initialize the ChatGoogleGenerativeAI model with the recommended 'gemini-2.5-flash'
    # This model is optimized for speed and cost-efficiency.
    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)

    # Create a chain that combines documents and answers questions
    # This replaces load_qa_chain(model, chain_type="stuff", prompt=prompt)
    document_chain = create_stuff_documents_chain(model, prompt)

    return document_chain

# Function to process user questions and generate a response
def user_input(user_question):
    # Initialize Google Generative AI Embeddings model
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    # Load the locally saved FAISS vector store
    # allow_dangerous_deserialization=True is necessary for loading local FAISS indices
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    
    # Create a retriever from the vector store for document similarity search
    retriever = new_db.as_retriever()

    # Get the document chain
    document_chain = get_conversational_chain()

    # Create a retrieval chain that first retrieves documents, then passes them to the document chain
    # This chain handles both document retrieval and question answering
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    # Invoke the retrieval chain with the user's question
    # The retrieval_chain expects 'input' as the key for the user's question
    try:
        response = retrieval_chain.invoke({"input": user_question})
        # The output structure of retrieval_chain.invoke typically includes 'answer' and 'context'
        st.write("Reply: ", response["answer"])
    except Exception as e:
        st.error(f"An error occurred while getting a response: {e}")
        st.info("Please ensure your Google API key is valid and the model is available.")


# Configure the Streamlit user interface
def main():
    st.set_page_config(page_title="Chat PDF", page_icon="🤖")

    st.header("Chat with multiple PDFs using Google Gemini AI")

    user_question = st.text_input("Ask a question from your PDFs")

    if user_question:
        user_input(user_question)

    with st.sidebar:
        st.title("Menu:")

        pdf_docs = st.file_uploader("Upload PDFs", type=["pdf"], accept_multiple_files=True)
        # Changed button text for clarity
        if st.button("Create Vector Store"): 
            if pdf_docs:
                with st.spinner("Extracting text from PDFs and creating vector store..."):
                    raw_text = get_pdf_text(pdf_docs)
                    text_chunks = get_text_chunks(raw_text)
                    get_vector_store(text_chunks)
            else:
                st.warning("Please upload PDF files first.")
            
# Run the application
if __name__ == "__main__":
    main()