from langchain.chains.router import RouterChain
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from agentWrapper import AgentWrapper
class Routing:
    def __init__(self, agentInstance1, agentInstance2, gemini_key, query):
        self.agentInstance1=agentInstance1
        self.agentInstance2=agentInstance2

        wrapperInstance1=AgentWrapper(self.agentInstance1, "creative")
        wrapperInstance2=AgentWrapper(self.agentInstance2, "fallback")


        router_model=ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=gemini_key)

        router_prompt=PromptTemplate(input_variables=["query"], template="Given this user input: {query}, decide which agent should respond: creative or fallback.")
        router_llm_chain=LLMChain(llm=router_model, prompt=router_prompt)
        
        self.router_chain=RouterChain.from_chains(destination_chains={"creative_chain":wrapperInstance1, "fallback_chain":wrapperInstance2}, router_chain=router_llm_chain, default_chain=wrapperInstance2, verbose=True)
    def route(self, query):    
        return self.router_chain.run({"query":query})