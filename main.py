from fastapi import FastAPI, Request, Body
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from langchain.agents.graph import Graph, Node
from langchain.chat_models import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory 
from langchain.agents.graph.tool_node import ToolNode
from langchain.agents.graph.llm_node import LLMNode
import os

gemini_key=os.getenv("GOOGLE_API_KEY")

llm= ChatGoogleGenerativeAI(model= "gemini-2.5-pro", api_key=gemini_key)

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

memory= ConversationBufferMemory(memory_key="chat_history", return_messages=True)

llmNode=LLMNode(llm=llm, prompt_template="Here is an upcoming text snippet. Your job is to be a social coach to the user. Be empathetic, supportive but also practical in your responses.", input_keys=[], output_key="", memory=memory)

toolNode1= ToolNode(tool=summary, input_keys=["input"], output_key="summary")
toolNode2= ToolNode(tool=sentimentAnalysis, input_keys=["input"], output_key="sentimentAnalysis")
toolNode3= ToolNode(tool=toneAnalysis, input_keys=["input"], output_key="toneAnalysis")
toolNode4= ToolNode(tool=advice, input_keys=["summary", "sentimentAnalysis", "toneAnalysis"], output_key="advice")

graph=Graph()
graph.add_node("summary_node", toolNode1)
graph.add_node("sentiment_node", toolNode2)
graph.add_node("tone_node", toolNode3)
graph.add_node("advice_node", toolNode4, parent_nodes=["summary_node", "sentiment_node", "tone_node"])

inputs={}

@app.post("/query", response_class=JSONResponse)
async def chat(data: dict=Body(...)):
    AIresponse= .run(data["query"])
    return {"resp": AIresponse}