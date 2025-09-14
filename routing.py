from langchain.chains.router import RouterChain
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from agentWrapper import AgentWrapper
class Routing:
    def __init__(self, agentInstance1, agentInstance2, gemini_key, query):
        self.agentInstance1=agentInstance1
        self.agentInstance2=agentInstance2
        
        wrapperInstance=AgentWrapper(self.agentInstance1, "creative")
        wrapperInstance({"query":query})
        
        
        
        router_model=ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=gemini_key)
        
        router_prompt=PromptTemplate(input_variables=["query"], template="Given this user input: {query}, decide which agent should respond: creative or fallback.")
        self.router_llm_chain=LLMChain(llm=self.router_model, prompt=router_prompt)
        
    def route(self):    
        router_chain=RouterChain.from_chains(destination_chains={"creative_chain":self.agentInstance1.run_creative_agent(query), "fallback_chain":}, router_chain=self.router_llm_chain, default_chain=self.agentInstance2.run_fallback_agent(query), verbose=True)
    