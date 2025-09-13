from flask import Flask, render_template, request, jsonify
import os
from agent import Agent

gemini_key=os.getenv("GOOGLE_API_KEY")
agentInstance=Agent(gemini_key)
agentInstance.initialize_the_agent()

app=Flask(__name__)
@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/query", methods=["POST"])
def chat():
    data=request.get_json()
    try:
        AIresponse= agentInstance.run_agent(data["query"])
        return jsonify({"resp": AIresponse})
    except Exception as e:
        try:
            queryCleaned= agentInstance.run_agent(f"Understand and summarize this query with your own nuance and understanding: \n{data['query']}")
            AIresponse= agentInstance.run_agent(queryCleaned)
            return jsonify({"resp": AIresponse})
        except Exception as e:
            return jsonify({"resp": f"Your response could not be understood....{e}"})    
    
if __name__=="__main__":
    port=int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0", port=port)    