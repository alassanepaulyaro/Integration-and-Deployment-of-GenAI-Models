from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/")
async def root():
    return {"message": "FastAPI server is running. Use /generate endpoint for content generation."}

class Request(BaseModel):
    prompt: str

@app.post("/generate")
async def generate_content(request: Request):
    try:
        completion = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[{"role": "user", "content": request.prompt}]
        )
        ai_response = completion.choices[0].message.content
        return {"response": ai_response}
    except Exception as e:
        return {"error": str(e)}
