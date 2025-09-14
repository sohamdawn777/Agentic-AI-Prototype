from langchain.chains.base import Chain
from pydantic import Field

class AgentWrapper(Chain):   
     
     @property
     def input_keys(self):
         return ["query"]
     @property
     def output_keys(self):
         return ["answer"]
     def _call(self, inputs):
         query=inputs["query"]
         if self.mode=="creative":
             result= self.agent_instance.run_creative_agent(query)
         else:
             result= self.agent_instance.run_fallback_agent(query)    
         return {"answer": result}    