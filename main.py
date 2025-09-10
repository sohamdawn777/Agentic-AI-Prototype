from fastapi import FastAPI, Request, Body
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app= FastAPI()

app.mount("/static", StaticFiles(directory="static", name="static"))   

templates= Jinja2Templates(directory= "templates")
@app.get("/chat", response_class= HTMLResponse)
async def chat(request: Request):
    return templates.TemplateResponse("chatWindow.html",{"request": request})