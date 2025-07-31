# Sequential LangChain with gpt2-medium
import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# Load environment variables (optional)
load_dotenv()

# --- HuggingFace LLM: gpt2-medium ---
model_name = "gpt2-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
hf_pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=64,
    temperature=0.7,
    do_sample=True,
    pad_token_id=tokenizer.eos_token_id
)
llm = HuggingFacePipeline(pipeline=hf_pipeline)

# --- Step 1: Generate company name ---
first_prompt = PromptTemplate.from_template(
    "What is a good name for a company that makes {product}?"
)

# --- Step 2: Generate catchphrase for company ---
second_prompt = PromptTemplate.from_template(
    "Write a catch phrase for the following company: {company_name}"
)

# --- Chain: product -> company_name -> catchphrase ---
chain = (
    first_prompt
    | llm
    | (lambda name: {"company_name": (
            name[0]['generated_text'].strip() if isinstance(name, list) else name.strip()
        )})
    | second_prompt
    | llm
)

result = chain.invoke({"product": "colorful socks"})
# Handle the result type (str or list)
if isinstance(result, str):
    print(result.strip())
elif isinstance(result, list):
    print(result[0]['generated_text'].strip())
else:
    print(result)
