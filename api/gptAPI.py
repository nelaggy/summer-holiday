from fastapi import FastAPI
from openai import OpenAI
from dotenv import load_dotenv
import httpx  # Async HTTP requests
import os

app = FastAPI()

# Load environment varialbes from .env file
load_dotenv()

# Load an OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Set this in your environment variables

client = OpenAI(api_key=OPENAI_API_KEY)

"""class Filters(BaseModel):
    location: str
    budget: float
    num_people: int
    start_date: str
    end_date: str
    dynamic_filters: dict[str, str]"""

async def query_chatgpt(prompt: str) -> str:
    """Send a search query to OpenAI's GPT API and return the response."""
    url = "https://api.openai.com/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "gpt-4",  # Choose model (e.g., "gpt-3.5-turbo" for cheaper option)
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 200
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)
        response_json = response.json()
    
    return response_json["choices"][0]["message"]["content"]



@app.get("/search")
async def search(q: str): # If using query class, add after str = FastAPI.Query(..., min_length=1, title="Search Query")
    """Handles a search request and queries ChatGPT."""

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    store=True,
    messages=[
        {"role": "user", "content": q}
    ]
    )
    
    return completion.choices[0].message

    chatgpt_response = await query_chatgpt(f"Search for: {q}")
    
    return {
        "query": q,
        "results": [chatgpt_response]  # Returning as a list for consistency
    }
