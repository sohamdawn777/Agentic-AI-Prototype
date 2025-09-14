from langchain.chains.router import RouterChain
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
class Routing(Chain):
    def __init__(self, agentInstance1, agentInstance2, gemini_key):
        super().__init__()
        self.agentInstance1=agentInstance1
        self.agentInstance2=agentInstance2
        
        self.router_model=ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=gemini_key)
    @property
    def input_keys(self):
        return ["query"]
    @property
    def output_keys(self):
        return ["answer"]
    
    def _call(self, inputs):
        query=inputs["query"]
        
        router_prompt=PromptTemplate(input_variables=["query"], template="Given this user input: {query}, decide which agent should respond: creative or fallback.")
        router_llm_chain=LLMChain(llm=self.router_model, prompt=router_prompt)
        
        router_chain=RouterChain.from_chains(destination_chains={"creative_chain":self.agentInstance1.run_creative_agent(query), "fallback_chain":self.agentInstance2.run_fallback_agent(query)}, router_chain=router_llm_chain, default_chain=self.agentInstance2.run_fallback_agent(query), verbose=True)
    