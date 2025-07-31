# RAG with OpenAI LangChain
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

load_dotenv()

# Load your document
loader = TextLoader('./managing-a-mobile-project-in-an-agile-environment.txt')
documents = loader.load()

# Split text into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_splitter.split_documents(documents)

# Embeddings and vector store (Chroma)
embeddings = OpenAIEmbeddings()
store = Chroma.from_documents(texts, embeddings, collection_name="managing-a-Mobile-Project")

# LLM: GPT-4.1-nano (OpenAI)
llm = ChatOpenAI(
    model="gpt-4.1-nano",
    temperature=0,
)

# Retrieval QA chain
chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=store.as_retriever()
)

# Run a question
print(chain.run("What is the role of the Product Owner and Scrum Master in project delivery?"))
