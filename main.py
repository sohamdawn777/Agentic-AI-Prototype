from flask import Flask, render_template, request, jsonify
import os
from agent import Agent
from routing import Routing
from database import Database

gemini_key=os.getenv("GOOGLE_API_KEY")

agentInstance1=Agent(gemini_key)
agentInstance1.initialize_creative_agent()
agentInstance2=Agent(gemini_key)
agentInstance2.initialize_fallback_agent()

routingInstance=Routing(agentInstance1, agentInstance2, gemini_key)

app=Flask(__name__)
@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/apiKey")
def apiKey():
    return os.getenv("FIREBASE_API_KEY")
@app.route("/authDomain")
def authDomain():
    return os.getenv("FIREBASE_AUTH_DOMAIN")
@app.route("/projectId")
def projectId():
    return os.getenv("FIREBASE_PROJECT_ID")
@app.route("/appId")
def appId():
    return os.getenv("FIREBASE_APP_ID")

databaseInstance=Database(os.getenv("FIREBASE_PROJECT_ID"), os.getenv("FIREBASE_API_KEY"), agentInstance1.memory, agentInstance2.memory)

print("jhingalala whoop whoop")
    
@app.route("/users", methods=["POST"])
def users():
    data=request.get_json()
    databaseInstance.store(data["uid"])
    
@app.route("/query", methods=["POST"])
def chat():
    data=request.get_json()
    try:
        AIresponse= routingInstance.route(data["query"])
        return jsonify({"resp": AIresponse})
    except Exception as e:
        try:
            queryCleaned= routingInstance.route(f"Understand and summarize this query with your own nuance and understanding: \n{data['query']}")
            AIresponse= routingInstance.route(queryCleaned)
            return jsonify({"resp": AIresponse})
        except Exception as e:
            return jsonify({"resp": f"Your response could not be understood....{e}"})    

if __name__=="__main__":
    port=int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0", port=port)    