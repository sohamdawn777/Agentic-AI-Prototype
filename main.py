from fastapi import FastAPI, Request, Body
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from langchain_google_vertexai import ChatVertexAI
from langchain.agents import AgentType, Tool, initialize_agent
from langchain.memory import ConversationBufferMemory 
from dotenv import load_dotenv
import os

load_dotenv("auth.env")
os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

llm= ChatVertexAI(model= "gemini-2.5-pro")

def summary(input):
    prompt=f"Summarize the full text given below in 2 to 3 sentences\n\n{input}"
    return llm.invoke(prompt).content
    
def sentimentAnalysis(input):
    prompt = f"Analyze the sentiment of the following text. Reply with Positive, Negative, or Neutral:\n\n{input}"
    return llm.invoke(prompt).content
    
def toneAnalysis(input):
    prompt=f"Detect the tone (formal, casual, nervous, confident, etc.) of this text:\n\n{input}"
    return llm.invoke(prompt).content
    
def advice(input):
    prompt=f"Based on this text, give one short motivational advice:\n\n{input}"
    return llm.invoke(prompt).content
    
app= FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")  

templates= Jinja2Templates(directory= "templates")

@app.get("/",response_class=HTMLResponse)
def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/chat", response_class= HTMLResponse)
def chatWindow(request: Request):
    return templates.TemplateResponse("chatWindow.html",{"request": request})

tool1= Tool(name="summary", func=summary, description="This summarizes the user query.")
tool2= Tool(name="sentimentAnalysis", func=sentimentAnalysis, description="This analyses the sentiments of the user query.")
tool3= Tool(name="toneAnalysis", func=toneAnalysis, description="This analyses the tone of the user query.")
tool4= Tool(name="advice", func=advice, description="This gives a short advice to the user.")
tools= [tool1, tool2, tool3, tool4]

memory= ConversationBufferMemory(memory_key="chat_history", return_messages=True)

agent=initialize_agent(tools=tools, llm=llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, memory=memory, verbose=True)

@app.post("/query", response_class=JSONResponse)
async def chat(data: dict=Body(...)):
    AIresponse= agent.run(data["query"])
    return {"resp": AIresponse}