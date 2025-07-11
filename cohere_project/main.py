import cohere
import os
from dotenv import load_dotenv

load_dotenv()

co = cohere.ClientV2(os.getenv("COHERE_API_KEY"))
response = co.chat(
    model="command-r-plus", 
    messages=[{"role": "user", "content": "hello world!"}]
)

print(response.message.content[0].text)