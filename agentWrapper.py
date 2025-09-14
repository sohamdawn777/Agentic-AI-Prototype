 class AgnetWrapper(Chain):   
     def __init__(agentInstance1, agentInstance2):
         super().__init__()
         self.agentInstance1=agentInstance1
         self.agentInstance2=agentInstance2
     @property
     def input_keys(self):
         return ["query"]
     @property
     def output_keys(self):
         return ["answer"]
     def _call(self, inputs):
         query=inputs["query"]
             