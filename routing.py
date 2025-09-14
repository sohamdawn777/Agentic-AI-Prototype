from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from agentWrapper import AgentWrapper
class Routing:
    def __init__(self, agentInstance1, agentInstance2, gemini_key):
        self.agentInstance1=agentInstance1
        self.agentInstance2=agentInstance2

        self.wrapperInstance1=AgentWrapper(agent_instance=self.agentInstance1, mode="creative")
        self.wrapperInstance2=AgentWrapper(agent_instance=self.agentInstance2, mode="fallback")

        self.router_model=ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=gemini_key)
    def route(self, query):    
        router_prompt=PromptTemplate(input_variables=["query"], template="""You are a strict router. Given this user input: {query}. Return exactly one of the following keys (and nothing else): creative_chain, fallback_chain. Answer with only the key name.""")
        router_llm_chain=LLMChain(llm=self.router_model, prompt=router_prompt)
        decision=router_llm_chain.run({"query":query}).strip()
        print("tichkule tangra redfty: ",repr(decision))

        if decision not in ["creative_chain", "fallback_chain"]:
            decision="fallback_chain"

        if decision=="creative_chain":
            final_result=self.wrapperInstance1({"query":query})
            return final_result["answer"]
        else:
            final_result=self.wrapperInstance2({"query":query})    
            return final_result["answer"]