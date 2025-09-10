from fastapi import FastAPI, Request, Body
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app= FastAPI()

app.mount("/static", StaticFiles(directory="static", name="static"))   

templates= Jinja2Templates(directory= "templates")

@app.get("/",response_class=HTMLResponse)
def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/chat", response_class= HTMLResponse)
def chatWindow(request: Request):
    return templates.TemplateResponse("chatWindow.html",{"request": request})

@app.post("/query", response_class=JSONResponse)
async def chat():



