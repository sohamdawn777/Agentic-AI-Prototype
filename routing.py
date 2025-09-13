class Routing:
    def __init__(self, agentInstance):
        self.agentInstance=agentInstance
    def run_instance(self, query):
        self.agentInstance.run_agent(query)
        