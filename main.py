from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import google.generativeai as genai
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Configure Gemini API (Ensure your GEMINI_API_KEY environment variable is set)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

class TravelRequest(BaseModel):
    name: str
    destination: str
    days: int
    budget: float
    interests: str
    travel_style: str
    technique: str  # 'zero-shot', 'few-shot', or 'structured'

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate-travel-plan")
async def generate_travel_plan(data: TravelRequest):
    if data.technique == "zero-shot":
        prompt = f"""
        Analyze the preferences of {data.name} visiting {data.destination} for {data.days} days with a budget of ${data.budget}. 
        Interests: {data.interests}. Travel Style: {data.travel_style}.
        Suggest places to visit, create a day-by-day itinerary, and recommend activities within the budget.
        """
    
    elif data.technique == "few-shot":
        prompt = f"""
        Here are examples of travel itineraries:
        Example 1:
        Name: John | Destination: Paris | Days: 3 | Budget: $600 | Style: Solo | Interests: History, Food
        Itinerary: Day 1: Louvre Museum ($20), Bistro lunch ($30). Day 2: Eiffel Tower ($25). Day 3: Seine cruise ($40).
        
        Example 2:
        Name: Sarah | Destination: Tokyo | Days: 3 | Budget: $1000 | Style: Family | Interests: Shopping, Nature
        Itinerary: Day 1: Shinjuku shopping. Day 2: Ueno Park (Free). Day 3: Shibuya Crossing.

        Now, generate a personalized travel plan for:
        Name: {data.name}
        Destination: {data.destination}
        Days: {data.days}
        Budget: ${data.budget}
        Interests: {data.interests}
        Travel Style: {data.travel_style}
        """
        
    elif data.technique == "structured":
        prompt = f"""
        Generate a travel itinerary for {data.name} going to {data.destination} for {data.days} days. 
        Budget: ${data.budget}, Interests: {data.interests}, Style: {data.travel_style}.
        Follow these steps internally:
        1. Analyze user preferences.
        2. Consider the available budget.
        3. Consider the number of travel days.
        4. Select suitable attractions and activities.
        5. Create a day-by-day itinerary.
        Provide short justifications explaining why each recommendation was selected.
        """
    else:
        prompt = f"Create a travel plan for {data.destination}."

    response = model.generate_content(prompt)
    return {"plan": response.text}