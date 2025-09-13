from flask import Flask, render_template, request, jsonify
import os
from agent import Agent

gemini_key=os.getenv("GOOGLE_API_KEY")

app=Flask(__name__)
@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/query", methods=["POST"])
def chat():
    data=request.get_json()
    try:
        AIresponse= agent.run(data["query"])
        return jsonify({"resp": AIresponse})
    except Exception as e:
        try:
            queryCleaned= agent.run(f"Understand and summarize this query with your own nuance and understanding: \n{data['query']}")
            AIresponse= agent.run(queryCleaned)
            return jsonify({"resp": AIresponse})
        except Exception as e:
            return jsonify({"resp": "Your response could not be understood"})    
    
if __name__=="__main__":
    port=int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0", port=port)    