# Prompt Chaining with HuggingFace + LangChain 
import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# Load environment variables from .env (optional)
load_dotenv()

# Load model and tokenizer locally
model_name = "google/flan-t5-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Create HuggingFace pipeline (do NOT pass temperature if not supported)
text_pipeline = pipeline(
    "text2text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=64
)

# Use the new langchain_huggingface integration
llm = HuggingFacePipeline(pipeline=text_pipeline)

# Create a prompt template with a variable
template = "You are a naming consultant for new companies. What is a good name for a company that makes {product}?"
prompt = PromptTemplate.from_template(template)

# Use chaining via the | operator
chain = prompt | llm

# Run the chain with the input variable using .invoke()
result = chain.invoke({"product": "colorful socks"})
print(result)
