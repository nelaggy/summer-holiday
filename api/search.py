from fastapi import APIRouter
from pydantic import BaseModel, Field
from openai import OpenAI
from dotenv import load_dotenv
import httpx  # Async HTTP requests
import os
import re

# Load environment varialbes from .env file
load_dotenv()

# Router for modular design - imported into main.py
router = APIRouter()

# Load an OpenAI API key and activate client
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Set this in your environment variables
client = OpenAI(api_key=OPENAI_API_KEY)

class Filters(BaseModel):
    location: str | None
    budget: float | None
    num_people: int | None
    start_date: str | None
    end_date: str | None
    dynamic_filters: dict[str,] | None

    def __init__(self, user_input, budget, num_adults, num_children, start_date, end_date, dynamic_filters):
        self.user_input = user_input
        self.budget = budget
        self.num_people = num_adults
        self.num_children = num_children
        self.start_date = start_date
        self.end_date = end_date
        self.dynamic_filters = dynamic_filters
        self.hard_dict = {"Filter1" : None, "Filter2" : None}
    
   

def city_decider(self):  
    # Exclude 'hard_dict' from the dictionary
    filters_dict = {key: value for key, value in vars(self).items() if key != "hard_dict"}

    prompt_message = f"""
    Preferences:
    {filters_dict}

    Hard Filters:
    {self.hard_dict}

    Based on the preferences, please suggest the most suitable city. Respond strictly in the following format:

    "City Name: [City Name]"

    Also, match the hard filters to the user input and create a dictionary of relevant filters in the following format:

    "[Filter Name]: [Boolean Value]"

    Ensure the response contains only the required information and no additional text.
    """

    messages = [{"role": "user", "content": prompt_message}]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=500
    )

    response_content = response.choices[0].message.content

    # Extract City Name
    match = re.search(r'City Name:\s*(.+)', response_content)
    if match:
        self.location = match.group(1).strip()

    # Extract and update hard filter values
    for key in self.hard_dict.keys():
        match = re.search(rf"\[{re.escape(key)}\]:\s*(True|False)", response_content)
        if match:
            self.hard_dict[key] = match.group(1).strip() == "True"

    result = ()
    return self.model_dump()




#reviews and hotel description and facility 

# Obselete Function defined assuming lack of openai library
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



@router.get("/search")
async def search(location: str | None = None, budget: float | None = None, num_people: int | None = None,
                 start_date: str | None = None, end_date: str | None = None, dynamic_filters: dict[str, str] | None = None):
    """Handles a search request and queries ChatGPT."""
    filter = Filters(location, budget, num_people, start_date, end_date, dynamic_filters)
    completion = client.chat.completions.create(model="gpt-3.5-turbo", store=True,
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
