from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentType, Tool, initialize_agent
from langchain.memory import ConversationBufferMemory 

class Agent:
    def __init__(self, gemini_key):
        self.llm= ChatGoogleGenerativeAI(model= "gemini-2.5-flash", api_key=gemini_key)
        self.memory= ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    def setup_creative_tools(self):
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
        self.creative_tools=[tool1, tool2, tool3, tool4]
    def initialize_creative_agent(self):
        self.setup_creative_tools()
        self.creative_agent=initialize_agent(tools=self.creative_tools, llm=self.llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, memory=self.memory, verbose=True)
    def setup_fallback_tools(self):
        def clarify(input):
            return "I'm not sure I fully understand. Could you clarify your request?"
        def refuse_any(input):
            return f"Sorry I am a creative writing agent so I cannot help with that. a brief summary of your input: {input[:100]}..."  
        def small_talk(input):
            return "Hello! I can help with creative writing or analysis. What would you like to do?"
        tool1=Tool(name="clarify", func=clarify, description="Asks the user to clarify if input is unclear.")
        tool2=Tool(name="refuse_any", func=refuse_any, description="Refuses off-topic inputs politely.")
        tool3=Tool(name="small_talk", func=small_talk, description="Handles greetings or off-topic messages.")
        self.fallback_tools=[tool1, tool2, tool3]
    def initialize_fallback_agent(self):
        self.setup_fallback_tools()
        self.fallback_agent=initialize_agent(tools=self.fallback_tools, llm=self.llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, memory=self.memory, verbose=True)
    def run_creative_agent(self, query):
        return self.creative_agent.run(query)   
    def run_fallback_agent(self, query):
        return self.fallback_agent.run(query)     