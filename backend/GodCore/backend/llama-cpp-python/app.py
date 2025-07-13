from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx
import os

BACKEND_URL = os.getenv(
    "LLAMA_BACKEND_URL", "http://localhost:8000/v1/chat/completions"
)

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def get_dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/chat")
async def chat_api(message: str = Form(...)):
    payload = {"model": "mistral", "messages": [{"role": "user", "content": message}]}
    async with httpx.AsyncClient() as client:
        resp = await client.post(BACKEND_URL, json=payload)
        result = resp.json()
    # Safely extract text, fallback if error
    content = (
        result.get("choices", [{}])[0].get("message", {}).get("content", "No response.")
    )
    return JSONResponse({"response": content})
