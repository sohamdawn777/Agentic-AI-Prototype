from langchain.chains.router import RouterChain
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from agentWrapper import AgentWrapper
class Routing:
    def __init__(self, agentInstance1, agentInstance2, gemini_key):
        self.agentInstance1=agentInstance1
        self.agentInstance2=agentInstance2

        self.wrapperInstance1=AgentWrapper(self.agentInstance1, "creative")
        self.wrapperInstance2=AgentWrapper(self.agentInstance2, "fallback")

        self.router_model=ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=gemini_key)
    def route(self, query):    
        router_prompt=PromptTemplate(input_variables=["query"], template="Given this user input: {query}, decide which agent should respond: creative_chain or fallback_chain.")
        router_llm_chain=LLMChain(llm=self.router_model, prompt=router_prompt)
        router_chain=RouterChain.from_chains(destination_chains={"creative_chain":self.wrapperInstance1, "fallback_chain":self.wrapperInstance2}, router_chain=router_llm_chain, default_chain=self.wrapperInstance2, verbose=True)
        return router_chain.run({"query":query})