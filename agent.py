from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentType, Tool, initialize_agent
from langchain.memory import ConversationBufferMemory 

class Agent:
    def __init__(self, gemini_key):
        self.llm= ChatGoogleGenerativeAI(model= "gemini-2.5-flash", api_key=gemini_key)
        self.memory= ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    def setup_tools(self):
        def summary(input):
            prompt=f"Summarize the full text given below in 2 to 3 sentences\n\n{input}"
            return self.llm.invoke(prompt).content
        def sentimentAnalysis(input):
            prompt = f"Analyze the sentiment of the following text. Reply with Positive, Negative, or Neutral:\n\n{input}"
            return self.llm.invoke(prompt).content
        def toneAnalysis(input):
            prompt=f"Detect the tone (formal, casual, nervous, confident, etc.) of this text:\n\n{input}"
            return self.llm.invoke(prompt).content
        def advice(input):
            prompt=f"Based on this text, give one short motivational advice:\n\n{input}"
            return self.llm.invoke(prompt).content
        tool1= Tool(name="summary", func=summary, description="This summarizes the user query.")
        tool2= Tool(name="sentimentAnalysis", func=sentimentAnalysis, description="This analyses the sentiments of the user query.")
        tool3= Tool(name="toneAnalysis", func=toneAnalysis, description="This analyses the tone of the user query.")
        tool4= Tool(name="advice", func=advice, description="This gives a short advice to the user.")
        self.tools=[tool1, tool2, tool3, tool4]
    def initialize_the_agent(self):
        self.setup_tools()
        self.agent=initialize_agent(tools=self.tools, llm=self.llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, memory=self.memory, verbose=True)
    def run_agent(self, query):
        return self.agent.run(query)    