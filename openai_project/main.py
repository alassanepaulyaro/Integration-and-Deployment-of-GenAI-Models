from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

completion = client.chat.completions.create(
    model="gpt-4.1-nano",
    store=True,
    messages=[
        {"role": "user", "content": "hello"}
    ]
)

print(completion.choices[0].message.content)