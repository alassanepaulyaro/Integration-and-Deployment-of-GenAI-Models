import os
from dotenv import load_dotenv
from langchain_community.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# Load environment variables from .env
load_dotenv()

# Load model and tokenizer locally
model_name = "google/flan-t5-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Create pipeline
text_pipeline = pipeline(
    "text2text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=64,
    temperature=0
)

# Wrap with LangChain
llm = HuggingFacePipeline(pipeline=text_pipeline)

prompt = "What are good fitness tips?"

print(llm.invoke(prompt))