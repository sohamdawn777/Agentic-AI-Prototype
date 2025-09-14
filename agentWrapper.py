from langchain.chains.base import Chain

class AgentWrapper(Chain):   
     def __init__(agent_instance,mode):
         super().__init__()
         self.agent_instance=agent_instance
         self.mode=mode
     @property
     def input_keys(self):
         return ["query"]
     @property
     def output_keys(self):
         return ["answer"]
     def _call(self, inputs):
         query=inputs["query"]
         if self.mode=="creative":
             result= agent_instance.run_creative_agent(query)
         else:
             result= agent_instance.run_fallback_agent(query)    